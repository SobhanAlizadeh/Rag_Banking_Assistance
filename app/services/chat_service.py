# # app/services/chat_service.py
# import mlflow
# from app.rag.retriever import retrieve_documents
# from app.llm.generator import generate_answer  # فرض کنید generator در llm است

# class ChatService:
#     def __init__(self):
#         mlflow.set_tracking_uri("http://mlflow:5000")
#         mlflow.set_experiment("RAG_Banking")

#     def ask(self, question: str):
#         with mlflow.start_run(run_name=f"query-{question[:20]}"):
#             mlflow.log_param("question", question)
            
#             docs = retrieve_documents(question)
#             mlflow.log_param("num_docs", len(docs))
            
#             if not docs:
#                 answer = "متأسفانه اطلاعات مرتبطی یافت نشد."
#             else:
#                 context = "\n".join(docs)
#                 answer = generate_answer(context, question)
            
#             mlflow.log_metric("answer_length", len(answer))
            
#             # ذخیره اسناد به‌عنوان artifact
#             with open("temp_docs.txt", "w") as f:
#                 f.write("\n---\n".join(docs))
#             mlflow.log_artifact("temp_docs.txt")
            
#             return answer,docs
from app.rag.pipeline import pipeline


class ChatService:

    def ask(self, session_id: str, question: str):

        return pipeline.execute(session_id, question)


chat_service = ChatService()