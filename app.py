"""
app.py

Aplikasi backend untuk Aplikasi Pembayaran Listrik Pascabayar menggunakan Flask.
Berisi route untuk mengelola data pemakaian listrik pelanggan.

Fitur:
- Tambah pemakaian (POST)
- Lihat histori pemakaian (GET)
- Ubah pemakaian (PUT)
- Hapus pemakaian (DELETE)

Author: Noufal Zaidan
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import auth_bp
from crud import create_pemakaian, get_histori_pemakaian, update_pemakaian, delete_pemakaian
from utils import token_required
from utils import pemakaian_to_dict
import time

# Inisialisasi App Flask
app = Flask(__name__)
CORS(app)

# Registrasi blueprint untuk autentikasi
app.register_blueprint(auth_bp)

@app.route("/pemakaian", methods=["POST"])
@token_required
def tambah_pemakaian():
    """
    Endpoint untuk menambahkan data pemakaian listrik.

    Returns:
        JSON response berisi data pemakaian yang berhasil ditambahkan.
    """
    try:
        data = request.json
        user_id = request.user_data["id"]

        result = create_pemakaian(user_id, data['bulan'], data['tahun'], data['kwh'])

        return jsonify(result), 200 
    except Exception as e:
        print("Error di /pemakaian POST:", e)
        return jsonify({"message": "Terjadi kesalahan", "error": str(e)}), 500

@app.route("/pemakaian", methods=["GET"])
@token_required
def lihat_histori():
    """
    Endpoint untuk melihat histori pemakaian listrik.
    Admin akan melihat seluruh data, pelanggan hanya miliknya sendiri.

    Returns:
        JSON list dari data histori pemakaian.
    """
    start = time.time()
    role = request.user_data['role']
    if role == "admin":
        histori = get_histori_pemakaian()
    else:
        histori = get_histori_pemakaian(user_id=request.user_data['id'])
    end = time.time()
    print(f"Query time: {end - start:.4f}s")
    return jsonify([{
        "id": p.id,
        "bulan": p.bulan,
        "tahun": p.tahun,
        "kwh": p.kwh,
        "total_tagihan": p.total_tagihan
    } for p in histori])

@app.route("/pemakaian/<int:id>", methods=["PUT"])
@token_required
def ubah_pemakaian(id):
    """
    Endpoint untuk mengubah data pemakaian listrik.
    Hanya admin yang memiliki akses.

    Args:
        id (int): ID pemakaian yang akan diubah.

    Returns:
        JSON response berisi data yang diperbarui atau pesan kesalahan.
    """
    try:
        if request.user_data['role'] != 'admin':
            return jsonify({"message": "Akses ditolak"}), 403

        data = request.json
        print("Data PUT diterima:", data)

        pemakaian = update_pemakaian(id, data['kwh'])
        if pemakaian:
            return jsonify(pemakaian)
        else:
            return jsonify({"message": "Data tidak ditemukan"}), 404

    except Exception as e:
        print("Error di PUT /pemakaian/<id>:", e)
        return jsonify({"message": "Terjadi kesalahan", "error": str(e)}), 500

@app.route("/pemakaian/<int:id>", methods=["DELETE"])
@token_required
def hapus_pemakaian(id):
    """
    Endpoint untuk menghapus data pemakaian listrik.
    Hanya admin yang dapat menghapus data.

    Args:
        id (int): ID pemakaian yang akan dihapus.

    Returns:
        JSON response berupa pesan berhasil dihapus atau akses ditolak.
    """
    if request.user_data['role'] != 'admin':
        return jsonify({"message": "Akses ditolak"}), 403
    delete_pemakaian(id)
    return jsonify({"message": "Dihapus"})

if __name__ == "__main__":
    app.run(debug=True)