# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from psycopg2 import connect, OperationalError, errors
from models.models import Base
import config

class DatabaseManager:
    def __init__(self):
        self.config = config.Config()
        self.engine = create_engine(self.config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    def create_database_if_not_exists(self):
        try:
            # Kết nối tới PostgreSQL database 'postgres' (database mặc định)
            conn = connect(
                dbname="postgres",  # Kết nối tới database 'postgres'
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                host=self.config.DB_HOST,
                port=self.config.DB_PORT
            )
            conn.autocommit = True  # Tắt transaction block
            with conn.cursor() as cur:
                # Kiểm tra nếu database đã tồn tại
                try:
                    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.config.DB_NAME}'")
                    if not cur.fetchone():
                        cur.execute(f"CREATE DATABASE {self.config.DB_NAME}")
                        print(f"Database '{self.config.DB_NAME}' created.")
                    else:
                        print(f"Database '{self.config.DB_NAME}' already exists.")
                except errors.DuplicateDatabase:
                    print(f"Database '{self.config.DB_NAME}' already exists (caught error).")
            conn.close()  # Đóng kết nối sau khi thực thi
        except OperationalError as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def create_tables(self):
        # Kết nối tới database chính để tạo bảng
        engine = create_engine(self.config.DATABASE_URL)
        Base.metadata.create_all(engine)
        print("Tables created successfully.")

    def get_session(self):
        return self.Session()
