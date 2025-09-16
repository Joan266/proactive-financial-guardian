# create_tables.py
from guardian_orchestrator.database import engine, Base
from guardian_orchestrator.models import User  

print("Connecting to the database and creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")