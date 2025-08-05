import cohere

api_key = "4QnIpyn0ctjvwjhSdZdrkxwWBzwdWdkSWI0WwXsw"
client = cohere.Client(api_key)

# 🔍 Debug print to check what `client.chat` actually is
print("DEBUG: client.chat =", type(client.chat))  # <--- Add this line

response = client.chat.completions.create(
    model="command-nightly",
    messages=[{"role": "user", "content": "Hello from Cohere!"}],
    max_tokens=20,
    temperature=0
)

print(response.choices[0].message.content)
