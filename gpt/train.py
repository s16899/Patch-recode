# import tiktoken

# encoding = tiktoken.get_encoding("cl100k_base")

# prompt = str(input("Prompt : "))

# encode = encoding.encode(prompt)

# print("encoded message : ", encode)

# decode_to_bytes = encoding.decode_tokens_bytes(encode)

# print("Decoded message : ", decode_to_bytes)

# import tiktoken

# encoding = tiktoken.get_encoding("cl100k_base")

# count = 0
# token_list = []

# user_input = str(input("Prompt : "))

# encode = encoding.encode(user_input)
# decode = encoding.decode_tokens_bytes(encode)

# for token in decode:
#     token_list.append(token.decode())

# character_count = sum(len(i) for i in token_list)
# length = len(encode)

# for tk in token_list:
#     if count == 0:
#         print('\x1b[0;47;1m' + tk + '\x1b[0m', end='')
#         count += 1
#     elif count == 1:
#         print('\x1b[0;42;1m' + tk + '\x1b[0m', end='')
#         count += 1
#     elif count == 2:
#         print('\x1b[0;43;1m' + tk + '\x1b[0m', end='')
#         count += 1
#     elif count == 3:
#         print('\x1b[0;44;1m' + tk + '\x1b[0m', end='')
#         count += 1
#     elif count == 4:
#         print('\x1b[0;46;1m' + tk + '\x1b[0m', end='')
#     elif count == 5:
#         print('\x1b[0;45;1m' + tk + '\x1b[0m', end='')
#         count = 0

# print("\n\n" + str(token_list) + "\n")
# print(str(encode) + "\n")
# print("Token count: " + str(length))
# print("Character count: " + str(character_count))

import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")
color_codes = ['0;47', '0;42', '0;43', '0;44', '0;46', '0;45']

user_input = str(input("Prompt : "))

encoded = encoding.encode(user_input)
decoded = encoding.decode_tokens_bytes(encoded)
token_list = [token.decode() for token in decoded]

character_count = sum(len(i) for i in token_list)

for idx, token in enumerate(token_list):
    print(f"\x1b[{color_codes[idx % len(color_codes)]};1m{token}\x1b[0m", end="")

print("\n\n" + str(token_list) + "\n")
print(str(encoded) + "\n")
print("Token count: " + str(len(encoded)))
print("Character count: " + str(character_count))