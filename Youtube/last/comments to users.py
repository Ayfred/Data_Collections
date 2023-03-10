import pandas as pd
from os.path import abspath, dirname
import json

df = pd.read_excel(r"C:\\Users\steve\Documents\\Cours\\FIG172\\2IA\\Collecte et stockage données\\projet\\youtube-chatGPT-comments.xlsx")

comments = []
users = dict()

for index, rows in df.iterrows():
    comments.append(rows.to_dict())

for comment in comments:
    usr = comment['authorChannelId']
    if usr not in users:
        users[usr] = []
    users[usr].append(comment)
    del users[usr][-1]['authorChannelId']
    if str(users[usr][-1]['parentId']).lower() == 'nan':
        users[usr][-1]['parentId'] = None

users2 = dict()
for userId in users.keys():
    users2[userId] = json.dumps(users[userId], indent=0, ensure_ascii=False)

pretty_json_2 = json.dumps(users, indent=4, ensure_ascii=False) 
with open(f"{dirname(abspath(__file__))}\youtube-chatGPT-users.json", 'w', encoding='utf-8') as outfile:
    outfile.write(pretty_json_2)

df2 = pd.DataFrame(users2.items(), columns=('authorChannelId', 'comments'))
output_file_path_2 = f"{dirname(abspath(__file__))}\youtube-chatGPT-users.xlsx"
df2.to_excel(output_file_path_2, index=False)

