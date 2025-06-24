import asyncio
from database.requests import get_projects, get_tasks, create_project, create_task
from database.models import async_main


async def main():
    print("🔧 Инициализация базы данных...")
    await async_main()

    while True:
        print("\n--- Меню ---")
        print("1. Создать проект")
        print("2. Посмотреть проекты")
        print("3. Добавить задачу к проекту")
        print("4. Посмотреть задачи проекта")
        print("5. Завершить задачу")
        print("6. Выйти")

        choice = input("Выберите опцию: ")

        if choice == "1":
            name = input("Введите название проекта: ")
            await create_project(name)

        elif choice == "2":
            projects = await get_projects()
            print("\n📋 Проекты:")
            for p in projects:
                print(f"ID: {p.id} | Название: {p.name}")

        elif choice == "3":
            projects = await get_projects()
            print("\n📋 Выберите ID проекта:")
            for p in projects:
                print(f"ID: {p.id} | Название: {p.name}")
            id = int(input("ID проекта: "))
            name = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            await create_task(name=name, description=description, project_id=id)

        elif choice == "4":
            project_id = int(input("Введите ID проекта: "))
            tasks = await get_tasks(project_id)
            print("\n📋 Задачи:")
            for t in tasks:
                print(f"ID: {t.id} | {t.name}")

        elif choice == "5":
            print("Ещё не поддерживается")

        elif choice == "6":
            print("👋 Выход.")
            break

        else:
            print("❌ Неверный выбор.")


if __name__ == "__main__":
    asyncio.run(main())
