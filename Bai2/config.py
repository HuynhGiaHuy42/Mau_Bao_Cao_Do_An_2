class Config:
    DB_NAME = "QLSinhVien"
    DB_USER = "postgres"
    DB_PASSWORD = "123456"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME.lower()}"
    
    @property
    def DEFAULT_DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/postgres"
