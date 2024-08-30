import requests
from bs4 import BeautifulSoup
import re
import time
import random
import csv

#1. data initializing
# Headers containing API key for Semantic Scholar API requests
headers = {
    "x-api-key": "API KEY"
}

# Subject categories for different fields
physics_subs = ['astro-ph','cond-mat','gr-qc','hep-ex','hep-lat','hep-ph','hep-th','math-ph','nlin','nucl-ex','nucl-th','physics','quant-ph']
math_subs = ['math']
cs_subs = ['cs']
bio_subs = ['q-bio']
finance_subs = ['q-fin']
stats_subs = ['stat']
eess_subs = ['eess']
econ_subs = ['econ']

# Combine all non-physics categories into one list
all_subs = bio_subs + finance_subs + stats_subs + eess_subs + econ_subs

# List of all months to iterate through
month = ['01','02','03','04','05','06','07','08','09','10','11','12']

# Base URL for Semantic Scholar API
base_url = 'https://api.semanticscholar.org/graph/v1'

# Parameters for the API request
params = {
    "fields": "references.title,references.authors"
}

#2. getting arxiv paper id for semantic scholar api.
# Iterate over each subject category in the list
for k in all_subs:
    sub_list = []  # Initialize a list to store arXiv IDs
    for i in range(2020, 2024):  # Iterate over each year (modify range as needed)
        for j in month:  # Iterate over each month
            arxiv_ids = []  # Initialize a list to store arXiv IDs for the current month
            # Construct the arXiv URL for the current subject, year, and month
            url = f'https://arxiv.org/list/{k}/{i}-{j}?skip=0&show=2000'
            response = requests.get(url)  # Send a GET request to the arXiv URL
            response.raise_for_status()  # Raise an error if the request failed
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content
            links = soup.find_all('a', href=True)  # Find all links in the page

            # Regex pattern to find arXiv IDs in the format 'arXiv:xxxx.xxxxx'
            arxiv_id_pattern = re.compile(r'arXiv:(\d{4}\.\d{5})')

            # Extract arXiv IDs from the links
            for link in links:
                match = arxiv_id_pattern.search(link.get_text())
                if match:
                    arxiv_ids.append(match.group(1))

            # Select 5 random arXiv IDs, or take all if there are fewer than 5
            if len(arxiv_ids) < 5:
                five_arxiv = arxiv_ids  # Take all if fewer than 5
            else:
                five_arxiv = random.sample(arxiv_ids, 5)
            
            sub_list = sub_list + five_arxiv  # Add selected arXiv IDs to the subject list

#3. Applying semantic scholar api to get author information and reference information
            # Iterate over the selected arXiv IDs to fetch and store their data
            for arxiv_id in five_arxiv:
                # Construct the API URL to get paper details from Semantic Scholar
                base_url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=title,authors,references.title,references.authors"
                response = requests.get(base_url, headers=headers)  # Send GET request to the API
                data = response.json()  # Parse the JSON response
                time.sleep(1.1)  # Sleep to avoid hitting the rate limit

                # Extract paper title and first author
                current_title = data.get("title", "No Title")
                current_authors = data.get("authors", [])
                current_first_author = current_authors[0].get("name", "No Name") if len(current_authors) > 0 else "No Author"
                arxiv_info = [current_title, current_first_author]  # Store title and first author

                # Create a filename for storing the data in a TSV file
                filename = f"/home/ab1234/home/direct_test/paper_dataset/{k}/{arxiv_id}.tsv" #file saving directory
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter='\t')
                    # Write header
                    writer.writerow(["title", "first_author"])
                    # Write arXiv article info
                    writer.writerow(arxiv_info)

                    # Write references information
                    references = data.get("references", [])
                    for ref in references:
                        title = ref.get("title", "No Title")
                        authors = ref.get("authors", [])
                        first_author = authors[0].get("name", "No Name") if len(authors) > 0 else "No Author"
                        ref_info = [title, first_author]
                        writer.writerow(ref_info)

    # Save all selected arXiv IDs for the subject to a text file
    with open(f'IDlist/{k}_list.txt', 'w') as file: #idList saving directory
        for id in sub_list:
            file.write(f"{id}\n")