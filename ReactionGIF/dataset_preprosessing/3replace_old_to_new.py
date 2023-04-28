import pandas as pd

# Read the JSON files
data1 = pd.read_json('/home/vboxuser/Voice-Assistant/ReactionGIF_new.json', lines=True)
data2 = pd.read_json('/home/vboxuser/Voice-Assistant/output2.json', lines=True)

# Convert the data into DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Replace the "text" label value with the new data
df1['text'] = df2['text']

# Write the DataFrame back to a JSON file
df1.to_json('output3.json', orient='records', lines=True, force_ascii=False)