# create_tables.py
from app.database import engine, Base
from app.models import User  # Make sure to import all your models here

print("Connecting to the database and creating tables...")

# This line reads your models' metadata and creates the actual tables
# in the PostgreSQL database connected to by the engine.
Base.metadata.create_all(bind=engine)

print("Tables created successfully.")