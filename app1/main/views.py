from django.shortcuts import render
from product.models import Categories
# views.py
from django.http import JsonResponse
from langchain_gigachat.chat_models import GigaChat
from langchain.schema import HumanMessage
from langchain.document_loaders import TextLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from chromadb.config import Settings
from langchain_gigachat.embeddings.gigachat import GigaChatEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
# Подключение GigaChat
GIGACHAT_CREDENTIALS = "MDFlMTZiMjQtZDYxNS00ZTEwLThmZTctZjE2NTYyZjZiZTJlOjNiYmEwMDljLWFkYmQtNDNmZS1hNDliLWQzYzM1MjNiNjQyZA=="
llm = GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False)

loader = TextLoader("/Users/sraperanosan/Downloads/dev_env/app1/main/test.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
documents = text_splitter.split_documents(documents)
embeddings = GigaChatEmbeddings(
    credentials="MDFlMTZiMjQtZDYxNS00ZTEwLThmZTctZjE2NTYyZjZiZTJlOjNiYmEwMDljLWFkYmQtNDNmZS1hNDliLWQzYzM1MjNiNjQyZA==", verify_ssl_certs=False
)
db = Chroma.from_documents(
    documents,
    embeddings,
    client_settings=Settings(anonymized_telemetry=False),
)

def chat_answer(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if not message:
            return JsonResponse({'response': "Сообщение не получено."})

        # Получаем историю из сессии или инициализируем
        chat_history = request.session.get('chat_history', [])
        chat_history.append({"role": "user", "content": message})

        try:
            # Собираем последние сообщения как контекст
            context = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history[-6:]])  # последние 3 пары

            # Формируем итоговый запрос к модели
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
            result = qa_chain({"query": context})
            answer = result.get('result', 'Извините, ответ не получен.')

            # Добавляем ответ в историю
            chat_history.append({"role": "assistant", "content": answer})
            request.session['chat_history'] = chat_history  # сохраняем обратно

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
