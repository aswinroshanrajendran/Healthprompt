import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
from sklearn.metrics import precision_score, recall_score, f1_score
from utils import load_dataset, prepare_dataset

def evaluate(model, eval_dataloader, device):
    model.eval()
    predictions = []
    true_labels = []
    
    with torch.no_grad():
        for batch in eval_dataloader:
            input_ids, attention_mask, labels = batch
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            labels = labels.to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            batch_predictions = torch.argmax(logits, dim=1).tolist()
            
            predictions.extend(batch_predictions)
            true_labels.extend(labels.tolist())
    
    # Calculate evaluation metrics
    precision = precision_score(true_labels, predictions, average='weighted')
    recall = recall_score(true_labels, predictions, average='weighted')
    f1 = f1_score(true_labels, predictions, average='weighted')
    
    return predictions, precision, recall, f1

def main():
    # Load configuration
    with open('./config/config.json', 'r') as f:
        config = json.load(f)
    
    # Paths and hyperparameters
    eval_dataset_file = config["dataset_file"]
    model_output_dir = config["output_dir"]
    batch_size = config["evaluation"]["batch_size"]
    model_name = config["model_name"]

    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_output_dir)

    # Load dataset for evaluation
    dataset = load_dataset(eval_dataset_file)
    input_ids, attention_masks, labels = prepare_dataset(
        dataset, 
        tokenizer, 
        max_length=config["zero_shot_learning"]["max_length"], 
        padding=config["zero_shot_learning"]["padding"], 
        truncation=config["zero_shot_learning"]["truncation"], 
        return_tensors=config["zero_shot_learning"]["return_tensors"]
    )
    
    eval_dataset = TensorDataset(input_ids, attention_masks, labels)
    eval_dataloader = DataLoader(eval_dataset, batch_size=batch_size, shuffle=False)

    # Evaluate the model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    predictions, precision, recall, f1 = evaluate(model, eval_dataloader, device)

    # Print evaluation metrics
    print(f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1 Score: {f1:.4f}")
    print("Predictions:", predictions)

if __name__ == "__main__":
    main()
