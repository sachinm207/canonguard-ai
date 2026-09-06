import time
import uuid
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from ..config import settings

logger = logging.getLogger("canonguard.db")

class ClickHouseEngine:
    """
    Dual-mode Sub-20ms Columnar & Vector Engine for CanonGuard AI.
    - Native Mode: Connects to ClickHouse Cloud / Cluster via clickhouse-connect.
    - Embedded Columnar Mode: High-speed in-memory columnar store mimicking ClickHouse
      ReplacingMergeTree & vector cosine search when external cluster is offline.
    """
    def __init__(self):
        self.client = None
        self.is_native = False
        self._init_connection()

    def _init_connection(self):
        try:
            import clickhouse_connect
            self.client = clickhouse_connect.get_client(
                host=settings.CLICKHOUSE_HOST,
                port=settings.CLICKHOUSE_PORT,
                username=settings.CLICKHOUSE_USER,
                password=settings.CLICKHOUSE_PASSWORD,
                database=settings.CLICKHOUSE_DATABASE,
                secure=settings.CLICKHOUSE_SECURE,
                connect_timeout=2
            )
            # Ping test
            self.client.command("SELECT 1")
            self.is_native = True
            logger.info("Connected to native ClickHouse instance successfully.")
        except Exception as e:
            logger.warning(f"Native ClickHouse unavailable ({e}). Initializing High-Performance Embedded Columnar Engine.")
            self.is_native = False
            self._init_embedded_tables()

    def _init_embedded_tables(self):
        # Columnar In-Memory Storage
        self.characters: List[Dict[str, Any]] = []
        self.timeline_events: List[Dict[str, Any]] = []
        self.relationships: List[Dict[str, Any]] = []
        self.lore_rules: List[Dict[str, Any]] = []
        self.audit_logs: List[Dict[str, Any]] = []
        self.universes: Dict[str, Dict[str, Any]] = {}
        self.active_universe_id: str = settings.UNIVERSE_ID

    def switch_universe(self, universe_id: str) -> bool:
        """Switch the active franchise canon in the engine."""
        if not self.universes:
            from .seed_universes import seed_all_universes
            seed_all_universes()
        for uid in self.universes:
            if uid.lower() == universe_id.lower():
                self.active_universe_id = uid
                return True
        return False

    def get_active_universe(self) -> Dict[str, Any]:
        """Returns the currently active franchise metadata."""
        if not self.universes:
            from .seed_universes import seed_all_universes
            seed_all_universes()
        return self.universes.get(self.active_universe_id, {
            "id": self.active_universe_id,
            "name": self.active_universe_id,
            "default_year": 1982,
            "default_location": "Berlin Safehouse",
            "default_title": "Active_Script.fountain",
            "demo_traps": []
        })

    def get_all_universes(self) -> List[Dict[str, Any]]:
        """Returns all loaded canons with active indicators."""
        if not self.universes:
            from .seed_universes import seed_all_universes
            seed_all_universes()
        result = []
        for uid, udata in self.universes.items():
            u_copy = dict(udata)
            u_copy["is_active"] = (uid == self.active_universe_id)
            # Add character and event counts for UI display
            u_copy["characters_count"] = len([c for c in self.characters if c.get("universe_id") == uid])
            u_copy["events_count"] = len([e for e in self.timeline_events if e.get("universe_id") == uid])
            u_copy["rules_count"] = len([r for r in self.lore_rules if r.get("universe_id") == uid])
            result.append(u_copy)
        return result

    def ingest_custom_universe(
        self,
        universe_id: str,
        name: str,
        genre: str,
        era: str,
        description: str,
        characters: List[Dict[str, Any]],
        timeline_events: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        lore_rules: List[Dict[str, Any]],
        default_year: int = 2026,
        default_location: str = "Central Facility",
        demo_traps: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Ingests a user-uploaded story bible or custom canon into ClickHouse."""
        self.universes[universe_id] = {
            "id": universe_id,
            "name": name,
            "genre": genre,
            "era": era,
            "description": description,
            "default_year": default_year,
            "default_location": default_location,
            "default_title": f"{name.replace(' ', '_')}.fountain",
            "demo_traps": demo_traps or []
        }
        for c in characters:
            c["universe_id"] = universe_id
        for e in timeline_events:
            e["universe_id"] = universe_id
        for r in relationships:
            r["universe_id"] = universe_id
        for rule in lore_rules:
            rule["universe_id"] = universe_id

        self.characters.extend(characters)
        self.timeline_events.extend(timeline_events)
        self.relationships.extend(relationships)
        self.lore_rules.extend(lore_rules)
        self.active_universe_id = universe_id
        return self.universes[universe_id]

    def check_character_status(self, character_names: List[str], scene_year: int) -> Dict[str, Any]:
        """
        Executes sub-20ms temporal invariant verification for characters.
        Checks if character is DEAD, in STASIS, or UNBORN relative to scene_year.
        """
        start_time = time.perf_counter()
        normalized_names = [n.strip().lower() for n in character_names if n.strip()]
        if not normalized_names:
            return {"results": [], "latency_ms": 0.0}

        results = []

        if self.is_native and self.client:
            try:
                query = """
                SELECT 
                    name, 
                    species, 
                    birth_year, 
                    death_year, 
                    status, 
                    stasis_start_year, 
                    stasis_end_year,
                    if(death_year IS NOT NULL AND {year:Int32} > death_year, 'DEAD_BEFORE_SCENE',
                       if({year:Int32} < birth_year, 'UNBORN_BEFORE_SCENE', 
                          if(stasis_start_year IS NOT NULL AND {year:Int32} >= stasis_start_year AND ({year:Int32} <= ifNull(stasis_end_year, 9999)), 'IN_CRYOGENIC_STASIS', 'VALID_ACTIVE')
                       )
                    ) AS temporal_evaluation
                FROM franchise_characters
                WHERE universe_id = {univ:String}
                  AND lower(name) IN ({names:Array(String)})
                LIMIT 10
                """
                res = self.client.query(query, parameters={
                    "year": scene_year,
                    "univ": self.active_universe_id,
                    "names": normalized_names
                })
                for row in res.result_rows:
                    results.append({
                        "name": row[0],
                        "species": row[1],
                        "birth_year": row[2],
                        "death_year": row[3],
                        "status": row[4],
                        "stasis_start_year": row[5],
                        "stasis_end_year": row[6],
                        "evaluation": row[7]
                    })
            except Exception as e:
                logger.error(f"ClickHouse query failed: {e}. Falling back to embedded columnar.")
                return self._embedded_check_characters(normalized_names, scene_year, start_time)
        else:
            return self._embedded_check_characters(normalized_names, scene_year, start_time)

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return {"results": results, "latency_ms": round(latency_ms, 2)}

    def _embedded_check_characters(self, normalized_names: List[str], scene_year: int, start_time: float) -> Dict[str, Any]:
        results = []
        for char in self.characters:
            if char.get("universe_id") and char.get("universe_id") != self.active_universe_id:
                continue
            char_name = char["name"].lower()
            aliases = [a.lower() for a in char.get("aliases", [])]
            if char_name in normalized_names or any(a in normalized_names for a in aliases):
                evaluation = "VALID_ACTIVE"
                b_year = char.get("birth_year", -9999)
                d_year = char.get("death_year")
                s_start = char.get("stasis_start_year")
                s_end = char.get("stasis_end_year")

                if d_year is not None and scene_year > d_year:
                    evaluation = "DEAD_BEFORE_SCENE"
                elif scene_year < b_year:
                    evaluation = "UNBORN_BEFORE_SCENE"
                elif s_start is not None and scene_year >= s_start and (s_end is None or scene_year <= s_end):
                    evaluation = "IN_CRYOGENIC_STASIS"

                results.append({
                    "name": char["name"],
                    "species": char.get("species", "HUMAN"),
                    "birth_year": b_year,
                    "death_year": d_year,
                    "status": char.get("status", "ALIVE"),
                    "stasis_start_year": s_start,
                    "stasis_end_year": s_end,
                    "evaluation": evaluation
                })

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return {"results": results, "latency_ms": round(latency_ms, 2)}

    def check_relic_and_relationship_status(self, object_names: List[str], scene_year: int) -> Dict[str, Any]:
        """
        Executes sub-20ms causal graph lookup on artifacts, items, or ties.
        Checks if an item was DESTROYED prior to scene_year.
        """
        start_time = time.perf_counter()
        normalized = [o.strip().lower() for o in object_names if o.strip()]
        if not normalized:
            return {"results": [], "latency_ms": 0.0}

        results = []
        if self.is_native and self.client:
            try:
                query = """
                SELECT 
                    subject_name, 
                    predicate, 
                    object_name, 
                    valid_from_year, 
                    valid_to_year, 
                    status, 
                    source_media
                FROM entity_relationships
                WHERE universe_id = {univ:String}
                  AND (lower(object_name) IN ({objs:Array(String)}) OR lower(subject_name) IN ({objs:Array(String)}))
                LIMIT 10
                """
                res = self.client.query(query, parameters={
                    "univ": self.active_universe_id,
                    "objs": normalized
                })
                for row in res.result_rows:
                    valid_to = row[4]
                    stat = row[5]
                    evaluation = "ACTIVE"
                    if stat == "DESTROYED" or (valid_to is not None and scene_year > valid_to):
                        evaluation = "DESTROYED_OR_INACTIVE"

                    results.append({
                        "subject_name": row[0],
                        "predicate": row[1],
                        "object_name": row[2],
                        "valid_from_year": row[3],
                        "valid_to_year": valid_to,
                        "status": stat,
                        "source_media": row[6],
                        "evaluation": evaluation
                    })
            except Exception as e:
                logger.error(f"Relationship query failed: {e}")
                return self._embedded_check_relics(normalized, scene_year, start_time)
        else:
            return self._embedded_check_relics(normalized, scene_year, start_time)

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return {"results": results, "latency_ms": round(latency_ms, 2)}

    def _embedded_check_relics(self, normalized: List[str], scene_year: int, start_time: float) -> Dict[str, Any]:
        results = []
        for rel in self.relationships:
            if rel.get("universe_id") and rel.get("universe_id") != self.active_universe_id:
                continue
            subj = rel["subject_name"].lower()
            obj = rel["object_name"].lower()
            if subj in normalized or obj in normalized:
                valid_to = rel.get("valid_to_year")
                stat = rel.get("status", "ACTIVE")
                evaluation = "ACTIVE"
                if stat == "DESTROYED" or (valid_to is not None and scene_year > valid_to):
                    evaluation = "DESTROYED_OR_INACTIVE"

                results.append({
                    "subject_name": rel["subject_name"],
                    "predicate": rel.get("predicate", "POSSESSES"),
                    "object_name": rel["object_name"],
                    "valid_from_year": rel.get("valid_from_year", 0),
                    "valid_to_year": valid_to,
                    "status": stat,
                    "source_media": rel.get("source_media", "Canon Core"),
                    "evaluation": evaluation
                })

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return {"results": results, "latency_ms": round(latency_ms, 2)}

    def get_lore_rules(self, category: Optional[str] = None, entity_or_species: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetches universe axioms (e.g. Atmosphere composition, FTL laws).
        """
        rules = []
        for rule in self.lore_rules:
            if rule.get("universe_id") and rule.get("universe_id") != self.active_universe_id:
                continue
            if category and rule.get("category", "").lower() != category.lower():
                continue
            if entity_or_species and entity_or_species.lower() not in rule.get("entity_or_species", "").lower():
                continue
            rules.append(rule)
        return rules

    def search_similar_events(self, query_vec: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Vector similarity search over canon_timeline_events using cosine distance.
        """
        if not self.timeline_events or not query_vec:
            return []

        q_vec = np.array(query_vec, dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []

        scored_events = []
        for event in self.timeline_events:
            if event.get("universe_id") and event.get("universe_id") != self.active_universe_id:
                continue
            e_vec = np.array(event["embedding"], dtype=np.float32)
            e_norm = np.linalg.norm(e_vec)
            if e_norm == 0:
                continue
            cos_dist = 1.0 - (np.dot(q_vec, e_vec) / (q_norm * e_norm))
            scored_events.append((cos_dist, event))

        scored_events.sort(key=lambda x: x[0])
        return [item[1] for item in scored_events[:top_k]]

    def record_audit_log(self, screenplay_title: str, flagged_line: str, violation_type: str, mitigation: str, latency_ms: float):
        log_entry = {
            "log_id": str(uuid.uuid4()),
            "universe_id": self.active_universe_id,
            "screenplay_title": screenplay_title,
            "flagged_line": flagged_line,
            "violation_type": violation_type,
            "mitigation_suggested": mitigation,
            "mitigation_accepted": 0,
            "query_latency_ms": latency_ms,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.audit_logs.append(log_entry)
        if self.is_native and self.client:
            try:
                self.client.insert("audit_retcon_logs", [[
                    log_entry["log_id"],
                    log_entry["universe_id"],
                    log_entry["screenplay_title"],
                    log_entry["flagged_line"],
                    log_entry["violation_type"],
                    log_entry["mitigation_suggested"],
                    0,
                    latency_ms,
                    log_entry["timestamp"]
                ]])
            except Exception as e:
                logger.error(f"Failed to record native audit log: {e}")

# Global Singleton Instance
ch_engine = ClickHouseEngine()
