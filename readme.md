**Aplikasi Pembayaran Listrik Pascabayar**

Aplikasi ini merupakan sistem berbasis web API (Flask) dan interface Streamlit untuk mengelola pemakaian dan tagihan listrik pelanggan secara pascabayar, dengan sistem login dan pembagian role admin dan pelanggan.

🧰 Fitur Utama

- Autentikasi login dengan token JWT
- Role-based access (admin & pelanggan)
- CRUD data pemakaian listrik
- Perhitungan tagihan otomatis berdasarkan KWH
- Interface berbasis Streamlit
- Penyimpanan data di PostgreSQL

🔧 Instalasi & Setup
1. Clone Repository
git clone [https://github.com/namauser/aplikasi-listrik.git](https://github.com/Enzeed/listrik-prabayar.git)
cd aplikasi-listrik

2. Buat Virtual Environment (Opsional tapi Disarankan)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Setup PostgreSQL
CREATE DATABASE listrik_db;
CREATE USER listrik_user WITH PASSWORD 'noufalznak09';
GRANT ALL PRIVILEGES ON DATABASE listrik_db TO listrik_user;

5. Jalankan Backend Flask API
python app.py

6. Jalankan Frontend Streamlit
streamlit run streamlit_app.py
