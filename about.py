import streamlit as st
def main():
    st.title("About Page")
    st.write("Welcome to the AboutPage.")

if __name__ == "__main__":
    main()

def app():
    st.title("About Us")

    st.markdown("<h2 style='font-size: 32px; text-align: center; color: #006aff; margin-bottom: 30px;'>Meet Our Team</h2>", unsafe_allow_html=True)

    # Informasi anggota kelompok beserta jabatannya dan pesan
    anggota_kelompok = [
        {"nama": "Ghaida' Nada Nazihah", "foto": "nada.jpg", "jabatan": "Project Manager", "pesan": "Hiduplah dengan cara bagaimana kamu ingin hidup, jika kamu tidak menyerah dari harapan dan impianmu, maka akan selalu ada akhir yang baik."},
        {"nama": "M. Irsyad Hasbadi", "foto": "irsyad.jpg", "jabatan": "Anggota Kelompok", "pesan": "Bismillah IPK 4.0"},
        {"nama": "Rama Dani Wanda Prasetyo", "foto": "rama.png", "jabatan": "Anggota Kelompok", "pesan": "Bismillah Sukses"},
        {"nama": "Alnindia Lintang Permata Putri", "foto": "lintang.jpg", "jabatan": "Anggota Kelompok", "pesan": "apapun hasilnya berangkat."},
        {"nama": "Ananda Adi Saputra", "foto": "adi.jpg", "jabatan": "Anggota Kelompok", "pesan": "Semoga setiap momen membawa kita lebih dekat kepada impian kita.."},
        # Tambahkan anggota kelompok lain di sini
    ]

    # Menampilkan nama, foto, jabatan, dan pesan anggota kelompok
    for anggota in anggota_kelompok:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(anggota['foto'], width=100)
        with col2:
            st.markdown(f"### {anggota['nama']}")
            st.markdown(f"**{anggota['jabatan']}**")
            st.markdown(f"*{anggota['pesan']}*")
        st.markdown("---")

# Menjalankan aplikasi
if __name__ == "__main__":
    app()
