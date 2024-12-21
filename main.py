import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

engine = create_engine("sqlite:///db.sqlite")
Base = declarative_base()

class Skill(Base):
	__tablename__ = "skills"
	id = Column(Integer, primary_key=True)
	idCode = Column(String)
	name = Column(String)
	url = Column(String)
	description = Column(String)

url = "https://edwardtanguay.vercel.app/share/skills.json"

response = requests.get(url)

# save to sqlite
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
if response.status_code == 200:
	data = response.json()
	for item in data:
		skill = Skill(idCode=item['idCode'], name=item['name'], url=item['url'], description=item['description'])
		session.add(skill)
else:
	print(f"Failed to fetch data: {response.status_code}")
session.commit()

# display data
skills = session.query(Skill).all()
for skill in skills:
	print(f"RECORD #{skill.id}: {skill.name}")