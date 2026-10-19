import json
import os

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Fayldan mövcud tapşırıqları oxuyur."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Xəbərdarlıq: Fayl zədələnib, yeni siyahı yaradılır.")
                return []
        return []

    def save_tasks(self):
        """Tapşırıqları JSON faylına yadda saxlayır."""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)
        except IOError:
            print("Xəta: Faylı yadda saxlamaq mümkün olmadı!")

    def add_task(self, title):
        """Yeni tapşırıq əlavə edir."""
        if not title.strip():
            print("Xəta: Tapşırıq başlığı boş ola bilməz!")
            return

        new_id = self.tasks[-1]["id"] + 1 if self.tasks else 1
        task = {
            "id": new_id,
            "title": title,
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"Uğurla əlavə olundu: '{title}'")

    def list_tasks(self):
        """Bütün tapşırıqları ekrana çıxarır."""
        if not self.tasks:
            print("\nHələ heç bir tapşırıq yoxdur.")
            return

        print("\n--- TAPŞIRIQLAR SİYAHISI ---")
        for task in self.tasks:
            status = "İcra olundu [X]" if task["completed"] else "Gözləmədə [ ]"
            print(f"{task['id']}. {task['title']} -- {status}")
        print("-" * 28)

    def complete_task(self, task_id):
        """Tapşırığı tamamlandı olaraq işarələyir."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                print(f"Tapşırıq #{task_id} tamamlandı olaraq işarələndi.")
                return
        print(f"Xəta: {task_id} ID-li tapşırıq tapılmadı.")

    def delete_task(self, task_id):
        """Tapşırığı silir."""
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                print(f"Tapşırıq #{task_id} silindi.")
                return
        print(f"Xəta: {task_id} ID-li tapşırıq tapılmadı.")


# Əsas menyu və tətbiqin işə düşməsi
def main():
    manager = TaskManager()

    while True:
        print("\n--- MENYU ---")
        print("1. Tapşırıqlara bax")
        print("2. Yeni tapşırıq əlavə et")
        print("3. Tapşırığı tamamla")
        print("4. Tapşırığı sil")
        print("5. Çıxış")

        choice = input("Seçiminizi daxil edin (1-5): ").strip()

        if choice == "1":
            manager.list_tasks()
        elif choice == "2":
            title = input("Tapşırıq başlığını daxil edin: ")
            manager.add_task(title)
        elif choice == "3":
            try:
                task_id = int(input("Tamamlanacaq tapşırığın ID-si: "))
                manager.complete_task(task_id)
            except ValueError:
                print("Xəta: Zəhmət olmasa rəqəm daxil edin!")
        elif choice == "4":
            try:
                task_id = int(input("Silinəcək tapşırığın ID-si: "))
                manager.delete_task(task_id)
            except ValueError:
                print("Xəta: Zəhmət olmasa rəqəm daxil edin!")
        elif choice == "5":
            print("Proqramdan çıxılır. Hələlik!")
            break
        else:
            print("Yanlış seçim! 1 və 5 arasında rəqəm daxil edin.")

if __name__ == "__main__":
    main()