# Data-Acqusition
My code is divided into two main parts. The first part, getdata_final, directly accesses the arXiv website using requests to retrieve all article IDs. It then randomly selects 5 arXiv articles per subject per month. Using the Semantic Scholar API, it gathers the first author of each selected article along with the titles and first authors of the referenced articles. This data is stored in {subject_name}/{arxiv_id}.tsv files. Additionally, the article IDs are saved in a {subject_name}_list.txt file, making them easily accessible for other parts of the code.

The second part of the code involves using the LLaMA 3 8B model to infer the nationality of the first authors of the articles. The author and article information obtained in the first part is fed into the model, which processes the input according to the options provided in the prompt. The output of this process is a text file containing the nationality information for each article.

This output file is then reintroduced into the program in the next section of the code, where data processing is conducted. In this step, the nationality information for each arXiv article and its references is organized, counted, and stored in a JSON file. This JSON file serves as a comprehensive record of the country information associated with each article and its references, enabling further analysis.

In the final JSON file, the arxiv_belonging field represents the country to which the arXiv article belongs. The reference_country_count field contains an array where choice represents the country ID, and count represents the number of references from that particular country. This structure allows for a clear and organized presentation of both the article's country of origin and the distribution of referenced countries within each article.

Country ID representation:
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

Inference result files are stored in opt_country directory, and json files are stored in opt_json directory
