# migrate.py
from database import DatabaseManager

def migrate():
    db_manager = DatabaseManager()
    db_manager.create_database_if_not_exists()
    db_manager.create_tables()

if __name__ == "__main__":
    migrate()
