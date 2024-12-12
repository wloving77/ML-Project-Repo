# Guide for Getting Up and Running Locally:

1. Configure a `.env` file, you need:
    - POSTGRES_USER=wloving77
    - POSTGRES_PASSWORD=secure_password
    - POSTGRES_DB=ml_project
    - GEMINI_API_KEY=YOUR_GEMINI_API_KEY
2. Run `docker-compose up` in `app_src` directory
3. Run `python3 populate_db.py` in the `app_src` directory to populate the database, this will take a few minutes for sure
4. Navigate to `0.0.0.0:8050` in your browser and you should see a dashy app.
5. Try it out! It is by no means great but it does work which is cool, probably need more thorough embeddings (maybe the full papers going forward or smthn)