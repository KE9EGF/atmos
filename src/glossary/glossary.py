# Packages my beloved
import requests
import sys

glossary = requests.get("api.weather.gov/glossary")

print(glossary)

