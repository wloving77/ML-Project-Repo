import requests
from bs4 import BeautifulSoup

def scrape_professors(major, num_pages):
    # Base URL
    base_url = f"https://engineering.virginia.edu/department/{major}/faculty?page="
    
    # List to store faculty names
    faculty_names = []
    
    # Loop through pages
    for page in range(num_pages):
        url = f"{base_url}{page}"
        response = requests.get(url)
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all 'people_list_item' divs
        people_items = soup.find_all('div', class_='people_list_item')
        
        # Extract the name from each item
        for item in people_items:
            name_span = item.find('span', class_='contact_block_name_link_label')
            if name_span:
                faculty_names.append(name_span.text.strip())
    
    return faculty_names

    import requests

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

        