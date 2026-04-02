from langchain_gigachat import GigaChat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.vector_store.retriever import DocumentRetriever
import os


class RAGChain:
    def __init__(self):
        self.retriever_module = DocumentRetriever()
        self.retriever = self.retriever_module.vector_store.as_retriever(search_kwargs={"k": 5})
        self.llm = GigaChat(
            credentials=os.getenv("GIGACHAT_CREDENTIALS"),
            scope=os.getenv("SCOPE"),
            model=os.getenv("MODEL"),
            verify_ssl_certs=False,
            temperature=0.2
        )

        template = """Ты — эксперт по программированию. 
        Твоя задача: ответить на вопрос пользователя, опираясь на предоставленный КОНТЕКТСТ.

        Если в контексте есть программный код или примеры эквивалентности, объясни их логику.
        Если информации совсем нет, скажи: "В моих документах этого нет, но вообще..." и дай краткий ответ из своих знаний (уточнив, что это твои знания).

        КОНТЕКСТ:
        {context}

        ВОПРОС: {question}

        ОТВЕТ:"""

        self.prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.rag_chain = (
            {"context" : self.retriever | format_docs, "question" : RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str):
        return self.rag_chain.invoke(question)

# Usage
if __name__ == "__main__":
    chain = RAGChain()
    q = "How i can use decorators in my code?"
    print(f"\n Question: {q}")
    print(f"Answer GigaChat:\n{chain.ask(q)}")