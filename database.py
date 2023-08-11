import motor.motor_asyncio
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import os
from dotenv import load_dotenv

load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


MONGO_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.profiles
profile_collection = database.get_collection("profile")



def profile_helper(profile) -> dict:
    return {
        "user_id": str(profile["user_id"]),
        "profile_picture": profile["profile_picture"],
    }


# Retrieve all profiles present in the database
async def retrieve_profiles():
    profiles = []
    async for profile in profile_collection.find():
        profiles.append(profile_helper(profile))
    return profiles


# Add a new Profile in to database
async def add_profile(profile_data: dict) -> dict:
    profile = await profile_collection.insert_one(profile_data)
    new_profile = await profile_collection.find_one({"_id": profile.inserted_id})
    return profile_helper(new_profile)


# Retrieve a profile with a matching ID
async def retrieve_profile(id: int) -> dict:
    profile = await profile_collection.find_one({"user_id": int(id)})
    if profile:
        return profile_helper(profile)
