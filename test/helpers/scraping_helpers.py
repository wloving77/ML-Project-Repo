import requests
from bs4 import BeautifulSoup
import urllib
import time
import random
import json


class ScrapeHelpers:

    def __init__(self):
        # first link is the general all CS professors link:
        self.urls = [
            "https://engineering.virginia.edu/department/computer-science/people?keyword=&position=2&impact_area=All&research_area=All",
            "https://engineering.virginia.edu/department/computer-science/research/artificial-intelligence-research",
            "https://engineering.virginia.edu/department/computer-science/research/computer-systems-research",
            "https://engineering.virginia.edu/department/computer-science/research/cyber-physical-systems-research",
            "https://engineering.virginia.edu/department/computer-science/research/robotics",
            "https://engineering.virginia.edu/department/computer-science/research/security-research",
            "https://engineering.virginia.edu/department/computer-science/research/software-engineering",
            "https://engineering.virginia.edu/department/computer-science/research/theory",
        ]

    def fetch_professors_google_scholar_links_by_interest_area(self, url):
        """This function scrapes UVA professor names and their google scholar links if they exist, if the scholar link is not found the professor is ignored"""
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        professors_links = {}

        # Loop through each div with the specific class
        for contact_block in soup.find_all(
            "div", class_="contact_block_row js-contact-grid-row"
        ):
            # Find the span with the professor's name
            name_span = contact_block.find(
                "span", class_="contact_block_name_link_label"
            )
            name = name_span.get_text(strip=True) if name_span else None

            # Find the link to Google Scholar within the div
            scholar_link = None
            for a_tag in contact_block.find_all("a", href=True):
                href = a_tag["href"]
                if "https://scholar.google.com/citations" in href:
                    scholar_link = href
                    break

            # Only add to dictionary if both name and scholar link are found
            if name and scholar_link:
                professors_links[name] = scholar_link

        return professors_links

    def fetch_professor_names_and_google_scholar_links(self, base_url, num_pages=1):
        """This function scrapes professor names and their Google Scholar links
        across multiple pages. Only professors with a Google Scholar link are included.
        """

        professors_links = {}

        # Loop over the specified number of pages
        for page in range(0, num_pages):

            url = f"{base_url}&page={page}"

            # Make the GET request
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for person in soup.find_all("div", class_="people_list_item has_image"):
                # Find the span with the professor's name
                name_span = person.find("span", class_="contact_block_name_link_label")
                name = name_span.get_text(strip=True) if name_span else None

                # Find the Google Scholar link within the div
                scholar_link = None
                for a_tag in person.find_all("a", href=True):
                    href = a_tag["href"]
                    if "https://scholar.google.com/citations" in href:
                        scholar_link = href
                        break

                # Only add to dictionary if both name and scholar link are found
                if name and scholar_link:
                    professors_links[name] = scholar_link

        return professors_links

    def fetch_paper_titles_and_links_to_abstracts(self, prof_name, scholar_urls):
        """This function takes a professors name and their google scholar page and scrapes all of the paper titles and links to their abstracts"""

        profile_url = scholar_urls.get(prof_name)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        try:
            response = requests.get(profile_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract citations
            papers = []
            for entry in soup.find_all("a", href=True):
                href = entry["href"]
                if "/citations?view_op=view_citation" in href:
                    citation_link = urllib.parse.urljoin(
                        "https://scholar.google.com", href
                    )
                    paper_title = entry.get_text(strip=True)
                    papers.append(
                        {"title": paper_title, "abstract_link": citation_link}
                    )

            return papers
        except Exception as e:
            print(f"Error fetching papers for {prof_name}: {e}")
            return []

    def gather_all_papers_by_professor(self, prof_names_and_links):
        """This functions scrapes google scholar and returns a dictionary of professors and their papers, with the paper titles and links to their abstracts"""
        professor_info = []
        for professor in prof_names_and_links:
            prof_dictionary = {"Professor": professor, "Papers": []}
            prof_papers = self.fetch_scholar_papers(professor, prof_names_and_links)
            prof_dictionary["Papers"] = prof_papers
            professor_info.append(prof_dictionary)
            print(f"Papers Gathered for {professor}")
            # sleep a random amt of time to avoid scraping detection
            self.random_sleep()
        return professor_info

    def fetch_paper_abstract_and_link_semantic_scholar(self, title):
        """This function returns the paper abstract for a given paper title using the semantic scholar API"""
        response = requests.get(
            f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}&fields=title,abstract,url"
        )

        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                abstract = data[0].get("abstract", "Abstract not found")
                link = data[0].get("url", "Link not available")
                return abstract, link
        return "Paper not found or no abstract available", "Link not available"

    def fetch_all_paper_abstracts_by_professor(self, professor_info):
        """This function takes over an hour to run and spams the semantic scholar API to get all of the paper abstracts and links to the papers."""
        for professor_and_papers in professor_info:
            for paper in professor_and_papers["Papers"]:
                abstract, link = self.fetch_paper_abstract_and_link_semantic_scholar(
                    paper["title"]
                )
                paper["abstract"] = abstract
                paper["abstract_link"] = link
                self.random_sleep(min_delay=1, max_delay=5)
            print(f"Papers Gathered for {professor_and_papers['Professor']}")
            self.random_sleep()

    def random_sleep(self, min_delay=5, max_delay=10):
        """This function sleeps for a random amount of time between 3 and 10 seconds to avoid scraping detection by Google :O"""
        delay = random.uniform(min_delay, max_delay)
        print(f"Sleeping for {delay:.2f} seconds...")
        time.sleep(delay)

    def write_dict_to_json(self, data, filename="output.json"):
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def read_json_to_dict(self, filename="input.json"):
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        return data
