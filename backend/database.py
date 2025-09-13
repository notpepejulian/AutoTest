from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.exc import SQLAlchemyError

# URL de conexión a la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://autotest_user:autotest_pass@localhost:3306/autotest_db")

try:
    # Crear el motor de la base de datos
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    
    # Probar la conexión
    with engine.connect() as connection:
        connection.execute("SELECT 1")
        
except SQLAlchemyError as e:
    print(f"Error al conectar con la base de datos: {e}")
    raise

# Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()