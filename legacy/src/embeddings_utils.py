

def scrape():
    print("Hello World!")

def clean():
    print("Hello World!")


def create_embeddings(data):
    embeddings = None
    return embeddings

def upload_to_mysql(paper_data):
    
    db = MySQLdb.connect(
        host="mysql-db", 
        user="mlteam",
        passwd="mlteam",
        db="cs_research_db"
    )
    
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO papers (title, authors, publication_date, journal, abstract, url, keywords)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            paper_data['title'],
            paper_data['authors'],
            paper_data['publication_date'],
            paper_data['journal'],
            paper_data['abstract'],
            paper_data['url'],
            paper_data['keywords']
        ))
        
        db.commit()
        
    except MySQLdb.Error as e:
        print(f"Error inserting data into MySQL: {e}")
        db.rollback()
    
    finally:
        cursor.close()
        db.close()

def upload_to_vector_db(paper_id, vector_embeddings):    
    conn = psycopg2.connect(
        host="vector-db", 
        user="mlteam",
        password="mlteam",
        dbname="ml_team_vectors"
    )
    
    cursor = conn.cursor()
    vector = np.array(vector_embedding).tolist()

    try:
        cursor.execute("""
            INSERT INTO embeddings (paper_id, vector)
            VALUES (%s, %s)
        """, (paper_id, vector))

        conn.commit()
        
    except psycopg2.Error as e:
        print(f"Error inserting data into PostgreSQL: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()