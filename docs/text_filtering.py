import re
context_with_response = ['@@ПЕРВЫЙ@@ как у тебя жизнь @@ВТОРОЙ@@У меня все отлично, а у вас как?@@ПЕРВЫЙ@@']
# context_with_response = ['@@ПЕРВЫЙ@@ расскажи анекдот @@ВТОРОЙ@@Приходит мужик в публичный дом, а там ему говорят: - Извините, но у нас нет женщин. - Как нет? А как же я? - Ну, вы мужчина, у вас есть']

pattern = r'@@ВТОРОЙ@@(.*?)(?=@@ПЕРВЫЙ@@|$)'

match = re.search(pattern, context_with_response[0])
if match:
   extracted_text = match.group(1)
   print("Response Text: ", extracted_text)


import unicodedata

def remove_emojis(input_string):

    emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)

    filter_layer = emoji_pattern.sub(r'', input_string)

    return ''.join(c for c in filter_layer if unicodedata.category(c) != 'So')


text = "нормально, но я не знаю что делать дальше 🥺🤲🏻‍♀️"
text_without_emojis = remove_emojis(text)
print(text_without_emojis)  # Outputs: У нас +6, а у вас? 