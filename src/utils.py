import json
import torch
from transformers import AutoTokenizer

def load_dataset(file_path):
    with open(file_path, 'r') as f:
        dataset = [json.loads(line) for line in f]
    return dataset

def prepare_dataset(dataset, tokenizer, max_length=512, padding='max_length', truncation=True, return_tensors='pt'):
    input_ids_list = []
    attention_mask_list = []
    labels_list = []

    for example in dataset:
        text = example['text']
        encoded = tokenizer.encode_plus(
            text, 
            max_length=max_length, 
            padding=padding, 
            truncation=truncation, 
            return_tensors=return_tensors
        )
        input_ids = encoded['input_ids']
        attention_mask = encoded['attention_mask']
        label = example.get('label', 0)  # Assuming the label key might not always exist, defaulting to 0 if missing

        input_ids_list.append(input_ids)
        attention_mask_list.append(attention_mask)
        labels_list.append(label)

    input_ids = torch.cat(input_ids_list, dim=0)
    attention_masks = torch.cat(attention_mask_list, dim=0)
    labels = torch.tensor(labels_list)

    return input_ids, attention_masks, labels

