import requests
from bs4 import BeautifulSoup

def scrape_professor_names(url, num_pages):
    professor_names = []
    
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        contact_rows = soup.find_all("div", class_="contact_block_row js-contact-grid-row")
        
        # Within each contact row div, find the span with the professor's name
        for row in contact_rows:
            name_span = row.find("span", class_="contact_block_name_link_label")
            
            # Append the name if found
            if name_span:
                professor_names.append(name_span.get_text(strip=True))
    else:
        print(f"Failed to retrieve {url} with status code: {response.status_code}")

    return professor_names

def get_author_id(name):
    url = f"https://api.semanticscholar.org/graph/v1/author/search?query={name}&fields=name,authorId,paperCount,citationCount"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            authors = []
            for author in data["data"]:
                affiliations = author.get("affiliations")
                authors.append({
                    "name": author["name"],
                    "authorId": author["authorId"],
                    "paperCount": author["paperCount"],
                    "affiliations": affiliations,
                    "citationCount": author["citationCount"]
                })
            return authors
        else:
            return "No authors found with this name."

        