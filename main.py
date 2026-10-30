
from database import get_connection

def main():
    connection = None
    cursor = None

    try:
        # Connect to MySQL and create a separate database
        connection = get_connection(database=None)
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS chores_db")
        cursor.execute("USE chores_db")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chore_name VARCHAR(100) NOT NULL,
                assigned_to VARCHAR(100) NOT NULL,
                due_date DATE,
                status VARCHAR(20) DEFAULT 'Pending'
            )
        """)
        connection.commit()

        while True:
            print("\n===== CHORES RECORDER =====")
            print("1. Add Chore")
            print("2. View Chores")
            print("3. Update Chore")
            print("4. Delete Chore")
            print("5. Exit")

            choice = input("Choose an option: ").strip()

            # CREATE
            if choice == "1":
                name = input("Chore name: ").strip()
                person = input("Assigned to: ").strip()
                date = input("Due date (YYYY-MM-DD, blank if none): ").strip()
                date = date or None

                if not name or not person:
                    print("Chore name and assigned person are required.")
                    continue

                cursor.execute("""
                    INSERT INTO chores
                    (chore_name, assigned_to, due_date)
                    VALUES (%s, %s, %s)
                """, (name, person, date))

                connection.commit()
                print("Chore added successfully!")

            # READ
            elif choice == "2":
                cursor.execute("SELECT * FROM chores ORDER BY id")
                chores = cursor.fetchall()

                if not chores:
                    print("No chores found.")
                else:
                    for chore in chores:
                        print(chore)

            # UPDATE
            elif choice == "3":
                try:
                    chore_id = int(input("Enter chore ID: "))
                except ValueError:
                    print("Please enter a valid ID.")
                    continue

                cursor.execute(
                    "SELECT * FROM chores WHERE id = %s",
                    (chore_id,)
                )
                chore = cursor.fetchone()

                if chore:
                    name = input(f"Name [{chore[1]}]: ").strip() or chore[1]
                    person = input(f"Assigned to [{chore[2]}]: ").strip() or chore[2]
                    date = input(f"Due date [{chore[3] or ''}]: ").strip()
                    date = date or chore[3]
                    status = input(f"Status [{chore[4]}]: ").strip() or chore[4]

                    cursor.execute("""
                        UPDATE chores
                        SET chore_name=%s, assigned_to=%s,
                            due_date=%s, status=%s
                        WHERE id=%s
                    """, (name, person, date, status, chore_id))

                    connection.commit()
                    print("Chore updated successfully!")
                else:
                    print("Chore not found.")

            # DELETE
            elif choice == "4":
                try:
                    chore_id = int(input("Enter chore ID: "))
                except ValueError:
                    print("Please enter a valid ID.")
                    continue

                cursor.execute(
                    "SELECT chore_name FROM chores WHERE id = %s",
                    (chore_id,)
                )
                chore = cursor.fetchone()

                if chore:
                    confirm = input(
                        f"Delete '{chore[0]}'? (yes/no): "
                    ).strip().lower()

                    if confirm == "yes":
                        cursor.execute(
                            "DELETE FROM chores WHERE id = %s",
                            (chore_id,)
                        )
                        connection.commit()
                        print("Chore deleted successfully!")
                    else:
                        print("Deletion cancelled.")
                else:
                    print("Chore not found.")

            # EXIT
            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")

    except Exception as error:
        print("Error:", error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
