import asyncio
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from database.models import async_main
from database.requests import get_projects, get_tasks, create_project, create_task, complete_task, delete_project


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Zettl - App für Aufgabenverwaltung")
        self.root.state("zoomed")

        style = ttk.Style()
        style.configure("TFrame", foreground="white", background="#293133")

        self.projects = []
        self.tasks_widgets = []

        self.project_frame = ttk.Frame(root, style="TFrame", padding=10)
        self.project_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.project_label = ttk.Label(self.project_frame, text="Projekte")
        self.project_label.pack(side=tk.TOP, pady=(0, 10))

        self.project_listbox = tk.Listbox(self.project_frame, width=40, selectbackground="#ec4e39")
        self.project_listbox.pack(fill=tk.BOTH, expand=True)
        self.project_listbox.bind("<<ListboxSelect>>", self.on_project_select)

        self.task_frame = ttk.Frame(root, style="TFrame", padding=10)
        self.task_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tasks_label = ttk.Label(self.task_frame, text="Aufgaben")
        self.tasks_label.pack(side=tk.TOP, pady=(0, 10))

        self.add_project_button = ttk.Button(self.project_frame, text="Projekt erstellen", command=self.add_project_dialog)
        self.add_project_button.pack(side=tk.BOTTOM, anchor=tk.CENTER, padx=20, pady=20)

        self.add_task_button = ttk.Button(self.task_frame, text="Task hinzufügen")
        self.delete_project_button = ttk.Button(self.task_frame, text="Projekt löschen")
    
    async def initialize(self):
        await async_main()
        await self.load_projects()

    async def load_projects(self):
        projects = await get_projects()

        self.projects = list(projects)
        self.project_listbox.delete(0, tk.END)

        for index, project in enumerate(self.projects):
            self.project_listbox.insert(tk.END, f"{index + 1}: {project.name}")
    
    def on_project_select(self, event):
        selection = self.project_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        project = self.projects[index]
        asyncio.create_task(self.load_tasks(project.id))
    
    def add_project_dialog(self):
        name = simpledialog.askstring("Neues Projekt", "Name vom neuen Projekt:")
        if name:
            asyncio.create_task(self.create_project_and_reload(name))
    
    async def create_project_and_reload(self, name):
        await create_project(name)
        await self.load_projects()

    async def load_tasks(self, project_id):
        for widget in self.tasks_widgets:
            widget.destroy()

        self.tasks_widgets = []

        self.add_task_button.config(command=lambda: self.add_task_dialog(project_id))
        self.add_task_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=20, pady=20)

        self.delete_project_button.config(command=lambda: asyncio.create_task(self.delete_project(project_id)))
        self.delete_project_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=20, pady=20)

        tasks = await get_tasks(project_id)

        for index, task in enumerate(tasks):
            frame = ttk.Frame(self.task_frame, relief=tk.RIDGE, padding=5)
            frame.pack(fill=tk.X, pady=3)

            label = ttk.Label(frame, text=f"{index + 1}: {task.name} — {task.status}", background="#293133", foreground="white")
            label.pack(side=tk.LEFT, padx=5)

            if task.status != "Erledigt":
                btn = ttk.Button(frame, text="Abschließen", command=lambda task_id=task.id: asyncio.create_task(self.finish_task(task_id)))
                btn.pack(side=tk.RIGHT)

            self.tasks_widgets.append(frame)

    async def delete_project(self, project_id):
        await delete_project(project_id)
        await self.load_projects()
        await self.load_tasks(0)

        self.add_task_button.pack_forget()
        self.delete_project_button.pack_forget()

        messagebox.showinfo("Nachricht", f"Projekt wurde erfolgreich gelöscht ✅")
    
    def add_task_dialog(self, project_id):
        name = simpledialog.askstring("Neue Aufgabe", "Name:")
        description = simpledialog.askstring("Neue Aufgabe", "Beschreibung:")
        if name and description:
            asyncio.create_task(self.create_task_and_reload(name, description, project_id))
    
    async def finish_task(self, task_id):
        await complete_task(task_id)
        selection = self.project_listbox.curselection()
        if selection:
            index = selection[0]
            project = self.projects[index]
            await self.load_tasks(project.id)
        messagebox.showinfo("Aufgabe abgeschlossen", f"Aufgaben-ID {task_id} wird als erledigt markiert ✅")


    async def create_task_and_reload(self, name, description, project_id):
        await create_task(name, description, project_id)
        await self.load_tasks(project_id)


def main():
    root = tk.Tk()

    root.configure(bg="#293133")
    root.option_add("*Font", ("Lucida Console", 11))
    root.option_add("*Background", "#293133")
    root.option_add("*Foreground", "white")

    async def runner():
        app = App(root)
        await app.initialize()
        while True:
            root.update()
            await asyncio.sleep(0.01)

    asyncio.run(runner())


if __name__ == "__main__":
    asyncio.run(main())
