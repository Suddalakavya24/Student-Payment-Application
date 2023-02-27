from datetime import datetime
from PaymentApplication import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    rollnumber = db.Column(db.String(20), unique=True, nullable=False)
    branch = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    transactions = db.relationship('Transaction', backref='payer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


class Transaction(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"{self.user_id}"

class DebitCardInfo(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cardholderName=db.Column(db.String(100), nullable=False)
    cardNumber=db.Column(db.String(19), nullable=False)
    expiryDate=db.Column(db.String,nullable=False)
    cvv=db.Column(db.Integer,nullable=False)

    

