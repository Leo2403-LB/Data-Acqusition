# Data-Acquisition

## Overview

This project is designed to retrieve and analyze data from arXiv articles, specifically focusing on extracting the nationality of the first authors and the countries associated with referenced articles. The project is divided into two main parts:

### 1. Data Collection (`getdata_final`)

The first part of the project involves directly accessing the arXiv website using `requests` to retrieve all article IDs. The script randomly selects 5 arXiv articles per subject per month. Using the Semantic Scholar API, it gathers:

- The first author of each selected article.
- The titles and first authors of the articles referenced by these selected articles.

This data is stored in `{subject_name}/{arxiv_id}.tsv` files. Additionally, the IDs of the selected articles are saved in a `{subject_name}_list.txt` file, making them easily accessible for further processing.

### 2. Nationality Inference Using LLaMA 3 Model

The second part of the project uses the LLaMA 3 8B model to infer the nationality of the first authors of the articles. The author and article information obtained in the first part is input into the model. The model processes the input based on predefined options in the prompt, producing a text file containing the inferred nationality for each article.

This output file is then reintroduced into the program, where the data is further processed. The nationality information for each arXiv article and its references is organized, counted, and stored in a JSON file. This JSON file serves as a comprehensive record of the country information associated with each article and its references, enabling further analysis.

## JSON Structure

- **`arxiv_belonging`**: Represents the country to which the arXiv article belongs.
- **`reference_country_count`**: An array where each entry includes:
  - **`choice`**: The country ID.
  - **`count`**: The number of references from that particular country.

This structure allows for a clear and organized presentation of both the article's country of origin and the distribution of referenced countries within each article.

### Country ID Representation

1. USA  
2. China  
3. France  
4. Japan  
5. Canada  
6. Italy  
7. UK  
8. Germany  
9. Netherlands  
10. India  
11. Nigeria  
12. Ethiopia  
13. Qatar  
14. Emirate  
15. South Korea  
16. Finland  
17. Spain  
18. Israel  
19. Turkey  
20. Russia  
21. Sweden  
22. Australia  
23. South Africa  
24. Brazil  
25. Saudi Arabia  
26. Iran  
27. None of the above

## Output Directories

- **`opt_country`**: Contains the inference result files.
- **`opt_json`**: Contains the processed JSON files.

## Notes

- Some arXiv articles had their country information categorized under "None of the above." It’s unclear whether these should be excluded or included in the model training, so please take this into account for future model training.
- The new code runs efficiently; processing approximately 4,320 arXiv articles takes less than a day on an RTX 8000 GPU. This allows for rapid data acquisition in future runs.
