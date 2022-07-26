"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)

    # reservations = a list of reservation objects

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

    @classmethod
    def create(cls, email):
        """Create and return a new user."""

        return cls(email=email)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()


class Reservation(db.Model):
    """A Reservation."""

    __tablename__ = "reservations"

    reservation_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="reservations")

    def __repr__(self):
        return f"<Reservation res_id={self.reservation_id} by user {self.user_id}>"

    @classmethod
    def create(cls, date, start_time, end_time, user_id):
        """Create and return a new reservation."""

        return cls(date=date, start_time=start_time, end_time=end_time, user_id=user_id)

    # @classmethod
    # def update(cls, rating_id, new_score):
    #     """ Update a rating given rating_id and the updated score. """
    #     rating = cls.query.get(rating_id)
    #     rating.score = new_score


def connect_to_db(flask_app, db_uri="postgresql:///reservations", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
