import sys
from src.rag.rag_chain import RAGChain

def main():
    print('GigaChat document agent запущен!')
    print('Загрузка базы знаний и модели ... Подождите немного.')

    try:
        rag = RAGChain()
        print("Агент готов к работе.")
        print("Введите вопрос или 'выход' для заврешения. \n")

        while True:
            query = input("👤 Вы: ").strip()
            if query.lower() in ['выход', 'exit', 'quit', 'stop']:
                print("До свидания!")
                break
            if not query:
                continue
            print("Ищй ответ в документах")
            try:
                response = rag.ask(query)
                print(f"\n🤖 GigaChat: {response}\n")
                print("-" * 50)
            except Exception as e:
                print(f"Произошла ошибка при обработке запроса: {e}")

    except Exception as e:
        print(f"Ошибка при инициализации: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
