# from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
#
# # ایجاد ایندکس از داده‌ها (فقط یک بار اجرا شود)
# def build_index(data_folder='data/'):
#     documents = SimpleDirectoryReader(data_folder).load_data()
#     index = GPTVectorStoreIndex.from_documents(documents)
#     index.storage_context.persist('index_storage')
#     return index
#
# # بارگذاری ایندکس
# def load_index():
#     storage_context = StorageContext.from_defaults(persist_dir='index_storage')
#     return load_index_from_storage(storage_context)
#
# # پرسش از مدل RAG
# def ask_question_rag(question):
#     index = load_index()
#     response = index.query(question)
#     return response.response
