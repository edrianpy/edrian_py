`screenshot.png`

# To-Do List Application

This is a simple To-Do List application built with Python and MySQL. It allows users to manage tasks by adding, viewing, completing, and deleting them from a MySQL database.

## Features
- **Add Tasks**: Add tasks with a title and description.
- **View Tasks**: View all tasks along with their status.
- **Mark as Completed**: Mark tasks as completed.
- **Delete Tasks**: Remove tasks from the list.

## Database Configuration
The database connection is managed in the `database.py` file. The connection parameters are set using environment variables with default values:

- **Host**: `localhost`
- **Port**: `3306`
- **User**: `root`
- **Password**: (empty by default)
- **Database**: `todo_db`

### Example of `database.py` Connection
The `get_connection` function in `database.py` establishes a connection to the MySQL database:

```python
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )