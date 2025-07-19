"""
database.py

Modul konfigurasi database menggunakan SQLAlchemy.
Digunakan untuk mengatur koneksi ke database PostgreSQL dan membuat session.

Fitur:
- Mengatur koneksi ke PostgreSQL
- Menyediakan factory `SessionLocal` untuk membuat sesi database
- Menyediakan `Base` untuk mendefinisikan model ORM
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL koneksi ke database PostgreSQL
DATABASE_URL = "postgresql://listrik_user:noufalznak09@localhost:5432/listrik_db"

# Inisialisasi engine untuk koneksi ke database
engine = create_engine(DATABASE_URL)

# Session factory untuk membuat session baru pada tiap permintaan
SessionLocal = sessionmaker(bind=engine)

# Base class yang digunakan semua model ORM akan diwarisi dari sini
Base = declarative_base()