from lamini import Lamini

# Directly set the API key
# api_key = 'your api key here'

# Initialize the Lamini object with the API key
llm = Lamini(api_key=api_key, model_name="mistralai/Mistral-7B-Instruct-v0.1")

prompts = [
    "Symptoms: I've been experiencing a persistent cough, a high fever, body aches, and fatigue.",
    "Duration: These symptoms have been ongoing for the past three days.",
    "Severity: The fever seems to be getting worse, and the fatigue is making it difficult to perform daily activities.",
    "Medications: I have been taking over-the-counter pain relievers, but they don't seem to be helping much.",
    "Additional Concerns: I'm also feeling quite dizzy and have lost my appetite."
    """what does an example jsonl file look like that is loaded with this function? def load_examples(self):
        filename = self.saved_examples_path
        if not os.path.exists(filename):
            return {}

        # load the examples from the jsonl file using the jsonlines library
        with jsonlines.open(filename) as reader:
            examples = {}
            for row in reader:
                class_name = row["class_name"]
                example = row["examples"]
                self.add_class(class_name)
                examples[class_name] = example

        return examples""",
]

for prompt in prompts:
    try:
        print(f"=============Prompt: {prompt}=============")
        print(llm.generate(prompt))
        print(f"=============Prompt: <s>[INST] {prompt} [/INST]=============")
        print(llm.generate(f"<s>[INST] {prompt} [/INST]"))
    except Exception as e:
        print(f"An error occurred for prompt '{prompt}': {e}")

# Compare with Llama 2
llm_compare = Lamini(api_key=api_key, model_name="meta-llama/Llama-2-7b-chat-hf")

prompts = [
    {
        "system": "You are not feeling good.",
        "user": "I'm feeling sick",
    },
]

for prompt in prompts:
    concat_prompt = f"{prompt['system']} {prompt['user']}"
    hydrated_prompt = f"<s>[INST] <<SYS>>\n{prompt['system']}\n<</SYS>>\n{prompt['user']} [/INST]"
    try:
        print(f"=============Prompt: {concat_prompt}=============")
        print(llm_compare.generate(concat_prompt))
        print(f"=============Prompt: {hydrated_prompt}=============")
        print(llm_compare.generate(hydrated_prompt))
    except Exception as e:
        print(f"An error occurred for prompt '{prompt}': {e}")
