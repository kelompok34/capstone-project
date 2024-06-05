import streamlit as st
import sqlite3
import base64
import os
from main import halaman_utama  # Mengimpor fungsi dari main.py

def buat_koneksi():
    conn = sqlite3.connect('user.db')
    return conn

def buat_tabel():
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


# CSS khusus untuk mengatur gambar latar belakang
page_bg_img = '''
<style>
.stApp {{
  background-image: url("data:image/png;base64,{img_base64}");
  background-size: cover;
}}
</style>
'''

# Fungsi untuk membaca gambar dan mengonversinya ke base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Tentukan jalur ke gambar Anda, mengganti backslash dengan forward slash
img_path = 'kentang.jpg'

# Pastikan file ada di lokasi yang ditentukan
if os.path.exists(img_path):
    img_base64 = get_base64_of_bin_file(img_path)
    # Sisipkan CSS ke dalam aplikasi Streamlit
    st.markdown(page_bg_img.format(img_base64=img_base64), unsafe_allow_html=True)
else:
    st.error("File gambar tidak ditemukan. Pastikan jalur file benar.")


def login():
    st.subheader("Otatop Login")

    input_username = st.text_input("Username")
    input_password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = buat_koneksi()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (input_username, input_password))
        hasil = cursor.fetchone()
        conn.close()
        if hasil:
            st.success("Login Berhasil!")
            st.session_state.logged_in = True
            st.session_state.username = input_username
            st.experimental_rerun()  # Rerun aplikasi untuk memperbarui tampilan
        else:
            st.error("Username atau password salah")

def register():
    st.subheader("Otatop Register")

    username_baru = st.text_input("Username (Maksimal 15 karakter)")
    password_baru = st.text_input("Password (Maksimal 15 karakter)", type="password")
    konfirmasi_password = st.text_input("Konfirmasi Password (Maksimal 15 karakter)", type="password")

    if st.button("Register"):
        # Validasi panjang karakter username dan password
        if len(username_baru) > 15 or len(password_baru) > 15:
            st.error("Username dan password tidak boleh lebih dari 15 karakter.")
        elif password_baru == konfirmasi_password:
            try:
                conn = buat_koneksi()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username_baru, password_baru))
                conn.commit()
                conn.close()
                st.success("Registrasi Berhasil! Silakan login.")
            except sqlite3.IntegrityError:
                st.error("Username sudah ada. Silakan pilih username lain.")
        else:
            st.error("Password tidak cocok. Silakan coba lagi.")


def main():
    buat_tabel()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        halaman_utama()  # Panggil fungsi dari main.py
    else:
        menu = ["Login", "Register"]
        pilihan = st.sidebar.selectbox("Menu", menu)

        if pilihan == "Login":
            login()
        elif pilihan == "Register":
            register()

if __name__ == "__main__":
    main()
