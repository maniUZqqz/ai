from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'
KEY_Pinecone = 'pcsk_6wK7rt_9hcNfdA2HPVRMFwCr5EuNwmf6CLDAXJwW4JSM126j4tYJof9yUxpA5bVBQyAxDe'
Host = "https://quickstart-98d8jji.svc.aped-4627-b74a.pinecone.io"




pc = Pinecone(
    api_key=KEY_Pinecone,
    host=Host
)


index_name = "quickstart"

index = pc.Index(index_name)  # اتصال به ایندکس


QQZdb1 = """
data = [0.1, 0.2, 0.3, 0.4, 0.5]
vector_id = "example-id"
# برای بروزرسانی ویکتور ها از upsert استفاده می کنیم
# که پارامتر اول شناسه ویکتور و پارامتر دوم دیتا
index.upsert([(vector_id, data)])
# تابع describe_index_stats برای دریافت آمار
# و اطلاعات وضعیت ایندکس استفاده می‌شود. این آمار می‌تواند شامل تعداد وکتورهای موجود،
# فضای ذخیره‌سازی مصرف‌شده، و دیگر جزئیات ایندکس باشد.
stats = index.describe_index_stats()
print(stats)
"""


QQZdb2 = """
# درست کردن یک ایندکس جدید
pc.create_index(
    name=index_name, # اسم ایندکس
    dimension=2, # ویزگی ها و ابعاد و نمودار
    metric="cosine", # معیار شباهت جستوجو در این جا سینوسی تایین شده
# ما در spec تنظیمات پیکربندی رو تعیین می کنیم
# تابع ServerlessSpec یعنی تنظیمات روی سرورلس قرار بگیرد
    spec= ServerlessSpec(
# یعنی روی aws قرار بگیرد ( aws آمازونه )
        cloud="aws",
# منطقه ی که باید باشه
        region="us-east-1"
    )
)
"""


QQZdb3 = """
response = index.query(
    namespace="ns1",
    vector=[0.1, 0.3],
    top_k=2,
    include_values=True,
    include_metadata=True,
    filter={"genre": {"$eq": "action"}}
)
"""


QQZdb4 = """
index.upsert(
    vectors=[
        {
            "id": "vec1",
            "values": [1.0, 1.5],
            "metadata": {"genre": "drama"}
        },
        {
            "id": "vec2",
            "values": [2.0, 1.0],
            "metadata": {"genre": "action"}
        },
        {
            "id": "vec3",
            "values": [0.1, 0.3],
            "metadata": {"genre": "drama"}
        },
        {
            "id": "vec4",
            "values": [1.0, -2.5],
            "metadata": {"genre": "action"}
        }
    ],
    namespace="ns1"
)
"""