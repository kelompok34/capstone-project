import streamlit as st
import torch
from torchvision import models, transforms
from PIL import Image
import base64
import tensorflow as tf
import numpy as np


def main():
    st.title("Prediksi Page")
    st.write("Welcome to the Prediksi Page.")

if __name__ == "__main__":
    main()


def app():
    # Fungsi untuk membaca gambar sebagai base64
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # Tampilkan gambar sebagai background dengan transparansi
    def set_png_as_page_bg(png_file):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-color: rgba(255, 255, 255, 0.9);  /* Background konten */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .stApp::before {{
            content: '';
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            opacity: 70;  /* Sesuaikan dengan tingkat transparansi yang diinginkan */
            z-index: -1;
        }}
        .stContent {{
            background-color: rgba(255, 255, 255, 0.9);  /* Background konten */
            border-radius: 10px;
            padding: 20px;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

    # Panggil fungsi untuk menetapkan gambar sebagai background
    set_png_as_page_bg('otatop_logo.jpeg')

    # Definisikan class names
    class_names = {
        0: 'Black Scurf',
        1: 'Blackleg',
        2: 'Common Scab',
        3: 'Dry Rot',
        4: 'Healthy Potatoes',
        5: 'Miscellaneous',
        6: 'Pink Rot'
    }

    # Transformasi gambar untuk model PyTorch
    pytorch_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Muat model yang telah dilatih (PyTorch)
    pytorch_model = models.resnet50(pretrained=False)
    num_ftrs = pytorch_model.fc.in_features
    pytorch_model.fc = torch.nn.Linear(num_ftrs, len(class_names))
    pytorch_model.load_state_dict(torch.load('best_model.pth', map_location=torch.device('cpu')))
    pytorch_model.eval()  # Mengatur model ke mode evaluasi

    # Muat model yang telah dilatih (Keras)
    keras_model = tf.keras.models.load_model('best_keras_model.h5')

    # Fungsi untuk melakukan prediksi menggunakan model PyTorch
    def classify_potato_pytorch(image):
        image = pytorch_transform(image).unsqueeze(0)  # Tambahkan dimensi batch
        with torch.no_grad():
            output = pytorch_model(image)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            _, predicted = torch.max(probabilities, 1)
            predicted_class = class_names[predicted.item()]
            predicted_prob = probabilities[0][predicted.item()].item()
        return predicted_class, predicted_prob

    # Fungsi untuk melakukan prediksi menggunakan model Keras
    def classify_potato_keras(image):
        image = image.resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        predictions = keras_model.predict(image)
        predicted_class_idx = np.argmax(predictions, axis=1)[0]
        predicted_class = class_names[predicted_class_idx]
        predicted_prob = predictions[0][predicted_class_idx]
        return predicted_class, predicted_prob

    st.title("Otatop Prediction")
    st.write("Prediksi Kualitas Kentangmu!!")

    # Pilihan model
    model_choice = st.radio("Pilih model yang ingin digunakan:", ("ResNet (PyTorch)", "Keras"))

    # Tampilkan area untuk mengunggah gambar kentang
    uploaded_file = st.file_uploader("Unggah gambar kentang", type=['jpg', 'jpeg', 'png'])

    # Tambahkan kolom agar konten berada di tengah halaman
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        if uploaded_file is not None:
            # Baca dan tampilkan gambar kentang yang diunggah
            image = Image.open(uploaded_file)

            if model_choice == "ResNet (PyTorch)":
                predicted_class, predicted_prob = classify_potato_pytorch(image)
            else:
                predicted_class, predicted_prob = classify_potato_keras(image)

            st.write("Kelas gambar:", predicted_class)  # Tampilkan kelas gambar di atas gambar kentang
            st.image(image, caption='Gambar Kentang yang Diunggah', use_column_width=True)

            # Logika untuk menentukan keterangan kentang
            if predicted_class == 'Healthy Potatoes':
                st.write("Kentang berkualitas, tidak terkena penyakit.")
            else:
                st.write("Kentang terkena penyakit:", predicted_class)

            st.write(f"Probabilitas: {predicted_prob:.4f}")

if __name__ == "__main__":
    app()
