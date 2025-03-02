from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import time
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# **1️⃣ Datenbankverbindung mit Azure SQL herstellen**
DATABASE_URL = os.getenv("DATABASE_URL")  # Holt den Wert aus den Umgebungsvariablen

# SQLAlchemy Setup für Azure SQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# **2️⃣ Datenbanktabelle definieren**
class TestTable(Base):
    __tablename__ = "perf_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    value = Column(String(100))

# **3️⃣ Datenbank erstellen (falls noch nicht vorhanden)**
Base.metadata.create_all(bind=engine)

# **4️⃣ Dependency für DB-Session**
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# **5️⃣ API-Endpunkte für CRUD-Operationen**
@app.get("/get_data")
def get_data():
    """Liest Daten aus Azure SQL"""
    start_time = time.time()
    db = SessionLocal()
    data = db.query(TestTable).limit(10).all()
    db.close()
    return {"response_time": time.time() - start_time, "data": [{"id": row.id, "name": row.name, "value": row.value} for row in data]}

@app.post("/update_data")
def update_data():
    """Fügt eine neue Zeile in Azure SQL ein"""
    start_time = time.time()
    db = SessionLocal()
    new_entry = TestTable(name="TestName", value="TestValue")
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    db.close()
    return {"response_time": time.time() - start_time, "status": "inserted", "id": new_entry.id}
