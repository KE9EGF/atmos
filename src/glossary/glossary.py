# Packages my beloved
from prompt_toolkit import print_formatted_text as fprint
from prompt_toolkit.formatted_text import HTML

import requests
import sys
import json
import os

# Variables
url = "https://api.weather.gov/glossary"
headers = {
    "User-Agent": "(AtmosProject, severett078@gmail.com)"
}


r = requests.get(url, headers=headers)

if r.status_code == 200:
    data = r.json()

    glossary = data.get('glossary', [])
    for item in glossary:
        item['definition'].replace("<br>", "")
with open("output.txt", "w") as f:
    print(glossary, file=f)

def get_definition(term):
    try:
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            data = r.json

            glossary = data.get('glossary', [])
    except Exception as e:
        print(f'An error occurred: {e}')
    
