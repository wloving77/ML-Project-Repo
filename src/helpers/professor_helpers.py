import requests
from bs4 import BeautifulSoup
import time


class ProfessorHelpers:

    def __init__(self):
        self.urls = [
            "https://engineering.virginia.edu/department/computer-science/research/artificial-intelligence-research",
            "https://engineering.virginia.edu/department/computer-science/research/computer-systems-research",
            "https://engineering.virginia.edu/department/computer-science/research/cyber-physical-systems-research",
            "https://engineering.virginia.edu/department/computer-science/research/robotics",
            "https://engineering.virginia.edu/department/computer-science/research/security-research",
            "https://engineering.virginia.edu/department/computer-science/research/software-engineering",
            "https://engineering.virginia.edu/department/computer-science/research/theory",
        ]

    def scrape_professor_names(self, url):
        professor_names = []

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            contact_rows = soup.find_all(
                "div", class_="contact_block_row js-contact-grid-row"
            )

            for row in contact_rows:
                name_span = row.find("span", class_="contact_block_name_link_label")

                if name_span:
                    professor_names.append(name_span.get_text(strip=True))
        else:
            print(f"Failed to retrieve {url} with status code: {response.status_code}")

        return professor_names

    def get_potential_ids(self, name):
        url = f"https://api.semanticscholar.org/graph/v1/author/search?query={name}&fields=name,authorId,paperCount,citationCount"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                authors = []
                for author in data["data"]:
                    authors.append(
                        {
                            "name": author["name"],
                            "authorId": author["authorId"],
                            "paperCount": author["paperCount"],
                            "citationCount": author["citationCount"],
                        }
                    )
                return authors
            else:
                return "No authors found with this name."

    def filter_ids(self, professors):
        possible_professors = []

        # gets possible matches from semantic scholar
        for professor in professors:
            possible_professors.append(self.get_potential_ids(professor))
            time.sleep(1)

        # filters for exact name matches
        for i in range(len(professors)):
            possible_professors[i] = [
                professor
                for professor in possible_professors[i]
                if professor.get("name") == professors[i]
            ]

        return possible_professors

    def get_author_papers_with_abstracts(self, author_id):
        url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
        params = {"fields": "title,abstract,year"}  # Specify the fields you need
        response = requests.get(url, params=params)
        data = response.json()

        # Check if papers were returned
        if "data" not in data:
            return []

        # Extract abstracts
        papers_with_abstracts = []
        for paper in data["data"]:
            if "abstract" in paper and paper["abstract"]:
                papers_with_abstracts.append(
                    {
                        "title": paper["title"],
                        "abstract": paper["abstract"],
                        "year": paper["year"],
                    }
                )

        return papers_with_abstracts
