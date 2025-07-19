"""
models.py

Modul ini mendefinisikan struktur tabel database menggunakan SQLAlchemy ORM
untuk aplikasi pembayaran listrik pascabayar.

Model:
- User: Menyimpan informasi pengguna.
- Pemakaian: Menyimpan catatan pemakaian listrik bulanan oleh pengguna.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    """
    Model untuk menyimpan informasi pengguna.

    Attributes:
        id (int): Primary key pengguna.
        username (str): Nama pengguna yang unik.
        password (str): Hash password pengguna.
        role (str): Peran pengguna ('admin' atau 'pelanggan').
        pemakaian (list): Relasi ke data pemakaian listrik pengguna ini.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # 'admin' atau 'pelanggan'

    # Relasi satu ke banyak dengan tabel Pemakaian
    pemakaian = relationship("Pemakaian", back_populates="user")

class Pemakaian(Base):
    """
    Model untuk menyimpan catatan pemakaian listrik pengguna.

    Attributes:
        id (int): Primary key pemakaian.
        user_id (int): Foreign key yang mengacu ke ID pengguna.
        bulan (str): Bulan pemakaian (contoh: "Januari").
        tahun (int): Tahun pemakaian.
        kwh (float): Jumlah KWH yang digunakan.
        total_tagihan (float): Total tagihan berdasarkan KWH.
        created_at (datetime): Tanggal dan waktu data dibuat.
        user (User): Relasi ke objek pengguna terkait.
    """
    __tablename__ = 'pemakaian'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bulan = Column(String)
    tahun = Column(Integer)
    kwh = Column(Float)
    total_tagihan = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relasi ke model User
    user = relationship("User", back_populates="pemakaian")
