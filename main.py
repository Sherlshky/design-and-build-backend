import base64
from typing import List

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine
from facial_recognition import register_face, detect_face, remove_face

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Global variables to store the latest detection result and command
latest_detection_result = None
latest_command = None


@app.post("/image/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    # Process the image using the facial recognition service
    annotated_image, username = detect_face(contents)
    # Store the detection result
    global latest_detection_result
    latest_detection_result = {
        "annotated_image": base64.b64encode(annotated_image).decode("utf-8"),
        "username": username,
    }
    # Record check-in if a face is recognized
    if username:
        record = models.Record(username=username)
        db.add(record)
        db.commit()
    return {
        "message": "Image uploaded successfully.",
        "annotated_image": latest_detection_result["annotated_image"]
    }


@app.get("/detection_result/", response_model=schemas.DetectionResult)
def get_detection_result():
    if latest_detection_result:
        return latest_detection_result
    else:
        raise HTTPException(status_code=404, detail="No detection result available.")


@app.get("/user/{username}/", response_model=schemas.UserInDB)
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        face_image_base64 = (
            base64.b64encode(user.face_image).decode("utf-8")
            if user.face_image
            else None
        )
        user_out = schemas.UserInDB(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            password=user.password,
            exp=user.exp,
            email=user.email,
            face_image=face_image_base64,
        )
        return user_out
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/", status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    face_image_data = base64.b64decode(user.face_image)
    db_user = models.User(
        username=user.username,
        password=user.password,
        face_image=face_image_data,
        nickname=user.nickname,
        exp=user.exp,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Register the face using the facial recognition service
    register_face(face_image_data, user.username)

    return {"message": "User created successfully."}


@app.put("/user/{username}/")
def update_user(
        username: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        if user_update.password is not None:
            user.password = user_update.password
        if user_update.face_image is not None:
            face_image_data = base64.b64decode(user_update.face_image)
            user.face_image = face_image_data
            # Update the face in the facial recognition service
            remove_face(user.username)
            register_face(face_image_data, user.username)
        if user_update.nickname is not None:
            user.nickname = user_update.nickname
        if user_update.exp is not None:
            user.exp = user_update.exp
        if user_update.email is not None:
            user.email = user_update.email
        db.commit()
        return {"message": "User updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/user/{username}/", status_code=204)
def delete_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        # Remove the face from the facial recognition service
        remove_face(username)
        db.delete(user)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/user/", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/control/")
def send_control_command(
        command: schemas.ControlCommand, db: Session = Depends(get_db)
):
    global latest_command
    latest_command = command.command
    return {"message": "Command sent to robot."}


@app.get("/control/")
def get_control_command():
    global latest_command
    command = latest_command
    latest_command = ""
    return {"command": command}


@app.get("/records/", response_model=List[schemas.Record])
def get_records(db: Session = Depends(get_db)):
    records = db.query(models.Record).all()
    return [
        schemas.Record(username=record.username, timestamp=record.timestamp.isoformat())
        for record in records
    ]
