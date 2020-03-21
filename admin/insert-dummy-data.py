from covod.models.models import db, Course, Lecture

db.create_all()
c = Course(name="Bleh", description="Blah blah")
l = Lecture(number=1, name="Blu blu", course=c)
db.session.add(c)
db.session.add(l)
db.session.commit()
