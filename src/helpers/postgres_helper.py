import psycopg
from psycopg import OperationalError
from dotenv import load_dotenv
import os


class PostgresConnector:
    def __init__(self):
        """
        Initializes the PostgresConnector class with connection details.

        :param host: Database host
        :param database: Database name
        :param user: Username
        :param password: Password
        :param port: Port (default: 5432)
        """
        self.host = os.getenv("POSTGRES_HOST")
        self.dbname = os.getenv("POSTGRES_DB")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.port = os.getenv("POSTGRES_PORT")
        self.connection = None

    def create_connection(self):
        """
        Establishes a connection to the PostgreSQL database.

        :return: None
        """
        try:
            self.connection = psycopg.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def close_connection(self):
        """
        Closes the connection to the PostgreSQL database if it is open.

        :return: None
        """
        if self.connection:
            self.connection.close()
            print("The connection to the PostgreSQL DB is closed")

    def insert_professor_and_paper(
        self, professor_name, paper_title, paper_abstract, paper_embedding, paper_link
    ):
        """
        Inserts a professor and a paper into the database. Checks if the professor already exists.

        :param professor_name: Name of the professor
        :param paper_title: Title of the paper
        :param paper_abstract: Abstract of the paper
        :param paper_embedding: Embedding vector (e.g., 768-dimensional or 384-dimensional)
        :param paper_link: Link to the paper
        """
        try:
            with self.connection.cursor() as cur:
                # Check if professor already exists
                cur.execute(
                    """
                    SELECT id FROM professors WHERE name = %s;
                    """,
                    (professor_name,),
                )
                result = cur.fetchone()

                if result:
                    # If professor exists, get their ID
                    professor_id = result[0]
                    print(
                        f"Professor '{professor_name}' exists with ID {professor_id}."
                    )
                else:
                    # Insert new professor
                    cur.execute(
                        """
                        INSERT INTO professors (name)
                        VALUES (%s)
                        RETURNING id;
                        """,
                        (professor_name,),
                    )
                    professor_id = cur.fetchone()[0]
                    print(
                        f"Inserted new professor '{professor_name}' with ID {professor_id}."
                    )

                # Insert paper linked to the professor
                cur.execute(
                    """
                    INSERT INTO papers (professor_id, title, abstract, embedding, paper_link)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        professor_id,
                        paper_title,
                        paper_abstract,
                        paper_embedding,
                        paper_link,
                    ),
                )

                self.connection.commit()
                print("Professor and paper inserted successfully.")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"An error occurred: {e}")

    def find_similar_papers(self, embedding, n=5):
        """
        Finds the n most similar papers to a given embedding.

        :param embedding: A 768-dimensional embedding vector (list of floats).
        :param n: The number of most similar papers to return.
        :return: A list of dictionaries containing paper details including author.
        """
        try:
            with self.connection.cursor() as cur:
                # Query to find the most similar papers based on cosine similarity
                cur.execute(
                    """
                    SELECT p.id, p.title, p.abstract, p.paper_link, p.embedding <=> %s::vector AS similarity, pr.name AS author
                    FROM papers p
                    JOIN professors pr ON p.professor_id = pr.id
                    ORDER BY similarity
                    LIMIT %s;
                    """,
                    (embedding, n),
                )
                # Fetch results
                results = cur.fetchall()
                return [
                    {
                        "id": row[0],
                        "title": row[1],
                        "abstract": row[2],
                        "paper_link": row[3],
                        "similarity": row[4],
                        "author": row[5],
                    }
                    for row in results
                ]
        except Exception as e:
            print(f"An error occurred while querying similar papers: {e}")
            return []
