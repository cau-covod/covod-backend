import time

from covod.models.models import db, User, Course, Lecture, OAuth2Client, Comment

db.drop_all()
print("Dropped existing data")
db.create_all()
print("Created tables")


user = User(username="test", full_name="Prof. Essor", password="passwort")
user2 = User(username="benutzer", full_name="Ben Utzer", password="passwort")
db.session.add(user)
db.session.add(user2)
db.session.commit()

course = Course(name="Einführung in die Humangeographie",
                description="In diesem Kurs werden die Grundlagen der Humangeographie behandelt.", user_id=1)
db.session.add(course)
db.session.commit()

lecture = Lecture(number=1, name="Einleitung", course=course)
lecture2 = Lecture(number=2, name="Geschichte der Humangeographie", course=course,
                   description="Eine kurze Geschichte der Humangeographie beginnend im 18. Jahrhundert über die "
                               "Jahrhunderte bis in die Gegenwart.")
lecture3 = Lecture(number=3, name="Städte", course=course,
                   description="Was sind Städte? Wie enstehen sie?")
lecture4 = Lecture(number=4, name="Städte 2", course=course)
lecture5 = Lecture(number=5, name="Demographie", course=course)
db.session.add(lecture)
db.session.add(lecture2)
db.session.add(lecture3)
db.session.add(lecture4)
db.session.add(lecture5)
db.session.commit()

c1 = Comment(text="Ist gut gemacht.", user_id=2, lecture_id=1)
c2 = Comment(text="Dankeschön!", user_id=1, parent=c1, lecture_id=1)
c3 = Comment(text="Warum genau ist das so?", user_id=2, lecture_id=1, timestamp=30)
c4 = Comment(text="Gaanz einfach…", user_id=1, parent=c3, lecture_id=1)
c5 = Comment(text="Vielen Dank!", user_id=2, lecture_id=1, parent=c4)

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

client2 = OAuth2Client(
    user=user2,
    client_id="JCzWoDAfCrrQSwa5LZDSVtMp",
    client_secret="cPlToP59AfnRaIGQKumLQUrmI6vwR8VfVa5HPVUfDWQY54uX",
    client_id_issued_at=int(time.time()),
    client_secret_expires_at=int(time.time())+3600*24*90,
)

client_metadata = {
    "client_name": "testclient",
    "client_uri": "",
    "grant_types": "password",
    "redirect_uris": "",
    "response_types": "code",
    "scope": "upload view comment",
    "token_endpoint_auth_method": "client_secret_post"
}

client2_metadata = {
    "client_name": "testuser",
    "client_uri": "",
    "grant_types": "password",
    "redirect_uris": "",
    "response_types": "code",
    "scope": "view comment",
    "token_endpoint_auth_method": "client_secret_post"
}

client.set_client_metadata(client_metadata)
client2.set_client_metadata(client2_metadata)

db.session.add(client)
db.session.add(client2)
db.session.commit()

print("Added dummy data to database!")
