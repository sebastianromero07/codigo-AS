from fastapi import FastAPI
from sqlalchemy import create_engine
from .routes import router
from .models import Base

# Crear una base de datos SQLite en memoria o en un archivo local para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./payments_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Configuración básica en caso de querer correr el microservicio individualmente
app = FastAPI(title="Payments Service API", description="Microservicio de pagos e inversión.")

# Crear tablas en dev
Base.metadata.create_all(bind=engine)

app.include_router(router)