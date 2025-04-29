import streamlit as st


def estimate_requirements(num_pages, avg_image_size, avg_video_size_per_min, avg_video_duration, video_presence, num_users, cdn, safety_margin_percent):

    avg_video_size = avg_video_size_per_min * avg_video_duration * video_presence  # in MB
    print(avg_video_size_per_min)

    # Calculate total content size
    total_images_size = num_pages * avg_image_size  # in MB
    total_video_size = num_pages * avg_video_size  # in MB

    # Total content size (in MB)
    total_content_size = total_images_size + total_video_size

    total_ram_required = 1024 + num_users * 8
    if cdn:
        total_ram_required /= 2
    total_disk_space_required = total_content_size  # in MB

    # Convert to GB for better readability
    total_ram_required_gb = total_ram_required / 1024 * safety_margin_percent
    total_disk_space_required_gb = total_disk_space_required / \
        1024 * safety_margin_percent

    return total_disk_space_required_gb, total_ram_required_gb


image_quality_options = {
    'Bassa (250 KB)': 0.25,
    'Media (500 KB)': 0.5,
    'Alta (1 MB)': 1.0,
    'Molto Alta (2 MB)': 2.0
}

video_quality_options = {
    'Bassa (480p)': 11,
    'Media (720p)': 23,
    'Alta (1080p)': 50,
    'Molto Alta (4K)': 250
}

bit_rate_options = {
    'Bassa (480p)': 0.75,
    'Media (720p)': 2.25,
    'Alta (1080p)': 4.5,
    'Molto Alta (4K)': 20
}


def run():
    # Streamlit Interface
    st.title('Stima Requisiti Manuale Digitale')

    num_pages = st.number_input('Numero di pagine', min_value=0, value=50)

    image_quality = st.selectbox(
        'Dimensione immagini media',
        list(image_quality_options), index=1, help='Seleziona la qualità delle immagini per il calcolo della dimensione media.'
    )

    avg_image_size = image_quality_options.get(
        image_quality, 0.5)  # Default to 'Media' if not found

    video_quality = st.selectbox(
        'Qualità video media',
        list(video_quality_options), index=2, help='Seleziona la qualità dei video per il calcolo della dimensione media.'
    )

    avg_video_size_per_minute = video_quality_options.get(
        video_quality, 23)  # Default to 'Media' if not found

    avg_video_duration = st.number_input(
        'Durata media video (minuti)', min_value=0, value=15)

    video_rate_per_page = st.slider(
        'Pagine contenenti video (%)', min_value=0, max_value=100, value=50)
    video_rate_per_page = video_rate_per_page / 100

    num_users = st.number_input('Numero di utenti concorrenti', min_value=0, value=100)

    cdn = st.checkbox('CDN (Comporta costi aggiuntivi)', value=False)

    safety_margin_percent = st.slider(
        'Margine di sicurezza (%)', min_value=0, max_value=100, value=30)
    safety_margin_percent = 1 + safety_margin_percent / 100

    # Calculate and display the results
    if st.button('Calcola Requisiti'):
        total_disk_space, total_ram = estimate_requirements(
            num_pages, avg_image_size, avg_video_size_per_minute, avg_video_duration, video_rate_per_page, num_users, cdn, safety_margin_percent)

        bandwidth = bit_rate_options[video_quality] * num_users / 1000
        bandwidth *= safety_margin_percent
        if video_rate_per_page <= .3:
            bandwidth *= video_rate_per_page * 1.3
        bandwidth += .1

        st.subheader('Risorse Raccomandate:')
        st.write(f"Spazio su disco: {total_disk_space:.2f} GB")
        st.write(f"Memoria RAM: {total_ram:.2f} GB")
        if (not cdn):
            st.write(f"Larghezza di banda: {bandwidth:.2f} Gbps")


run()
