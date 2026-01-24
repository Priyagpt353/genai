import tiktoken

encode_text = tiktoken.encoding_for_model("gpt-5")
encode_token = [13225, 1354, 0, 5477, 11493, 6602, 24072, 13]
print(encode_text.decode(encode_token))





