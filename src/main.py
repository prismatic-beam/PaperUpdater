"""Small CLI to check and update the local PaperMC server jar."""
import argparse
import logging
import sys
import os
from pathlib import Path

from dotenv import load_dotenv
import localtracker, fileops


def main() -> int:
    # Get the directory where main.py is located (src/)
    script_dir = Path(__file__).resolve().parent
    # Look for .env in the parent directory of src/
    dotenv_path = script_dir.parent / '.env'

    load_dotenv(dotenv_path=dotenv_path)
    p = argparse.ArgumentParser(description="Check PaperMC remote and update local jar if needed")
    p.add_argument("--dir", "-d", default=os.getenv("PAPER_DIR", "."), type=Path, help="Directory containing the server jar")
    p.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    p.add_argument("--restore", "-r", action="store_true", help="Restore the most recent .old jar and exit")
    args = p.parse_args()
    dir_path: Path = args.dir # Type hint for autocomplete

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")

    if not dir_path.exists():
        logging.error("Directory does not exist: %s", args.dir)
        return 2

    if args.restore:
        try:
            restored = fileops.restore_backup(args.dir)
            if restored:
                logging.info("Restored: %s", restored.name)
            else:
                logging.info("No backups found to restore.")
            return 0
        except Exception:
            logging.exception("Restore failed")
            return 1

    if localtracker.update_server(args.dir):
        logging.info("Server updated successfully.")
    else:
        logging.info("Server is up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
