"""
auth.py

Modul autentikasi untuk Aplikasi Pembayaran Listrik Pascabayar.
Menyediakan endpoint login untuk menghasilkan token JWT.

Fitur:
- Login pengguna (username dan password)
- Verifikasi hash password menggunakan Werkzeug
- Pembuatan JWT token untuk autentikasi
"""

from flask import Blueprint, request, jsonify
import jwt
import datetime
from werkzeug.security import check_password_hash
from database import SessionLocal
from models import User

# Blueprint Flask untuk rute autentikasi
auth_bp = Blueprint("auth", __name__)

# Kunci rahasia JWT (Jangan gunakan ini di production!)
SECRET_KEY = "rahasia"

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Endpoint login untuk menghasilkan token JWT.

    Request:
        JSON berisi:
        - username (str)
        - password (str)

    Returns:
        200 OK:
            JSON berisi token JWT, role, dan ID user jika login berhasil.
        401 Unauthorized:
            JSON pesan kesalahan jika username/password salah.
    """
    db = SessionLocal()
    data = request.json
    # Cari user berdasarkan username
    user = db.query(User).filter_by(username=data['username']).first()

    # Verifikasi password menggunakan hashing
    if user and check_password_hash(user.password, data['password']):
        # Buat token JWT dengan informasi user dan waktu kedaluwarsa
        token = jwt.encode({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({
            "token": token,
            "role" : user.role,
            "id": user.id})
    return jsonify({"message": "Login gagal"}), 401