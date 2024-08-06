import os
import json
import torch
import argparse
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
from utils import load_dataset, prepare_dataset

def train(model, train_dataloader, optimizer, device):
    model.train()
    total_loss = 0.0

    for batch in train_dataloader:
        input_ids, attention_masks, labels = batch
        input_ids = input_ids.to(device)
        attention_masks = attention_masks.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(input_ids=input_ids, attention_mask=attention_masks, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()

        loss.backward()
        optimizer.step()

    avg_train_loss = total_loss / len(train_dataloader)
    return avg_train_loss

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type=str, default="./config/config.json",
                        help="Path to the JSON configuration file.")
    args = parser.parse_args()

    # Load configuration from JSON file
    with open(args.config_file, 'r') as config_file:
        config = json.load(config_file)

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
    model = AutoModelForSequenceClassification.from_pretrained(config["model_name"])
    model.to(device)

    # Load dataset
    dataset = load_dataset(config["dataset_file"])

    # Prepare dataset
    input_ids, attention_masks, labels = prepare_dataset(
        dataset, 
        tokenizer, 
        max_length=config["zero_shot_learning"]["max_length"], 
        padding=config["zero_shot_learning"]["padding"], 
        truncation=config["zero_shot_learning"]["truncation"], 
        return_tensors=config["zero_shot_learning"]["return_tensors"]
    )
    
    dataset = TensorDataset(input_ids, attention_masks, labels)
    train_dataloader = DataLoader(dataset, batch_size=config["batch_size"], shuffle=True)

    # Optimizer
    optimizer = AdamW(model.parameters(), lr=config["learning_rate"])

    # Training loop
    print("Start training...")
    for epoch in range(config["epochs"]):
        train_loss = train(model, train_dataloader, optimizer, device)
        print(f"Epoch {epoch + 1}/{config['epochs']} - Average Training Loss: {train_loss}")

    # Save model
    if not os.path.exists(config["output_dir"]):
        os.makedirs(config["output_dir"])
    model.save_pretrained(config["output_dir"])
    tokenizer.save_pretrained(config["output_dir"])

    print(f"Model and tokenizer saved in {config['output_dir']}")

if __name__ == "__main__":
    main()