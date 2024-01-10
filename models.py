from extensions import db, app, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    comments = db.relationship('Comment', back_populates='user')

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)


    user = db.relationship('User', back_populates='comments')
    work = db.relationship('Work', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment id={self.id}, user_id={self.user_id}, work_id={self.work_id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class Work(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    person = db.Column(db.String)
    img = db.Column(db.String)





if __name__ == "__main__":
    works = [
        {"name": "Starry Night", "person": "Lazare Mtskeradze", "img": "pic1.webp", "id": 0},
        {"name": "Starry Night", "person": "Lazare Mtskeradze", "img": "pic2.webp", "id": 1},
        {"name": "Starry Night", "person": "Lazare Mtskeradze", "img": "pic3.jpg", "id": 2},
        {"name": "Starry Night", "person": "Lazare Mtskeradze", "img": "pic3.webp", "id": 3},
        {"name": "Starry Night", "person": "Lazare Mtskeradze", "img": "pic5.jpg", "id": 4},
        {"name": "The Scream", "person": "Lazare Mtskeradze", "img": "pic6.jpg", "id": 5},
        {"name": "Starry Night", "person": "Lazare Mtskeradze", "img": "pic7.jpg", "id": 6},
        {"name": "Starry Night", "person": "Lazare Mtskeradze", "img": "pic8.jpg", "id": 7}
    ]
    with app.app_context():
        db.create_all()

        for work in works:
            new_work = Work(name=work['name'], person=work['person'], img=work['img'])
            new_work.create()

        admin_user = User(username="admin_user", password="password123", role="admin")
        admin_user.create()



