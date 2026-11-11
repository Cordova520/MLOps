#first make sure you have Hugging Face Datasets installed. You can use python -m pip install -U datasets to install it. Then you can use the following code to load a dataset and list available datasets.
from datasets import load_dataset
from huggingface_hub import HfApi

api = HfApi()
# List available datasets
datasets = list(api.list_datasets(limit=10))  # Limit to 10 datasets for display
print(f"Found {len(datasets)} datasets on Hugging Face Hub.")
for dataset in datasets[:10]:  # Display first 10 datasets
    print(f"- {dataset.id}")

#Loading example dataset
#Make sure you have the dependencie Pillow installed. You can use python -m pip install -U Pillow to install it. Then you can use the following code to load a dataset and display its contents.
dataset_name = "nvidia/simready-assets"  # Example dataset
dataset = load_dataset(dataset_name)
print(f"\nLoaded dataset: {dataset_name}")
print(f"Dataset splits: {dataset.keys()}")
df = dataset["test"].to_pandas() #Hugging Face Dataset to pandas DataFrame 
print(df.head(10))

print(df.describe())
