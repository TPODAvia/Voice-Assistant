import requests
bot_message = "jack"
while bot_message != "Bye":
	message = input("What's your message?\n")
	print("Sending message now...")
	r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"sender": bot_message, "message": message})
	print("Bot says, ")
	for i in r.json():
		# bot_message = i['text']
		# print(r.json())
		print(f"{i}")