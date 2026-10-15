
from database import get_connection


def add_task():
    title = input("Enter task title: ").strip()
    description = input("Enter description: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()
        query = """
            INSERT INTO tasks (title, description)
            VALUES (%s, %s)
        """

        cursor.execute(query, (title, description))
        connection.commit()

        print("Task added successfully!")

    except Exception as error:
        print("Error:", error)

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()


def view_tasks():
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, title, description, status FROM tasks ORDER BY id DESC"
        )

        tasks = cursor.fetchall()

        if not tasks:
            print("\nNo tasks found.")
            return

        print("\n--- YOUR TASKS ---")

        for task in tasks:
            task_id, title, description, status = task
            print(f"\nID: {task_id}")
            print(f"Title: {title}")
            print(f"Description: {description or 'None'}")
            print(f"Status: {status}")

    except Exception as error:
        print("Error:", error)

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()


def complete_task():
    try:
        task_id = int(input("Enter task ID to complete: "))

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE tasks SET status = %s WHERE id = %s",
            ("Completed", task_id)
        )
        connection.commit()

        if cursor.rowcount:
            print("Task marked as completed!")
        else:
            print("Task not found.")

        cursor.close()
        connection.close()

    except ValueError:
        print("Please enter a valid task ID.")
    except Exception as error:
        print("Error:", error)


def delete_task():
    try:
        task_id = int(input("Enter task ID to delete: "))

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )
        connection.commit()

        if cursor.rowcount:
            print("Task deleted successfully!")
        else:
            print("Task not found.")

        cursor.close()
        connection.close()

    except ValueError:
        print("Please enter a valid task ID.")
    except Exception as error:
        print("Error:", error)


def main():
    while True:
        print("\n===== TO-DO LIST =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
