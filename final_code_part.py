import transformers
import torch
import pandas as pd
import re
import json
import os

#model loading
model_name = '/vast/work/public/ml-datasets/llama-3/Meta-Llama-3-8B-Instruct-hf'
pipeline = transformers.pipeline("text-generation", model=model_name, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto")

#1. creating prompt and referencing
def get_opt(title, author1):
    prompt = (f'Title: {title}\nPossible First Author: {author1}\nPick a country where the author is affiliated with. If the paper is not affiliated with any of the countries in the list, pick the option, 27. None\n1. USA\n2. China\n3. France\n4. Japan\n5. Canada\n6. Italy\n7. UK\n8. Germany\n9. Netherlands\n10. India\n11. Nigeria\n12. Ethiopia\n13. Qatar\n14. Emirate\n15. South Korea\n16. Finland\n17. Spain\n18. Israel\n19. Turkey\n20. Russia\n21. Sweden\n22. Australia\n23. South Africa\n24. Brazil\n25. Saudi Arabia\n26. Iran\n27. None\nOnly the choice number is needed. Do not generate any additional information. Output the choice first.')
    result = pipeline(prompt, max_new_tokens=2)
    generated_text = result[0]['generated_text']
    return generated_text.strip()

# 2. Function to process the choices and save the output as a JSON file
def process_choices(input_file, output_folder, subject, data_id):
    # Regular expression pattern to extract choices
    choice_pattern = re.compile(r"(?:Output the choice first\.\s)(\d+)")
    
    # Read the content of the generated output file
    with open(input_file, 'r') as file:
        content = file.read()

    # Find all choices
    choices = choice_pattern.findall(content)

    # Record the first result
    first_result = choices[0] if choices else None

    # Count the remaining choices
    remaining_choices = choices[1:]
    choice_counts = {str(i): 0 for i in range(1, 28)}  # Initialize counts for choices 1 to 27
    for choice in remaining_choices:
        if choice in choice_counts:
            choice_counts[choice] += 1

    # Convert choice counts to DataFrame and then to a dictionary
    df = pd.DataFrame(list(choice_counts.items()), columns=["Choice", "Count"])
    data = {
        "arxiv_belonging": first_result,
        "reference_country_count": df.to_dict(orient="records")  # Convert to a list of dictionaries
    }

    # Define the output JSON file path
    output_json = os.path.join(output_folder, f'{subject}_{data_id}.json')

    # Save the results to the JSON file
    with open(output_json, 'w') as json_file:
        json.dump(data, json_file, indent=4)

#subject fields list for looping
subject_names = ['astro-ph', 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th',
                 'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'quant-ph', 'math',
                 'cs', 'q-bio', 'q-fin', 'stat', 'eess', 'econ']

data_directory = 'paper_dataset/' #directory where title and author data is stored
output_directory = '/scratch/ab1234/scratch/final_opt/opt_country/' #reference result saving directory
json_dir = '/scratch/ab1234/scratch/final_opt/opt_json/' #country counting result(json file) saving directory
idlist_path = '/home/ab1234/home/direct_test/paper_dataset/IDlist/' #dirctory where paper idlist is stored

for subject in subject_names:
    idlist_file_path = os.path.join(idlist_path, f'{subject}.txt')
    tmp_opt_dr = os.path.join(output_directory, subject)
    opt_json_dr = os.path.join(json_dir, subject)
    
    # Check if the ID list file exists
    if os.path.exists(idlist_file_path):
        # Read the ID list file
        with open(idlist_file_path, 'r') as id_file:
            data_ids = [line.strip() for line in id_file.readlines()]
        
        # Loop through each data ID and process the corresponding file
        for data_id in data_ids:
            data_file_path = os.path.join(data_directory, subject, f'{data_id}.tsv')
            year = int(data_id[:2])
            if year < 20 or year > 23:
                continue
            
            # Check if the data file exists
            if os.path.exists(data_file_path):
                # Load the TSV file into a DataFrame
                data = pd.read_csv(data_file_path, sep='\t')
                year_folder = os.path.join(tmp_opt_dr, str(year))
                
                # Skip files with fewer than 3 rows
                if len(data) < 3:
                    continue
                year_folder = os.path.join(tmp_opt_dr, str(year))
                temp_output_file = os.path.join(year_folder, f'{data_id}.txt')
                tmp_json_dir = os.path.join(opt_json_dr,str(year))
                
                # Process each row in the DataFrame
                for index, row in data.iterrows():
                    title = row['title']
                    author1 = row['first_author']
                    if title == None:
                        continue
                    
                    # Get the model output
                    output = get_opt(title, author1)

                    # Save the output to a temporary file for processing
                    
                    with open(temp_output_file, "a") as file:
                        file.write(f'{title}\n{output}\n\n')

                    # Process the choices and save the results in the correct folder
                process_choices(temp_output_file, tmp_json_dir, subject, data_id)