# import os
# import json
# import pandas as pd
# from preprocess import read_text_file, read_ann_file

# def convert_to_jsonl(pairs_file, data_dir, output_file):
#     pairs = pd.read_csv(pairs_file, header=None)
#     data = []

#     for _, row in pairs.iterrows():
#         text_file = row[0]
#         ann_file = row[1]

#         text = read_text_file(os.path.join(data_dir, text_file))
#         annotations = read_ann_file(os.path.join(data_dir, ann_file))

#         record = {
#             'text': text,
#             'annotations': annotations
#         }
#         data.append(record)

#     with open(output_file, 'w') as f:
#         for record in data:
#             json.dump(record, f)
#             f.write('\n')

# if __name__ == "__main__":
#     pairs_file = "./data/raw/text_ann_pairs.csv"
#     data_dir = "./data/raw/training_dataset"
#     output_file = "./data/processed/dataset.jsonl"
    
#     convert_to_jsonl(pairs_file, data_dir, output_file)
import os
import json
import pandas as pd

# Function to read text file
def read_text_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

# Function to read annotations file
def read_ann_file(filepath):
    annotations = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if parts[0].startswith('T'):
                entity_info = parts[1].split()
                entity_id = parts[0]
                entity_type = entity_info[0]
                ranges = entity_info[1:]  # List of start-end pairs or single range
                for rng in ranges:
                    range_parts = rng.split()
                    if len(range_parts) == 2:  # Handle start-end pairs
                        start = range_parts[0]
                        end = range_parts[1]
                        try:
                            entity = {
                                'id': entity_id,
                                'type': entity_type,
                                'start': int(start),
                                'end': int(end),
                                'text': parts[2]
                            }
                            annotations.append(entity)
                        except ValueError:
                            print(f"Skipping invalid annotation: {line}")
                    else:  # Handle single range or invalid format
                        print(f"Skipping invalid annotation: {line}")
            elif parts[0].startswith('R'):
                relation = {
                    'id': parts[0],
                    'type': parts[1].split()[0],
                    'arg1': parts[1].split()[1].split(':')[1],
                    'arg2': parts[1].split()[2].split(':')[1]
                }
                annotations.append(relation)
    return annotations

# Function to convert pairs to JSONL format
def convert_to_jsonl(pairs_file, data_dir, output_file):
    pairs = pd.read_csv(pairs_file, header=None)
    data = []

    for _, row in pairs.iterrows():
        text_file = row[0]
        ann_file = row[1]

        text = read_text_file(os.path.join(data_dir, text_file))
        annotations = read_ann_file(os.path.join(data_dir, ann_file))

        record = {
            'text': text,
            'annotations': annotations
        }
        data.append(record)

    with open(output_file, 'w') as f:
        for record in data:
            json.dump(record, f)
            f.write('\n')

if __name__ == "__main__":
    pairs_file = "./data/raw/text_ann_pairs.csv"
    data_dir = "./data/raw/training_dataset"
    output_file = "./data/processed/dataset.jsonl"
    
    convert_to_jsonl(pairs_file, data_dir, output_file)

