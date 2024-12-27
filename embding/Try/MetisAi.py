from openai import OpenAI

API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)

QQZ = "MMM"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=QQZ,
)


print(response.data[0].embedding)




