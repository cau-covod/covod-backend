import time

from covod.models.models import db, User, Course, Lecture, OAuth2Client, Comment

db.drop_all()
print("Dropped existing data")
db.create_all()
print("Created tables")


user = User(username="test", full_name="Frau Professor", password="passwort")
user2 = User(username="benutzer", full_name="Ben Utzer", password="jajajaja")
course = Course(name="Bleh", description="Blah blah", user_id=1)
lecture = Lecture(number=1, name="Blu blu", course=course)

c1 = Comment(text="Ist gut gemacht.", user_id=2, lecture_id=1)
c2 = Comment(text="Dankeschön!", user_id=1, parent=c1, lecture_id=1)
c3 = Comment(text="Aber ich hab nicht genau Verstanden warum das so ist?", user_id=2,
             parent=c1, lecture_id=1, timestamp=1337)
c4 = Comment(text="Gaanz einfach…", user_id=1, parent=c3, lecture_id=1)

for c in [c1, c2, c3, c4]:
    c.save()

course.add_user(user)

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
db.session.add(course)
db.session.add(lecture)
db.session.add(client)

db.session.commit()
print("Added dummy data to database!")
