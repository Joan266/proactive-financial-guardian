# create_tables.py
from app.database import engine, Base
from app.models import User  

print("Connecting to the database and creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")