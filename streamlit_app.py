import streamlit as st
import requests
import pandas as pd
import time

BASE_URL = "http://localhost:5000"

if "token" not in st.session_state:
    st.session_state.token = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# Login
if not st.session_state.token:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(BASE_URL + "/login", json={"username": username, "password": password})
        if res.status_code == 200:
            hasil = res.json()
            st.session_state.token = hasil["token"]
            st.session_state.role = hasil["role"]
            st.rerun()
        else:
            st.error("Login gagal")
    st.stop()


# Menu based on role
st.title("Aplikasi Pembayaran Listrik")
if st.session_state.role == "admin":
    menu = st.sidebar.radio("Menu", ["Input Pemakaian", "Lihat & Kelola Tagihan", "Logout"])
else:
    menu = st.sidebar.radio("Menu", ["Input Pemakaian", "Lihat Tagihan", "Logout"])

headers = {"Authorization": st.session_state.token}

# Imput Pemakaian
if menu == "Input Pemakaian":
    bulan = st.selectbox("Bulan", ["Januari", "Februari", "Maret", "April",
                                   "Mei", "Juni", "Juli", "Agustus", "September",
                                   "Oktober", "November", "Desember"])
    tahun = st.number_input("Tahun", 2020, 2030, step=1)
    kwh = st.number_input("Pemakaian KWH", 0.0)
    if st.button("Kirim"):
        res = requests.post(BASE_URL + "/pemakaian", json={"bulan": bulan, "tahun": tahun, "kwh": kwh}, headers=headers)
        if res.status_code == 200:
            st.success("Data tersimpan")
        else:
            st.error(f"Gagal! Status: {res.status_code}, Pesan: {res.text}")

# Lihat dan kelola tagihan
elif "Lihat" in menu:
    start_time = time.time()
    res = requests.get(BASE_URL + "/pemakaian", headers=headers)
    elapsed = time.time() - start_time

    if res.status_code == 200:
        data = res.json()
        df = pd.DataFrame(data)
        df["tahun"] = df["tahun"].astype(str)
        st.write(f"⏱️ Waktu akses data: {elapsed:.2f} detik")

        for item in data:
            with st.expander(f"{item['bulan']} {item['tahun']} - {item['kwh']} KWH"):
                if st.session_state.role == "admin":
                    # Form edit
                    new_kwh = st.number_input("Update KWH", value=item["kwh"], key=f"kwh_{item['id']}")
                    if st.button("Simpan Perubahan", key=f"edit_{item['id']}"):
                        update_res = requests.put(BASE_URL + f"/pemakaian/{item['id']}",
                                                  json={"kwh": new_kwh}, headers=headers)
                        if update_res.status_code == 200:
                            st.success("Berhasil diupdate")
                            st.rerun()
                        else:
                            st.error("Gagal update")
                    
                    # Tombol hapus
                    if st.button("Hapus", key=f"delete_{item['id']}"):
                        del_res = requests.delete(BASE_URL + f"/pemakaian/{item['id']}", headers=headers)
                        if del_res.status_code == 200:
                            st.warning("Data dihapus")
                            st.rerun()
                        else:
                            st.error("Gagal menghapus data")
                else:
                    # Pelanggan hanya bisa lihat
                    st.write(f"Tagihan: {item['kwh'] * 1500} Rupiah")

    else:
        st.error("Gagal memuat data")


elif menu == "Logout":
    st.session_state.token = ""
    st.session_state.role = ""
    st.success("Berhasil logout")
    st.rerun()
    