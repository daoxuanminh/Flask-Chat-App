class Friends(db.Model):
    __tablename__ = 'friends'
    user1_id = db.Column(db.Integer, primary_key=True)
    user2_id = db.Column(db.Integer)