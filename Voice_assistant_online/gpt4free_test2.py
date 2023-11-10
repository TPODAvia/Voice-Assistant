import g4f

def ask_gpt(messages: list) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=messages
    )
    print(response)
    return response

messages = []

# Open the comment if comment is needed
# content = "You are an assistant who controls the operation of devices. There are several devices, such as lamp, fan, curtains, heater. Output the results in English in the format [device - action]."
# messages.append({"role": "system", "content": content})
try:
    while True:
        question = input()
        messages.append({'role': "user", "content": question})
        answer = ask_gpt(messages=messages)
        messages.append({'role': "assistant", "content": answer})
except KeyboardInterrupt:
   print("Exiting the program")