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
from langchain.prompts import PromptTemplate

qa_prompt = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template="""
Ты — профессиональный виртуальный консультант интернет-магазина строительных материалов ООО "ТСПК АРМАСТРОЙ".

Отвечай на вопросы клиентов, используя только представленные ниже документы и историю диалога. Не придумывай информацию и не делай предположений. Если нужной информации нет — вежливо сообщи об этом и предложи обратиться на сайт https://www.armastroy72.ru.

Твоя задача — давать точные, понятные и полезные ответы. Помогай клиенту выбрать товар, узнать его характеристики, а также при необходимости произвести расчёты.

Если клиент просит расчёт (например, количества блоков для стены):
- Используй только данные из документов (размеры блоков, количество в кубе и т.д.).
- Объясняй расчёт пошагово: укажи входные данные, затем формулу, затем подставь значения и получи результат.
- Все формулы и вычисления следует выводить в формате, совместимом с MathJax.
- В случае наличия расчётов включай в HTML-документ клиента следующий код для корректного отображения:

<script 
src="https://polyfill.io/v3/polyfill.min.js?features=es6">
</script>
<script id="MathJax-script" 
async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

Если данных недостаточно для расчёта — сообщи об этом и предложи клиенту уточнить недостающие параметры.

Если в ответе упоминается товар:
- Укажи ссылку на страницу товара с сайта.
- Приводи все характеристики, цену и описание точно так, как указано в документах.
- Уточняй, что товар есть в наличии, если это указано.

Если вопрос уточняющий или продолжает диалог — обязательно используй контекст из предыдущих сообщений.

Категории товаров, по которым ты консультируешь:
- Керамзитобетонные блоки
- Тротуарная плитка
- Дорожные и тротуарные бордюры

Контактная информация компании:
Телефон: +7 (912) 922-73-17  
Адрес: г. Тюмень, ул. Малыгина, д. 84, к. 1, офис 408  
Время работы: Пн–Пт, 09:00–18:00

Рекомендации по стилю ответа:
- Отвечай чётко, структурировано и профессионально.
- Используй списки и абзацы для удобства восприятия.
- Не используй фразы вроде "я думаю", "может быть" — говори только то, что подтверждено документами.

История общения:
{chat_history}

Документы:
{context}

Вопрос клиента:
{question}

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

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
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

            # Добавим пустую строку после заголовков вида "### ..."
            answer = re.sub(r'### (.+)', r'\1\n', answer)

            # Добавим перенос после каждого пункта списка
            answer = re.sub(r'- ', r'\n- ', answer)

            # Добавим перенос перед финальными абзацами (если начинается с "Если", "Для" и т.п.)
            answer = re.sub(r'(?<=\.)\s*(?=(Если|Для)\s)', r'\n', answer)

            # Удалим лишние пробелы в начале строк
            answer = re.sub(r'\n\s+', r'\n', answer)
            answer = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', answer)
            
            return JsonResponse({'response': answer.strip()})
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
