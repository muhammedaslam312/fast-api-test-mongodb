from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

    # Create a one-to-one relationship to UserProfile
    user_profile = relationship("UserProfile", back_populates="user")


# postgres second table
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id")
    )  # Foreign key reference to User table
    profile_picture = Column(String)

    # Create a back-reference to User
    user = relationship("User", back_populates="user_profile")


# mongo-db profile collection
class Profile(BaseModel):
    user_id: int
    profile_picture: str
