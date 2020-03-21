from covod.models.models import db, User, Course, Lecture

db.create_all()
u = User(username="test", full_name="Test User", password="passwort")
c = Course(name="Bleh", description="Blah blah")
l = Lecture(number=1, name="Blu blu", course=c)
db.session.add(c)
db.session.add(l)
db.session.commit()
print("Added dummy data to database!")