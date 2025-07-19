from database import Base, engine
from models import User, Pemakaian

Base.metadata.create_all(bind=engine)
print("Tabel berhasil dibuat!")
