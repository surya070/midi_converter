from google import genai
import os

client = genai.Client()
print(client)
models = client.models.list()
for m in models:
    print(m.name)
