from mongoengine import connect
from mongoengine import Document, StringField, ListField, DateTimeField
from mongoengine import NotUniqueError
from datetime import datetime
import pandas as pd
import names

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
connect(
    db='mongodb',  # Specify your database name
    host='localhost',         # Host is localhost
    port=27017,               # Port is the one mapped in the Docker run command
    username='username',  # Use the username you set
    password='password'   # Use the password you set
)


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
    
