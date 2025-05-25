import json
import tqdm
data = json.load(open("m4_instruct_annotations_fixed.json", "r"))

for i in tqdm.tqdm(range(len(data))):
   conversations = data[i]["conversations"]
   if conversations[0]["from"] != "human":
       print(conversations)
       for j in range(len(conversations)):
            if j % 2 == 0:
                conversations[j]["from"] = "human"
            else:
                conversations[j]["from"] = "gpt"
        data[i]["conversations"] = conversations

with open("m4_instruct_annotations_fixed.json", "w") as f:
    json.dump(data, f, indent=4)