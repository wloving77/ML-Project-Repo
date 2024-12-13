def preprocess_query(query: str):
    query = None
    processed_query = ""
    return processed_query

def generate_query_embedding(query: str):
    query_embedding = None
    return query_embedding

def retrieve_relevant_papers(query_embedding):
    try:
        connection = psycopg2.connect(
            host='vector-db', 
            user='mlteam',
            password='mlteam',
            database='cs_research_vectordb' 
        )
        cursor = connection.cursor()

        vector = np.array(query_embedding).tolist() 

        cursor.execute("""
            SELECT paper_id, vector
            FROM embeddings
            ORDER BY vector <=> %s  -- <=> is the operator for pgvector to compute similarity
            LIMIT 5
        """, (vector,))

        papers = cursor.fetchall()

    except psycopg2.Error as e:
        print(f"Error retrieving relevant papers: {e}")
        papers = []
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    return papers


def generate_response_from_llm(retrieved_papers):
    response = None
    return response


def return_response(response):
    print(f"Response to user: {response}") 