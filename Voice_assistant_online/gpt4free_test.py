import g4f

g4f.debug.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking
print(g4f.version) # check version
print(g4f.Provider.Ails.params)  # supported args

# streamed completion
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Привет какая сегодня московская погода"}],
    stream=True,
)

# final_message = None
# for message in response:
#     print(message, flush=True, end='')
#     final_message = message


# print(final_message)

messages = []
for message in response:
    messages.append(message)

final_message = messages[-1]
print(final_message)