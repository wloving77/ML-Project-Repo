from sentence_transformers import SentenceTransformer


class EmbeddingHelper:

    def __init__(self):
        pass

    def create_embedding(self, text: str, model_name: str = "all-MiniLM-L6-v2") -> list:
        """
        Generate an embedding for the given text using Sentence-Transformers.

        Args:
            text (str): The input text to embed.
            model_name (str): The name of the Sentence-Transformers model to use.
                            Default is 'all-MiniLM-L6-v2'.

        Returns:
            list: A list representing the embedding vector for the input text.
        """
        try:
            # Load the model
            model = SentenceTransformer(model_name)

            # Generate embedding
            embedding = model.encode(text, convert_to_numpy=True).tolist()

            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise
