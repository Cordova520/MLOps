import os

# Set before importing TensorFlow-dependent libraries
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import click
from datasets import load_dataset
from huggingface_hub import HfApi
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def extract_text_from_url(url: str) -> str:
    """
    Extracts readable text from a given URL.

    Args:
        url (str): The URL to extract text from.

    Returns:
        str: The extracted text, or an empty string if extraction fails.
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        # Create HTTP request
        request = urllib.request.Request(
            url,
            headers=headers
        )

        # Open URL with timeout
        with urllib.request.urlopen(request, timeout=10) as response:
            html_content = response.read()

        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove unnecessary elements
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()

        # Extract readable text
        text = soup.get_text(separator=" ", strip=True)

        return text

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")

    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")

    except TimeoutError:
        print("Request timed out.")

    except Exception as e:
        print(f"Unexpected error: {e}")

    return ""

def process_text(text: str) -> str:
    """
    Processes the input text by removing extra whitespace and normalizing it.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    # Load the model and tokenizer
    model_name = "google-t5/t5-small"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Prepare input text
    inputs = tokenizer(
        "summarize: " + text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Generate summary
    outputs = model.generate(
        **inputs,
        max_new_tokens=180,
        do_sample=False
    )

    # Decode generated tokens
    summary = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    click.echo("Summarization process completed.")
    click.echo("=" * 80)

    return summary

@click.command()
@click.option("--url", help="The URL of the webpage to summarize.")
@click.option("--file", help="The path to save the summarized text.")
def main(url: str, file: str):
    """
    Main function to extract text from a URL, summarize it, and save the summary to a file.

    Args:
        url (str): The URL of the webpage to summarize.
        file (str): The path to save the summarized text.
    """
    if url:
        click.echo(f"Extracting text from URL: {url}")
        text = extract_text_from_url(url)
        if not text:
            click.echo("No text extracted from the URL.")
            return

        click.echo("Text extraction completed.")
        click.echo("=" * 80)

        summary = process_text(text)

        click.echo("\nGenerated Summary:")
        click.echo("=" * 80)
        click.echo(summary)

    elif file:
        click.echo(f"Reading text from file: {file}")
        try:
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            click.echo(f"File not found: {file}")
            return

        summary = process_text(text)

        click.echo("\nSummary:")
        click.echo("=" * 80)
        click.echo(summary)
