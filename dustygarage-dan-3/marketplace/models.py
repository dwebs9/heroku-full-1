from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    lastName = db.Column(db.String(100), index=True, nullable=False)
    emailid = db.Column(db.String(100), index=True,
                        unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bids = db.relationship('Bid', backref='user')
    tools = db.relationship('Tool', backref='user')

    def __repr__(self):
        return "<Name: {}, ID: {}, Last Name {}>".format(self.name, self.id, self.lastName)


class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    bid_date = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'))

    def __repr__(self):
        return "<bid_amount: {}, id: {}, user_id: {}, tool_id: {}>".format(self.bid_amount, self.id, self.user_id, self.tool_id)


class Tool(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(100))
    modelNo = db.Column(db.String(100))
    list_price = db.Column(db.Numeric(10))
    images = db.Column(db.String(1000), default='noimage.png')
    category = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    desc = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.now())
    sold_status = db.Column(db.String(100), default="")
    sold_date = db.Column(db.String(50))

    bid_id = db.relationship('Bid', backref='tools')

    def __repr__(self):
        return "\n\n<Tool Name: {}\n Tool ID: {}\n Brand: {}\n sold_status: {}\n User Id: {} \nImages: {}>\n".format(
            self.tool_name, self.id, self.brand, self.sold_status, self.user_id, self.images
        )
