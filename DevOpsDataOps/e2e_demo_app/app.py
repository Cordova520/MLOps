from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gradio as gr
import spaces
import torch

MODEL_NAME = "google/flan-t5-small"

#Automatically select GPU if available, otherwise CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
).to(device)

model.eval()

@spaces.GPU(duration=60)
def predict(prompt):

    if not prompt.strip():
        return "Please enter some text to summarize."

    # Tokenize the input
    inputs = tokenizer(
        "Summarize the following text: " + prompt,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    # Explicitly convert inputs into tensors
    input_ids = torch.as_tensor(
        inputs["input_ids"],
        dtype=torch.long,
        device=device
    )

    attention_mask = torch.as_tensor(
        inputs["attention_mask"],
        dtype=torch.long,
        device=device
    )

    # Generate summary
    with torch.inference_mode():
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=150,
            num_beams=4,
            do_sample=False
        )

    # Decode the generated summary
    summary = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return summary


demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(
        placeholder="Enter text to summarize...",
        lines=6,
        label="Input Text"
    ),
    outputs=gr.Textbox(label="Summary"),
    title="AI Text Summarizer",
    description="Summarize text using Hugging Face Transformers"
)


if __name__ == "__main__":
    demo.launch()