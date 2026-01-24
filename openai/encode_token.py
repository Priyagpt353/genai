import tiktoken

encode_text = tiktoken.encoding_for_model("gpt-5")
text = "Hello there! I'm testing token encoding."
token = encode_text.encode(text)
print(token)



