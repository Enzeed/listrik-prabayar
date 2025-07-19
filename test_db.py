from sqlalchemy import create_engine

DATABASE_URL = "postgresql://listrik_user:noufalznak09@localhost:5432/listrik_db"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("✅ Koneksi berhasil")
except Exception as e:
    print("❌ Gagal konek:", e)
