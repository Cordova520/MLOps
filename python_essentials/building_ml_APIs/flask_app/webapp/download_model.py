from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="onnxmodelzoo/roberta-sequence-classification-9",
    filename="roberta-sequence-classification-9.onnx",
    local_dir="webapp"
)

print(f"Model downloaded to: {model_path}")