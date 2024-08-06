import os
import csv

def read_text_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

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

def pair_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    
    pairs = []
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    for file in files:
        text_file = file
        ann_file = file.replace('.txt', '.ann')
        if os.path.exists(os.path.join(directory, ann_file)):
            pairs.append((text_file, ann_file))
    return pairs

def main():
    # Use the absolute path to your training_dataset directory
    data_dir = "./data/raw/training_dataset"

    try:
        pairs = pair_files(data_dir)

        with open("./data/raw/text_ann_pairs.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            for text_file, ann_file in pairs:
                writer.writerow([text_file, ann_file])
        print("Pairs file created successfully.")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()

