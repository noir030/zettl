from database.models import async_session
from database.models import Project, Task
from sqlalchemy import select, update


async def get_projects():
    async with async_session() as session:
        return await session.scalars(select(Project))


async def get_tasks(project_id: int):
    async with async_session() as session:
        return await session.scalars(select(Task).where(Task.project == project_id))


async def create_project(name: str):
    async with async_session() as session:
        session.add(Project(name=name))
        await session.commit()


async def create_task(name: str, description: str, project_id: int):
    async with async_session() as session:
        task = Task(
            name=name,
            description=description,
            status="Im Laufe",
            project=project_id
        )
        session.add(task)
        await session.commit()


async def complete_task(task_id: int):
    async with async_session() as session:
        await session.execute(update(Task).where(Task.id == task_id).values(status="Erledigt"))
        await session.commit()
