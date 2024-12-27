from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'
KEY_Pinecone = 'pcsk_6wK7rt_9hcNfdA2HPVRMFwCr5EuNwmf6CLDAXJwW4JSM126j4tYJof9yUxpA5bVBQyAxDe'
Host = "https://quickstart-98d8jji.svc.aped-4627-b74a.pinecone.io"


client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)

QQZ = "MMM"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=QQZ,
)


data = response.data[0].embedding

print(data)

pc = Pinecone(
    api_key=KEY_Pinecone,
    host=Host
)


index_name = "quickstart"

index = pc.Index(index_name)  # اتصال به ایندکس

vector_id = "example-id"











