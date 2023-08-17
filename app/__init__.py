"""App Modules."""
import os

if os.getenv("ENVIRONMENT") == "LOCAL":  # pragma: no cover
    from dotenv import load_dotenv

    load_dotenv()
