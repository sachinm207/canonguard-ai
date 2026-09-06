from .seed_universes import seed_all_universes, generate_pseudo_embedding

def seed_chronoverse_data():
    """
    Seeds all canonical franchise universes into the engine.
    Maintained for backwards compatibility with tests and main.py lifespan.
    """
    seed_all_universes()

if __name__ == "__main__":
    seed_chronoverse_data()
