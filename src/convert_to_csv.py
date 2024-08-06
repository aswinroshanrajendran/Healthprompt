import os
import pandas as pd

def generate_clinical_description(text):
    # Customize this function to generate clinical descriptions based on text content
    return f"Text excerpt related to clinical context: {text[:50]}..."

def prepare_data(data_dir):
    # Initialize an empty list to store data for CSV
    data = []

    # Iterate through each txt file
    for txt_file in os.listdir(data_dir):
        if txt_file.endswith('.txt'):
            txt_path = os.path.join(data_dir, txt_file)
            
            # Read text content from txt file
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            # Generate clinical description
            clinical_description = generate_clinical_description(text)
            
            # Example: creating a prompt (customize this part as needed)
            prompt = f"###Human:\nextract clinical information from this text..."
            
            # Append to data list
            data.append({
                'concept': 'Clinical Text',
                'clinical description': clinical_description,
                'prompt': prompt,
                'text': text
            })
    
    return data

def convert_to_csv(data, output_file):
    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['concept', 'clinical description', 'prompt', 'text'])
    
    # Save DataFrame to CSV with tab separation
    df.to_csv(output_file, sep='\t', index=False)

    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    # Path to the directory containing txt files
    data_dir = './data/raw/training_dataset'
    
    # Prepare data
    data = prepare_data(data_dir)

    # Specify output CSV file path
    output_file = './output.csv'
    
    # Convert data to CSV
    convert_to_csv(data, output_file)
