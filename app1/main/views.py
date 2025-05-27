from django.shortcuts import render
from product.models import Categories
from django.http import JsonResponse
from langchain_gigachat.chat_models import GigaChat
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_gigachat.embeddings.gigachat import GigaChatEmbeddings
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import re

# Подключение GigaChat
GIGACHAT_CREDENTIALS = "MDFlMTZiMjQtZDYxNS00ZTEwLThmZTctZjE2NTYyZjZiZTJlOjNiYmEwMDljLWFkYmQtNDNmZS1hNDliLWQzYzM1MjNiNjQyZA=="
llm = GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False)

# Путь к базе
CHROMA_DB_DIR = "chroma_db"

loader = TextLoader("/Users/sraperanosan/Downloads/dev_env/app1/main/test.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=500,
)
documents = text_splitter.split_documents(documents)

embeddings = GigaChatEmbeddings(
    credentials=GIGACHAT_CREDENTIALS,
    verify_ssl_certs=False
)

db = Chroma.from_documents(
    documents,
    embeddings,
    persist_directory=CHROMA_DB_DIR,
    client_settings=Settings(anonymized_telemetry=False)
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Шаблон запроса (строгое поведение)
qa_prompt = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template="""
Ты — помощник интернет-магазина строительных материалов 'ТСПК АРМАСТРОЙ'.
Отвечай только на основе приведённых ниже документов и истории общения.
Если информации в документах нет — напиши, что не можешь ответить и предложи перейти на сайт https://www.armastroy72.ru.
Если есть ссылка на товар — обязательно укажи её в ответе.
Если есть расчеты выводи форматом mathjax, polyfill.
История диалога:
{chat_history}

Документы:
{context}

Вопрос: {question}
Ответ:
""".strip()
)

from langchain.chains import ConversationalRetrievalChain

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    memory=memory,
    combine_docs_chain_kwargs={"prompt": qa_prompt}
)


def chat_answer(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if not message:
            return JsonResponse({'response': "Сообщение не получено."})
        try:
            # Получаем историю из сессии
            chat_history = request.session.get('chat_history', [])
            
            # Запрашиваем ответ
            result = qa_chain({
                "question": message,
                "chat_history": chat_history  # передаём в память вручную
            })

            # Сохраняем обновлённую историю (если используешь кастомную память)
            chat_history.append(("user", message))
            chat_history.append(("assistant", result['answer']))
            request.session['chat_history'] = chat_history

            answer = result.get('answer', 'Извините, ответ не получен.')
            answer = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', answer)
            return JsonResponse({'response': answer})
        except Exception as e:
            return JsonResponse({'response': f"Ошибка: {str(e)}"})

    return JsonResponse({'response': "Ожидался POST-запрос."})

def chat(request):
    return render(request, 'main/chat.html', {'title': 'Чат с ИИ'})


def index(request):
    categories = Categories.objects.all()
    context = {
        'title': "Главная",
        'categories': categories,
    }
    return render(request, 'main/index.html', context)


def bucket(request):
    context = {
        'title': "Корзина"
    }
    return render(request, 'main/bucket.html', context)


def contacts(request):
    context = {
        'title': "Контакты"
    }
    return render(request, 'main/contacts.html', context)

def favorite(request):
    context = {
        'title': "Избранные"
    }
    return render(request, 'main/favorite.html', context)

def reviews(request):
    context = {
        'title': "Отзывы"
    }
    return render(request, 'main/reviews.html', context)
