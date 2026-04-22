import json

with open("modelConfig.json", "r") as file:
    modelConfig = json.load(file)


print(modelConfig["GFS"]["baseUrl"])