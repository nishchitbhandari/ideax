from mongoengine import connect
from mongoengine import Document, StringField, ListField, DateTimeField
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


class User(Document):
    name = StringField(required=True)
    username = StringField(required=True)
    clerk_id = StringField(required=True, unique=True)  # Unique clerk_id
    email = StringField(required=True)
    password = StringField(required=False)
    role = StringField(choices=["student", "teacher", "null"], required=True)
    bio = StringField(required=False)
    picture = StringField(required=False)
    specializations = ListField(StringField(), required=True)
    join_at = DateTimeField(required=True)


# Connect to MongoDB
connect(
    db='mongodb',  # Replace with your database name
    host='localhost',         # Host is localhost
    port=27017,               # Default MongoDB port
    username=os.getenv('USERNAME'),  # Your MongoDB username
    password=os.getenv("PASSWORD")   # Your MongoDB password
)


def get_all_users():
    users = User.objects()  # Get all users
    return pd.DataFrame.from_dict([{"Id": str(user.clerk_id), "Subject speciality": ", ".join(user.specializations)} for user in users])
