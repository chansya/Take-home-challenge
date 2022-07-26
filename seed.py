"""Script to seed database."""

import os
import json
# from random import choice, randint
# from datetime import datetime

import model
import server

os.system("dropdb reservations")
os.system("createdb reservations")

model.connect_to_db(server.app)
model.db.create_all()

# Load user data from JSON file
with open("data/users.json") as f:
    user_data = json.loads(f.read())

users_in_db = []
for user in user_data:
    user_email = user['email']
    db_user = model.User.create(user_email)
    users_in_db.append(db_user)


model.db.session.add_all(users_in_db)
model.db.session.commit()

# Create 10 users; each user will make 10 ratings
# for n in range(10):
#     email = f"user{n}@test.com"  # Voila! A unique email!
#     password = "test"

#     user = model.User.create(email, password)
#     model.db.session.add(user)

#     for _ in range(10):
#         random_movie = choice(movies_in_db)
#         score = randint(1, 5)

#         rating = model.Rating.create(user, random_movie, score)
#         model.db.session.add(rating)

# model.db.session.commit()
