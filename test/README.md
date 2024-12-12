# Just trying to get the full pipeline together here, database, embeddings stored in database etc.

1. Run `python3 -m venv .venv` which just creates a virtual environment
2. Run `pip install -r requirements.txt` to install dependencies
    - Python versions around `3.9` seems to be ideal
3. Run `docker-compose up` which will create and initialize the database state.
4. Navigate to `sandbox.ipynb` and basically run the entire thing, this populates the database and tests the embedding stuff, it works decently well (well enough)