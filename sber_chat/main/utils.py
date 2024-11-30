# from transformers import AutoModelForCausalLM, AutoTokenizer

# model_name = "ai-forever/rugpt3large_based_on_gpt2"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# def generate_response(user_query):
#     inputs = tokenizer.encode(user_query, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)
