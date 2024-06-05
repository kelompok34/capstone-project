import streamlit as st
import os
import base64
import pandas as pd
import matplotlib.pyplot as plt

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def app():
    # Menampilkan header dengan logo
    logo_path = "otatop_logo.jpeg"
    if os.path.exists(logo_path):
        logo_base64 = get_base64_of_bin_file(logo_path)
        st.markdown(f'''
            <h1 style="display: flex; align-items: center;">
                <img src="data:image/jpeg;base64,{logo_base64}" style="margin-right: 10px; width: 50px; height: 50px;" />
                Otatop Prediction
            </h1>
        ''', unsafe_allow_html=True)
    else:
        st.header("Otatop Prediction")

    # Tambahkan CSS untuk background image
    page_bg_img = f'''
    <style>
    body {{
        background-image: url("data:image/jpeg;base64,{logo_base64}");
        background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    with st.expander("Apa itu Otatop Prediction?"):
        st.markdown("""
        Otatop Prediction adalah aplikasi berbasis web yang dirancang untuk membantu dalam mengidentifikasi dan mendiagnosis penyakit pada kentang melalui gambar. Dengan menggunakan teknologi pembelajaran mesin dan jaringan saraf tiruan, aplikasi ini dapat memprediksi kondisi kentang dan memberikan informasi tentang kualitas serta penyakit yang mungkin ada pada kentang tersebut.
        """)


    with st.expander("Tujuan Dibuatnya Otatop"):
        st.markdown("""
        Dalam industri manufaktur khususnya pada sektor pertanian dan pengolahan makanan, kualitas bahan baku adalah salah satu faktor kunci yang mempengaruhi hasil akhir produk. Kentang, sebagai salah satu komoditas utama dalam industri ini, seringkali rentan terhadap berbagai penyakit yang dapat mempengaruhi kualitas dan kuantitas hasil panen.
        """)

    with st.expander("Our Goals"):
        st.markdown("""
        1. **Peningkatan Kualitas Produk**: Dengan kemampuan untuk mendeteksi penyakit sejak dini, Otatop Prediction membantu petani dan produsen untuk memilah kentang berkualitas tinggi dari yang terinfeksi penyakit.
        2. **Efisiensi Produksi**: Mengurangi waktu dan biaya yang dihabiskan untuk inspeksi manual dan pengolahan kentang yang terinfeksi.
        3. **Keamanan Pangan**: Memastikan bahwa hanya kentang sehat yang masuk ke dalam rantai pasokan, sehingga meningkatkan standar keamanan pangan.
        4. **Data-Driven Decision Making**: Dengan analisis data yang akurat, petani dan produsen dapat membuat keputusan yang lebih baik mengenai pengelolaan tanaman dan proses produksi.
        """)

    with st.expander("Teknologi di Balik Otatop Prediction"):
        st.markdown("""
        Aplikasi ini menggunakan model **ResNet-50**, salah satu arsitektur jaringan saraf tiruan yang paling populer untuk tugas pengenalan gambar. Model ini telah dilatih dengan dataset gambar kentang yang mencakup berbagai kondisi dan penyakit, sehingga mampu melakukan prediksi dengan akurasi tinggi.

        Selain itu, kami juga menggunakan framework **Keras** untuk membangun dan melatih model Convolutional Neural Network (CNN). Keras adalah salah satu framework deep learning yang powerful dan mudah digunakan, menyediakan berbagai API yang memudahkan dalam membangun, melatih, dan mengevaluasi model. Model Keras ini juga dilatih dengan dataset gambar kentang untuk meningkatkan kemampuan prediksi.
        """)

        # Membaca hasil pelatihan dari file CSV ResNet-50
        csv_path_resnet = "training_results.csv"
        
        if st.button("Lihat Hasil Training ResNet-50"):
            if os.path.exists(csv_path_resnet):
                df_resnet = pd.read_csv(csv_path_resnet)

                # Memastikan kolom yang dibutuhkan ada
                if all(col in df_resnet.columns for col in ["epoch", "train_accuracy", "val_accuracy", "train_loss", "val_loss"]):
                    epochs = df_resnet['epoch']
                    train_accuracies = df_resnet['train_accuracy']
                    val_accuracies = df_resnet['val_accuracy']
                    train_losses = df_resnet['train_loss']
                    val_losses = df_resnet['val_loss']

                    # Plotting akurasi dan loss pelatihan dan validasi
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

                    # Plot akurasi
                    ax1.plot(epochs, train_accuracies, 'b', label='Akurasi Pelatihan')
                    ax1.plot(epochs, val_accuracies, 'r', label='Akurasi Validasi')
                    ax1.set_title('Akurasi Pelatihan dan Validasi')
                    ax1.set_xlabel('Epochs')
                    ax1.set_ylabel('Akurasi')
                    ax1.legend()

                    # Plot loss
                    ax2.plot(epochs, train_losses, 'b', label='Loss Pelatihan')
                    ax2.plot(epochs, val_losses, 'r', label='Loss Validasi')
                    ax2.set_title('Loss Pelatihan dan Validasi')
                    ax2.set_xlabel('Epochs')
                    ax2.set_ylabel('Loss')
                    ax2.legend()

                    # Menampilkan plot di aplikasi Streamlit
                    st.pyplot(fig)
                else:
                    st.error("File CSV tidak memiliki kolom yang dibutuhkan.")
            else:
                st.error(f"File CSV tidak ditemukan di {csv_path_resnet}")

        # Membaca hasil pelatihan dari file CSV Keras
        csv_path_keras = "keras_training_results.csv"
        
        if st.button("Lihat Hasil Training Keras"):
            if os.path.exists(csv_path_keras):
                df_keras = pd.read_csv(csv_path_keras)

                # Memastikan kolom yang dibutuhkan ada
                if all(col in df_keras.columns for col in ["loss", "accuracy", "val_loss", "val_accuracy"]):
                    epochs = range(len(df_keras))
                    train_accuracies = df_keras['accuracy']
                    val_accuracies = df_keras['val_accuracy']
                    train_losses = df_keras['loss']
                    val_losses = df_keras['val_loss']

                    # Plotting akurasi dan loss pelatihan dan validasi
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

                    # Plot akurasi
                    ax1.plot(epochs, train_accuracies, 'b', label='Akurasi Pelatihan')
                    ax1.plot(epochs, val_accuracies, 'r', label='Akurasi Validasi')
                    ax1.set_title('Akurasi Pelatihan dan Validasi')
                    ax1.set_xlabel('Epochs')
                    ax1.set_ylabel('Akurasi')
                    ax1.legend()

                    # Plot loss
                    ax2.plot(epochs, train_losses, 'b', label='Loss Pelatihan')
                    ax2.plot(epochs, val_losses, 'r', label='Loss Validasi')
                    ax2.set_title('Loss Pelatihan dan Validasi')
                    ax2.set_xlabel('Epochs')
                    ax2.set_ylabel('Loss')
                    ax2.legend()

                    # Menampilkan plot di aplikasi Streamlit
                    st.pyplot(fig)
                else:
                    st.error("File CSV tidak memiliki kolom yang dibutuhkan.")
            else:
                st.error(f"File CSV tidak ditemukan di {csv_path_keras}")

    with st.expander("Cara Menggunakan Otatop Prediction"):
        st.markdown("""
        1. **Analisis dan Hasil**: Model bakal proses gambar dan tunjukkan hasil prediksi tentang kondisi kentang, termasuk jenis penyakit dan probabilitasnya berdasarkan model yang kamu pilih.
        2. **Tindakan Lanjutan**: Berdasarkan hasil analisis, kamu bisa ambil tindakan yang perlu untuk pastiin kualitas dan kesehatan kentang sebelum melanjutkan ke tahap produksi berikutnya.

        Kami berharap Otatop Prediction dapat menjadi alat yang bermanfaat bagi industri manufaktur pertanian dan pengolahan makanan, membantu meningkatkan kualitas produk dan efisiensi produksi.
        """)

# Menjalankan aplikasi
if __name__ == "__main__":
    app()

