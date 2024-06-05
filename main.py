import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import home
import prediksi
import about

# Set the page configuration as the first Streamlit command
st.set_page_config(
    page_title="Otatop Prediction",
)

# Load environment variables
load_dotenv()

def main():
    # Langsung menampilkan halaman utama jika pengguna sudah login
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        halaman_utama()
    else:
        # Tampilkan halaman utama tanpa perlu login jika pengguna belum masuk
        halaman_utama()

# Retrieve the analytics tag from the environment variables
analytics_tag = os.getenv('analytics_tag')

st.markdown(
    f"""
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={analytics_tag}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{analytics_tag}');
    </script>
    """, unsafe_allow_html=True
)

# Function untuk menambahkan background image dengan CSS
def set_background_image(image_path):
    bg_css = f"""
    <style>
    .reportview-container {{
        background: url("{image_path}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Panggil fungsi untuk menetapkan background image
set_background_image('otatop_logo.JPEG')

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            st.sidebar.title("Menu")
            app = option_menu(
                menu_title='',
                options=['Home', 'Prediksi', 'About'],
                icons=['house-fill', 'graph-up', 'info-circle-fill'],
                menu_icon='list',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

            # Tambahkan tombol logout di sidebar
            if st.sidebar.button("Logout"):
                st.session_state.logged_in = False
                # Log the event
                print("User has logged out.")
                st.experimental_rerun()  # Refresh halaman untuk kembali ke login

        if app == "Home":
            home.app()
        elif app == "Prediksi":
            prediksi.app()
        elif app == 'About':
            about.app()

# Halaman utama setelah login
def halaman_utama():
    app = MultiApp()
    app.add_app("Home", home.app)
    app.add_app("Prediksi", prediksi.app)
    app.add_app("About", about.app)
    app.run()

if __name__ == "__main__":
    main()
