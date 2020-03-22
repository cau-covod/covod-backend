import time

from covod.models.models import db, User, Course, Lecture, OAuth2Client

db.drop_all()
print("Dropped existing data")
db.create_all()
print("Created tables")


user = User(id=1, username="test", full_name="Test User", password="passwort")
course = Course(name="Bleh", description="Blah blah", user_id=1)
lecture = Lecture(number=1, name="Blu blu", course=course)

client = OAuth2Client(
    user=user,
    client_id="PPDPDvXf7bkd5bDLVhttUIxn",
    client_secret="qvU7ckxCxYZBNfIItVRtPp5mML9UxnTu4M31migU9FYXTj13",
    client_id_issued_at=int(time.time()),
    client_secret_expires_at=int(time.time())+3600*24*90,
)

client_metadata = {
    "client_name": "testclient",
    "client_uri": "",
    "grant_types": "password",
    "redirect_uris": "",
    "response_types": "code",
    "scope": "upload view",
    "token_endpoint_auth_method": "client_secret_post"
}

client.set_client_metadata(client_metadata)

db.session.add(user)
db.session.commit()

course.add_user(user)

db.session.add(course)
db.session.add(lecture)
db.session.add(client)
db.session.commit()

print("Added dummy data to database!")
