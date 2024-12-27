# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.llms import OpenAI
# from langchain.chains import RetrievalQA
#
#
# # بارگذاری ایندکس با مجوز deserialization خطرناک
# vectorstore = FAISS.load_local("faiss_index", allow_dangerous_deserialization=True)
#
#
# # بارگذاری اسناد و ایندکس‌سازی
# def build_index(data_folder='data/'):
#     documents = []
#     loader = PyPDFLoader(data_folder)
#     documents.extend(loader.load())
#
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     split_docs = text_splitter.split_documents(documents)
#
#     embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = FAISS.from_documents(split_docs, embedding)
#     vectorstore.save_local("faiss_index")
#     return vectorstore
#
# # بارگذاری ایندکس ذخیره شده
# def load_index():
#     embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = FAISS.load_local("faiss_index", embedding)
#     return vectorstore
#
# # پرسش از مدل RAG
# def ask_question_rag(question):
#     vectorstore = load_index()
#     retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#
#     llm = OpenAI(model="gpt-3.5-turbo")  # یا مدل Hugging Face
#     qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
#     answer = qa_chain.run(question)
#     return answer
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # from langchain.llms import OpenAI
# # from langchain.document_loaders import PyPDFLoader
#
#
# # # ایندکس کردن داده‌ها از فایل‌های PDF
# # def build_index(data_folder='data/'):
# #     # بارگذاری اسناد از پوشه
# #     documents = []
# #     loader = PyPDFLoader(data_folder)
# #     documents.extend(loader.load())
# #
# #     # تقسیم‌بندی اسناد به بخش‌های کوچک
# #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# #     split_docs = text_splitter.split_documents(documents)
# #
# #     # ایجاد مدل Embedding
# #     embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# #
# #     # ایجاد ایندکس با FAISS
# #     vectorstore = FAISS.from_documents(split_docs, embedding)
# #     vectorstore.save_local("faiss_index")
# #     return vectorstore
# #
# # # بارگذاری ایندکس ذخیره شده
# # def load_index():
# #     embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# #     vectorstore = FAISS.load_local("faiss_index", embedding)
# #     return vectorstore
# #
# # # تابع برای پرسش از RAG
# # def ask_question_rag(question):
# #     vectorstore = load_index()
# #     retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
# #
# #     # استفاده از یک مدل زبانی برای پاسخ‌دهی
# #     llm = OpenAI(model="gpt-3.5-turbo")  # یا مدل Hugging Face
# #     qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
# #     answer = qa_chain.run(question)
# #     return answer