# Guide for Getting Up and Running Locally:

1. Configure a `prod.env` file, in it you need:
    - POSTGRES_USER=wloving77 // you can change this arbitrarily
    - POSTGRES_PASSWORD=secure_password // you can change this arbitrarily
    - POSTGRES_DB=ml_project // you can change this arbitrarily
    - POSTGRES_HOST=postgres_server // this is essential for docker and cannot be changed
    - POSTGRES_PORT=5432 // this is essential for docker and cannot be changed
    - GEMINI_API_KEY=YOUR_GEMINI_API_KEY
2. Run `docker-compose up` in `./src` directory
3. Run `docker exec -it dashy_server python3 populate_db.py` to populate the database, this will take a few minutes
4. Navigate to `0.0.0.0:8050` in your browser and you should see a dashy app.
5. Try it out! Link to [Github](https://github.com/wloving77/ML-Project-Repo/tree/williams-branch)


# Notes:

1. You should only have to populate the database once, all of the data will be stored in this `./src/pgdata/` directory and everytime `docker-compose up` is run the database data is read in from there.