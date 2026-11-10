from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

#Load the model and tokenizer
model_name = "google-t5/t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

#Define the input for different tasks
#Summarize
# text = "sumarize: Machine Learning in production environments is largely seen as the ultimate goal." \
# "Sometimes deploying models can be difficult when automation is not part of the workflow." \
# "Creating a foundational process that is reliable and automated is complex and requires commitment from the team and the organization as a whole."

#Sentiment
# text = "sst2 sentence: Automation takes hard work but allows you to have a solid deployment"

#Questions
#text = "question: Is deploying models in production hard?, context: Deploying models in production environments is largely seen as the ultimate goal. Sometimes deploying models can be difficult when automation is not part of the workflow. Creating a foundational process that is reliable and automated is complex and requires commitment from the team and the organization as a whole."

#Translation
text = "translate English to French: Machine Learning in production environments is largely seen as the ultimate goal. Sometimes deploying models can be difficult when automation is not part of the workflow. Creating a foundational process that is reliable and automated is complex and requires commitment from the team and the organization as a whole."

#Convert text into tokens
inputs = tokenizer(text, return_tensors="pt")

#Generate Output
outputs = model.generate(**inputs, max_length=40, num_beams=4, early_stopping=True)

#Convert tokens back into text
result = tokenizer.batch_decode(outputs[0], skip_special_tokens=True)

print(result)

#Text Generation Pipeline
gpt2_generator = pipeline("text-generation", model="openai-community/gpt2")
prompt = "Some phrase about Machine learning in production environments"
results = gpt2_generator(prompt, max_new_tokens=50, num_return_sequences=2, do_sample=True, truncation=True, pad_token_id=tokenizer.eos_token_id)

for idx, result in enumerate(results, start=1):
    print(f"Result {idx}: {result}")