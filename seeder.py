"""
seed_users.py

Skrip untuk menambahkan data awal pengguna ke dalam database PostgreSQL
untuk aplikasi pembayaran listrik pascabayar.

Menambahkan:
- Admin (username: admin, password: admin123)
- Pelanggan (username: noufal, password: noufalznak09)

Password di-hash menggunakan Werkzeug.
"""

from database import SessionLocal
from models import User
from werkzeug.security import generate_password_hash

# Inisialisasi session database
db = SessionLocal()

# Buat user admin dan pelanggan dengan password yang di-hash
admin = User(username="admin", password=generate_password_hash("admin123"), role="admin")
pelanggan = User(username="noufal", password=generate_password_hash("noufalznak09"), role="pelanggan")

# Tambahkan kedua user ke database
db.add_all([admin, pelanggan])
db.commit()
db.close()

print("Data user berhasil ditambahkan.")
