from sqlalchemy import *
from sqlalchemy.orm import declarative_base 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from faker import Faker
from random import choice, randint, random, randrange

engine = create_engine('sqlite:///mydb.db')


Base = declarative_base()
fake = Faker()
fake = Faker('fr-FR')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    group_id = Column(Integer, ForeignKey('groups.id'))

    # Relation avec la seconde table
    addresses = relationship("Address", back_populates="user")
    group = relationship("Group", back_populates="users")

# Définition du modèle pour la seconde table
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relation avec la première table
    user = relationship("User", back_populates="addresses")

# Définition du modèle pour la troisième table
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relation avec la première table
    users = relationship("User", back_populates="group")

# Création des tables dans la base de données
Base.metadata.create_all(engine)


session = sessionmaker(bind=engine)
session = session()

# Création des groupes

groups = []

for i in range(1, 3):
    group = Group(name ='Group ' + str(i))
    groups.append(group)

# Création de deux utilisateurs dans le premier groupe


users = []

for i in range(1, 6):
    
    user = User(name = fake.name(), age = 30, group = random.choice(groups))
    users.append(user)



for x in groups:
    session.add(x)

for x in users:
     session.add(x)

# Ajout des utilisateurs à la session
#session.add_all([group1, group2, user1, user2, user3])

# Commit de la session pour enregistrer les modifications dans la base de données
session.commit()

# Récupération des utilisateurs du premier groupe
users_in_group1 = session.query(User).filter_by(group_id = 1).all()

# Affichage des utilisateurs du premier groupe
print("Users in group 1:")
for user in users_in_group1:
    print(f"Name: {user.name}, Age: {user.age}")




Base.metadata.create_all(engine)