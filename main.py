from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

import database
import hashing
import models
import schemas
from database import SessionLocal, engine
from response import ErrorResponseModel, ResponseModel

models.Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# First Task(UsingpostgreSQL and MongoDb)- Registration
@app.post(
    "/register1/",
    response_description="User data added into the database",
    tags=["users"],
)
async def create_user(
    request: schemas.UserRegistrationWithPicture, db: Session = Depends(get_db)
):
    # Check if the email already exists
    existing_user = (
        db.query(models.User).filter(models.User.email == request.email).first()
    )
    if existing_user:
        return ErrorResponseModel(
            "An error occurred.", 400, "Email already registered."
        )
    try:
        hassed_password = hashing.Hash.bcrypt(request.password)
        new_user = models.User(
            first_name=request.first_name,
            email=request.email,
            phone=request.phone,
            password=hassed_password,
        )
        print(new_user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # here im using profile_picture_url from from front end
        profile = {"user_id": new_user.id, "profile_picture": request.profile_picture}
        new_profile = await database.add_profile(profile)

        # Create a response dictionary with combined data
        response_data = {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "email": new_user.email,
            "phone": new_user.phone,
            "profile_picture": new_profile["profile_picture"],
        }

        return ResponseModel(response_data, "User added successfully.")

    except Exception as e:
        db.rollback()
        error = str(e)
        return ErrorResponseModel("An error occurred.", 500, error)


# Second Task(UsingpostgreSQL only)- Registration
@app.post(
    "/register2/",
    response_description="User data added into the database",
    tags=["users"],
)
def create_user2(
    request: schemas.UserRegistrationWithPicture, db: Session = Depends(get_db)
):
    # Check if the email already exists
    existing_user = (
        db.query(models.User)
        .filter(
            or_(models.User.email == request.email, models.User.phone == request.phone)
        )
        .first()
    )
    print(existing_user)
    if existing_user:
        return ErrorResponseModel(
            "An error occurred.", 400, "Email or Phone already registered."
        )
    try:
        hassed_password = hashing.Hash.bcrypt(request.password)
        new_user = models.User(
            first_name=request.first_name,
            email=request.email,
            phone=request.phone,
            password=hassed_password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        new_user_profile = models.UserProfile(
            user_id=new_user.id, profile_picture=request.profile_picture
        )
        db.add(new_user_profile)
        db.commit()
        db.refresh(new_user_profile)

        # Create a response dictionary with combined data
        response_data = {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "email": new_user.email,
            "phone": new_user.phone,
            "profile_picture": new_user_profile.profile_picture,
        }

        return ResponseModel(response_data, "User added successfully.")

    except Exception as e:
        db.rollback()
        error = str(e)
        return ErrorResponseModel("An error occurred.", 500, error)


# Get User of Two Task --merged


@app.get("/user/{id}/", response_description="User data retrieved")
async def user_details(id, db: Session = Depends(get_db)):
    user_obj = db.query(models.User).filter(models.User.id == id).first()

    mongo_profile_obj = await database.retrieve_profile(id)

    psql_user_profile_obj = (
        db.query(models.UserProfile).filter(models.UserProfile.user == user_obj).first()
    )

    if user_obj:
        if mongo_profile_obj:
            response_data = {
                "id": user_obj.id,
                "first_name": user_obj.first_name,
                "email": user_obj.email,
                "phone": user_obj.phone,
                "mongo_profile_picture": mongo_profile_obj["profile_picture"],
            }

            return ResponseModel(response_data, "User data retrieved successfully")
        else:
            # psql only get method
            response_data = {
                "id": user_obj.id,
                "first_name": user_obj.first_name,
                "email": user_obj.email,
                "phone": user_obj.phone,
                "psql_profile_picture": psql_user_profile_obj.profile_picture,
            }

        return ResponseModel(response_data, "User data retrieved successfully")

    else:
        return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")
