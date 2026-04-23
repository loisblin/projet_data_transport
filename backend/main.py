import argparse
import logging
from backend.seeds import generate_seed_data
from backend.tables import create_tables, delete_tables

def main():
    """CLI tool to manage database and seed data."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--create", "-c", action="store_true", help="Create database tables")
    parser.add_argument("--reset", "-r", action="store_true", help="Reset database tables")
    parser.add_argument("--seed", "-s",nargs="?", type=int, const=1000, default=None, help="Number of seeds to generate (default: 1000)")

    args = parser.parse_args()
    
    try:
        # DEFAULT BEHAVIOR
        if not any([args.create, args.reset, args.seed]):
            logging.info("No args provided -> resetting DB + seeding 1000")
            delete_tables()
            create_tables()
            generate_seed_data(n=1000)
            return # stop function

        # MANUAL CONTROL
        # validation
        if args.create and args.reset:
            logging.error("Cannot use --create and --reset together")
            raise ValueError("Incompatible options: --create and --reset")
        
        if args.create:
            logging.info("Starting create tables")
            create_tables()

        if args.reset:
            logging.info("Starting reset tables")
            delete_tables()
            create_tables()

        if args.seed:
            logging.info("Starting seed")
            generate_seed_data(n=args.seed)

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()