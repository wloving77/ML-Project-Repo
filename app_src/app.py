# Dashy app for displaying our data

import dash
from dash import dcc, html, Input, Output, State
import json
from helpers import postgres_helper, embedding_helper, LLM_helpers
from dotenv import load_dotenv

# environment variables, PG stuff and gemini API key
load_dotenv("prod.env")

# For development:
# load_dotenv("dev.env")

pg_helper = postgres_helper.PostgresConnector()
embed_helper = embedding_helper.EmbeddingHelper()
LLM_helpers = LLM_helpers.GeminiLLMHelper()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    [
        # Text input for the user query
        dcc.Input(
            id="user-query",
            type="text",
            placeholder="Enter your query...",
            style={"width": "100%", "marginBottom": "10px"},
        ),
        html.Button("Submit", id="submit-query", n_clicks=0),
        # Div to display LLM response
        html.H1("LLM Response"),
        html.Div(
            id="llm-response",
            style={
                "marginTop": "20px",
                "padding": "10px",
                "border": "1px solid #ccc",
                "borderRadius": "5px",
            },
        ),
        # Div to display list of research papers
        html.H1("Potential Papers"),
        html.Div(
            id="paper-list",
            style={
                "marginTop": "20px",
                "padding": "10px",
                "border": "1px solid #ccc",
                "borderRadius": "5px",
            },
        ),
    ]
)


# Stub: Function to get response from LLM (Gemini)
def get_llm_response(query):

    context = get_research_papers(query)

    llm_response = LLM_helpers.send_request(query, context)

    # Placeholder: Replace with actual call to LLM
    return f"{llm_response}"


# Stub: Function to get research papers as JSON
def get_research_papers(query):
    query_embedding = embed_helper.create_embedding(query)

    pg_helper.create_connection()
    similar_papers = pg_helper.find_similar_papers(query_embedding, 10)
    similar_papers.reverse()
    pg_helper.close_connection()

    return similar_papers


# Callback to handle the query submission and update outputs
@app.callback(
    [Output("llm-response", "children"), Output("paper-list", "children")],
    [Input("submit-query", "n_clicks")],
    [State("user-query", "value")],
)
def handle_query_submission(n_clicks, query):
    if not query:
        return "Please enter a query.", []

    # Get LLM response
    llm_response = get_llm_response(query)

    # Get research papers
    papers = get_research_papers(query)

    # Format the research papers as an HTML list
    paper_list_items = [
        html.Div(
            [
                html.H4(paper["title"]),
                html.P(f"Author: {paper['author']}"),
                html.P(f"Abstract: {paper['abstract']}"),
                html.A("Read More", href=paper["paper_link"], target="_blank"),
                html.P(f"Similarity: {paper['similarity']:.2f}"),
            ],
            style={
                "marginBottom": "20px",
                "padding": "10px",
                "border": "1px solid #ddd",
                "borderRadius": "5px",
            },
        )
        for paper in papers
    ]

    return llm_response, paper_list_items


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
