"""
utils.py

Modul utilitas untuk aplikasi pembayaran listrik pascabayar.

Fungsi:
- token_required: Dekorator untuk validasi token JWT pada endpoint.
- pemakaian_to_dict: Fungsi helper untuk mengubah objek Pemakaian menjadi dict.
"""

import jwt
from flask import request, jsonify
SECRET_KEY = "rahasia"

def token_required(f):
    """
    Dekorator Flask untuk memvalidasi token JWT pada setiap permintaan.

    Menambahkan `user_data` ke dalam objek `request` jika token valid.

    Args:
        f (function): Fungsi route yang akan dihias.

    Returns:
        function: Fungsi yang dibungkus dengan validasi token.
    """
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token diperlukan"}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_data = data
        except:
            return jsonify({"message": "Token tidak valid"}), 403
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

def pemakaian_to_dict(pemakaian):
    """
    Mengubah objek `Pemakaian` menjadi dictionary agar bisa di-serialisasi ke JSON.

    Args:
        pemakaian (Pemakaian): Objek pemakaian dari database SQLAlchemy.

    Returns:
        dict: Representasi dictionary dari data pemakaian.
    """
    return {
        "id": pemakaian.id,
        "user_id": pemakaian.user_id,
        "username": pemakaian.user.username if pemakaian.user else None,
        "bulan": pemakaian.bulan,
        "tahun": pemakaian.tahun,
        "kwh": pemakaian.kwh,
        "total_tagihan": pemakaian.total_tagihan
    }