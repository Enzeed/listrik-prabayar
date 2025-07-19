"""
crud.py

Modul yang berisi fungsi-fungsi utama untuk mengelola data pemakaian listrik
dalam aplikasi pembayaran listrik pascabayar.

Fungsi CRUD meliputi:
- Menambahkan data pemakaian
- Mengambil histori pemakaian
- Memperbarui data pemakaian
- Menghapus data pemakaian
"""

from sqlalchemy.orm import joinedload
from utils import pemakaian_to_dict
from database import SessionLocal
from models import Pemakaian, User

# Tarif tetap per KWH
TARIF_PER_KWH = 1500


def create_pemakaian(user_id, bulan, tahun, kwh):
    """
    Membuat data pemakaian listrik baru untuk seorang pengguna.

    Args:
        user_id (int): ID pengguna.
        bulan (str): Bulan pemakaian.
        tahun (str): Tahun pemakaian.
        kwh (int): Jumlah KWH yang digunakan.

    Returns:
        dict: Data pemakaian yang berhasil dibuat, dalam format dictionary.
    """
    db = SessionLocal()
    total = kwh * TARIF_PER_KWH

    # buat data pemakaian
    pemakaian = Pemakaian(user_id=user_id, bulan=bulan, tahun=tahun, kwh=kwh, total_tagihan=total)
    db.add(pemakaian)
    db.commit()
    db.refresh(pemakaian)

    # Eager load relasi user untuk menghindari lazy load error
    pemakaian = db.query(Pemakaian)\
                  .options(joinedload(Pemakaian.user))\
                  .get(pemakaian.id)

    # Konversi ke dict sebelum close session
    result = {
        "id": pemakaian.id,
        "user_id": pemakaian.user_id,
        "username": pemakaian.user.username if pemakaian.user else None,
        "bulan": pemakaian.bulan,
        "tahun": pemakaian.tahun,
        "kwh": pemakaian.kwh,
        "total_tagihan": pemakaian.total_tagihan
    }

    db.close()
    return result


def get_histori_pemakaian(user_id=None):
    """
    Mengambil histori pemakaian listrik.

    Args:
        user_id (int, optional): ID pengguna. Jika None, kembalikan semua data (untuk admin).

    Returns:
        list: Daftar objek `Pemakaian` dari database.
    """
    db = SessionLocal()
    if user_id:
        data = db.query(Pemakaian).filter_by(user_id=user_id).all()
    else:
        data = db.query(Pemakaian).all()
    db.close()
    return data


def update_pemakaian(pemakaian_id, kwh):
    """
    Memperbarui data KWH dan total tagihan berdasarkan ID pemakaian.

    Args:
        pemakaian_id (int): ID data pemakaian yang akan diubah.
        kwh (int): Nilai KWH baru.

    Returns:
        dict or None: Data pemakaian yang telah diperbarui, atau None jika tidak ditemukan.
    """
    db = SessionLocal()

    # Ambil dengan joinedload agar relasi user ikut dimuat
    pemakaian = db.query(Pemakaian)\
                  .options(joinedload(Pemakaian.user))\
                  .get(pemakaian_id)

    result = None
    if pemakaian:
        pemakaian.kwh = kwh
        pemakaian.total_tagihan = kwh * TARIF_PER_KWH
        db.commit()
        db.refresh(pemakaian)

        # Konversi ke dict SEBELUM session ditutup!
        result = {
            "id": pemakaian.id,
            "user_id": pemakaian.user_id,
            "username": pemakaian.user.username if pemakaian.user else None,
            "bulan": pemakaian.bulan,
            "tahun": pemakaian.tahun,
            "kwh": pemakaian.kwh,
            "total_tagihan": pemakaian.total_tagihan
        }

    db.close()
    return result


def delete_pemakaian(pemakaian_id):
    """
    Menghapus data pemakaian listrik berdasarkan ID.

    Args:
        pemakaian_id (int): ID pemakaian yang akan dihapus.

    Returns:
        None
    """
    db = SessionLocal()
    pemakaian = db.query(Pemakaian).get(pemakaian_id)
    if pemakaian:
        db.delete(pemakaian)
        db.commit()
    db.close()
