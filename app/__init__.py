import os

if os.getenv("ENVIRONMENT") == "LOCAL":
    from dotenv import load_dotenv

    load_dotenv()
