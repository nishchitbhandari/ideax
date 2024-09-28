from mongoengine import connect
from mongoengine import Document, StringField, ListField, DateTimeField
from mongoengine import NotUniqueError
from datetime import datetime
import pandas as pd
import os
import names
from dotenv import load_dotenv

load_dotenv()

class User(Document):
    name = StringField(required=True)
    username = StringField(required=True)
    clerk_id = StringField(required=True, unique=True)  # Ensure clerk_id is unique
    email = StringField(required=True)
    password = StringField(required=False)
    role = StringField(choices=["student", "teacher", "null"], required=True)
    bio = StringField(required=False)
    picture = StringField(required=False)
    specializations = ListField(StringField(), required=True)
    join_at = DateTimeField(required=True)

# Connect to the MongoDB database running in the Docker container
# Load environment variables
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_HOST = os.getenv("RAILWAY_PRIVATE_DOMAIN")
MONGO_PORT = os.getenv("MONGOPORT")

# Construct the MongoDB URL
mongo_url = os.getenv("MONGO_URL")

# Connect to MongoDB
connect(host=mongo_url)


def add_user(name, username, clerk_id, email, role, specializations):
    user = User(
        name=name,
        username=username,
        clerk_id=clerk_id,
        email=email,
        role=role,
        specializations=specializations,
        join_at=datetime.now()
    )
    try:
        user.save()  # Save the user to the database
        print(f"User {name} added successfully.")
    except NotUniqueError:
        print(f"Error: The clerk_id '{clerk_id}' already exists. Please use a different one.")

df = pd.read_csv("dataset.csv")

for index, row in df.iterrows():
    integer = row[0]
    specializations = row[1].split(", ")
    name = names.names[integer-1]
    username = f"{name.lower()}{integer}"
    clerk_id = f"User{integer}"
    email = f"{name.lower()}{integer}@gmail.com"
    role = "teacher"    
    add_user(name=name, username=username, clerk_id=clerk_id, email=email, role=role, specializations=specializations)
    
