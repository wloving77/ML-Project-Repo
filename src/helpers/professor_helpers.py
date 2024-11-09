import requests
from bs4 import BeautifulSoup
import urllib
import time
import random
import json


class ProfessorHelpers:

    def __init__(self):
        # firt link is the general all CS professors link:
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

    def fetch_all_professors_google_scholar_links(self, base_url, num_pages=1):
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

    def fetch_scholar_papers(self, prof_name, scholar_urls):
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

    def fetch_paper_details(self, citation_url):
        """This function takes as input a citation url and returns a dictionary with the paper abstract and a link to the host site of the paper"""

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        response = requests.get(citation_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        paper_details = {"abstract": None, "paper_link": None}

        description_div = soup.find("div", class_="gsc_oci_field", string="Description")

        # Find the abstract text in the next sibling div
        if description_div:
            abstract_div = description_div.find_next_sibling(
                "div", class_="gsc_oci_value"
            )
            paper_details["abstract"] = (
                abstract_div.get_text(strip=True)
                if abstract_div
                else "Abstract not found."
            )
        else:
            print("Description field not found on page.")

        # Find the link to the paper
        title_link = soup.find("a", class_="gsc_oci_title_link")
        if title_link and title_link["href"]:
            paper_details["paper_link"] = title_link["href"]
        else:
            print("Paper link not found.")

        return paper_details["abstract"], paper_details["paper_link"]

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

    def gather_all_paper_abstracts_and_links(self, professors_and_papers):
        return None

    def random_sleep(self, min_delay=5, max_delay=10):
        """This function sleeps for a random amount of time between 3 and 10 seconds to avoid scraping detection by Google :O"""
        delay = random.uniform(min_delay, max_delay)
        print(f"Sleeping for {delay:.2f} seconds...")
        time.sleep(delay)

    def write_dict_to_json(self, data, filename="output.json"):
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
