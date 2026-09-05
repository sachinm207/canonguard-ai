-- =====================================================================
-- CanonGuard AI: ClickHouse High-Performance Columnar Schema
-- Target Track: ClickHouse Partner Track
-- Features: ReplacingMergeTree, Vector Cosine Distance, Temporal Range Keys
-- =====================================================================

-- 1. Franchise Characters & Life Status Table
CREATE TABLE IF NOT EXISTS franchise_characters (
    character_id UUID DEFAULT generateUUIDv4(),
    universe_id LowCardinality(String),
    name String,
    aliases Array(String),
    species LowCardinality(String),
    birth_year Int32,
    death_year Nullable(Int32),
    status Enum8('ALIVE' = 1, 'DEAD' = 2, 'STASIS' = 3, 'EXILED' = 4, 'UNKNOWN' = 5),
    stasis_start_year Nullable(Int32),
    stasis_end_year Nullable(Int32),
    home_planet LowCardinality(String),
    powers Array(String),
    created_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(created_at)
ORDER BY (universe_id, name, character_id);

-- 2. Canonical Timeline Events with Vector Search
CREATE TABLE IF NOT EXISTS canon_timeline_events (
    event_id UUID DEFAULT generateUUIDv4(),
    universe_id LowCardinality(String),
    canon_tier Enum8('TIER_1_MOVIE' = 1, 'TIER_2_TV_SHOW' = 2, 'TIER_3_NOVEL' = 3, 'TIER_4_COMIC' = 4),
    canonical_year Int32,
    location String,
    participants Array(String),
    summary String,
    source_media String,
    embedding Array(Float32),
    created_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(created_at)
ORDER BY (universe_id, canonical_year, event_id);

-- 3. Temporal Entity Relationships (Causal Triples)
CREATE TABLE IF NOT EXISTS entity_relationships (
    relationship_id UUID DEFAULT generateUUIDv4(),
    universe_id LowCardinality(String),
    subject_name String,
    predicate LowCardinality(String), -- 'POSSESSES', 'ALLIED_WITH', 'KILLED', 'LOCATED_AT', 'CREATED'
    object_name String,
    valid_from_year Int32,
    valid_to_year Nullable(Int32),
    status Enum8('ACTIVE' = 1, 'DESTROYED' = 2, 'SEVERED' = 3),
    source_media String,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (universe_id, subject_name, predicate, valid_from_year);

-- 4. Universal Lore Invariants & Physical Laws
CREATE TABLE IF NOT EXISTS canon_lore_rules (
    rule_id UUID DEFAULT generateUUIDv4(),
    universe_id LowCardinality(String),
    category LowCardinality(String), -- 'BIOLOGY', 'PHYSICS', 'MAGIC', 'TECHNOLOGY'
    entity_or_species String,
    rule_statement String,
    canon_tier Enum8('ABSOLUTE' = 1, 'RETRACTABLE' = 2),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (universe_id, category, entity_or_species);

-- 5. Audit & Telemetry Log for Retcon Interceptions
CREATE TABLE IF NOT EXISTS audit_retcon_logs (
    log_id UUID DEFAULT generateUUIDv4(),
    universe_id LowCardinality(String),
    screenplay_title String,
    flagged_line String,
    violation_type LowCardinality(String),
    mitigation_suggested String,
    mitigation_accepted UInt8,
    query_latency_ms Float32,
    timestamp DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (universe_id, timestamp);
