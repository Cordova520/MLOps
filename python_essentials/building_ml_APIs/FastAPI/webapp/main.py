from transformers import pipeline
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

generator = pipeline("text-generation", model="gpt2", framework="pt")

# Initialize FastAPI
app = FastAPI(
    title="GPT-2 Text Generation API",
    description="An API to generate text using Hugging Face Transformers",
    version="1.0.0"
)

class Body(BaseModel):
    prompt: str
    max_length: int = 50

@app.get('/', response_class=HTMLResponse)
def root():
    return """
    <h1>GPT-2 Text Generation API</h1>
    <p>A self-documenting API to interact with GPT-2.</p>
    <p>Visit <a href="/docs">/docs</a> for API documentation.</p>
    """

@app.post('/generate')
def predict(body:Body):
    results = generator(
        body.prompt,
        max_new_tokens=body.max_length,
        num_return_sequences=1,
        pad_token_id=generator.tokenizer.eos_token_id
    )
    return results[0]