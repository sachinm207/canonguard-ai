"""
ClickHouse Cloud Setup & Migration Utility for CanonGuard AI.
Connects to ClickHouse Cloud (or any target instance), initializes the schema,
and seeds all franchise lore facts into native tables.
"""
import os
import sys
import time
import logging
from ..config import settings
from .clickhouse import ch_engine
from .seed_universes import seed_all_universes

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("canonguard.setup_cloud")

def setup_clickhouse_cloud():
    print("=" * 70)
    print("🚀 CanonGuard AI: ClickHouse Cloud Setup & Migration Engine")
    print("=" * 70)
    print(f"Target Host:     {settings.CLICKHOUSE_HOST}")
    print(f"Target Port:     {settings.CLICKHOUSE_PORT}")
    print(f"Target Database: {settings.CLICKHOUSE_DATABASE}")
    print(f"Secure TLS:      {settings.CLICKHOUSE_SECURE}")
    print(f"User:            {settings.CLICKHOUSE_USER}")
    print("-" * 70)

    try:
        import clickhouse_connect
        start_t = time.perf_counter()
        client = clickhouse_connect.get_client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            username=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DATABASE,
            secure=settings.CLICKHOUSE_SECURE,
            connect_timeout=10
        )
        ping_latency = (time.perf_counter() - start_t) * 1000.0
        server_ver = client.command("SELECT version()")
        print(f"✅ Successfully connected to ClickHouse Server v{server_ver} ({ping_latency:.2f}ms latency)")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPlease ensure your environment variables are configured correctly in .env:")
        print("CLICKHOUSE_HOST=your-cluster.clickhouse.cloud")
        print("CLICKHOUSE_PORT=8443")
        print("CLICKHOUSE_PASSWORD=your-password")
        print("CLICKHOUSE_SECURE=true")
        sys.exit(1)

    # 1. Execute schema.sql
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    print(f"📄 Reading schema from {schema_path}...")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Split on semicolons for individual DDL execution
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip() and not stmt.strip().startswith("--")]
    for stmt in statements:
        try:
            client.command(stmt)
        except Exception as e:
            logger.warning(f"Notice executing statement: {e}")

    print(f"✅ Initialized {len(statements)} tables and engines in ClickHouse.")

    # 2. Seed all universes into native tables
    print("🎬 Seeding franchise lore facts into ClickHouse tables...")
    ch_engine.client = client
    ch_engine.is_native = True
    seed_all_universes()

    # 3. Verify counts
    chars_cnt = client.command("SELECT count() FROM franchise_characters")
    events_cnt = client.command("SELECT count() FROM canon_timeline_events")
    rels_cnt = client.command("SELECT count() FROM entity_relationships")
    rules_cnt = client.command("SELECT count() FROM canon_lore_rules")

    print("=" * 70)
    print("🎉 ClickHouse Cloud Setup Complete!")
    print(f"   • franchise_characters: {chars_cnt} rows")
    print(f"   • entity_relationships: {rels_cnt} rows")
    print(f"   • canon_lore_rules:     {rules_cnt} rows")
    print(f"   • canon_timeline_events:{events_cnt} rows")
    print("=" * 70)

if __name__ == "__main__":
    setup_clickhouse_cloud()
