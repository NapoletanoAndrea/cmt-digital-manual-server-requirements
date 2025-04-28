import streamlit as st


def estimate_manual_size(
    num_images, avg_image_size,
    num_videos, avg_video_size,
    num_audio, avg_audio_size,
    num_pdfs, avg_pdf_size,
    safety_margin_percent
):
    total_images_size = num_images * avg_image_size
    total_videos_size = num_videos * avg_video_size
    total_audio_size = num_audio * avg_audio_size
    total_pdfs_size = num_pdfs * avg_pdf_size

    total_size_mb = total_images_size + total_videos_size + total_audio_size + total_pdfs_size
    total_size_with_margin_mb = total_size_mb * (1 + safety_margin_percent / 100)

    return total_size_mb, total_size_with_margin_mb


def run():

    # Streamlit UI
    st.title('📚 Requisiti Manuale Digitale')

    num_pages = st.number_input('Numero di pagine', min_value=0, value=50)

    image_quality = st.selectbox(
        'Qualità delle Immagini',
        ('Bassa (250 KB)', 'Media (500 KB)', 'Alta (1 MB)', 'Molto Alta (2 MB)'), index=1, help='Seleziona la qualità delle immagini per il calcolo della dimensione media.'
    )

    col1, col2 = st.columns(2)

    with col1:
        num_images = st.number_input('Number of Images', min_value=0, value=100)
        avg_image_size = st.number_input('Average Image Size (MB)', min_value=0.0, value=2.0)

        num_videos = st.number_input('Number of Videos', min_value=0, value=5)
        avg_video_size = st.number_input('Average Video Size (MB)', min_value=0.0, value=50.0)

    with col2:
        num_audio = st.number_input('Number of Audio Files', min_value=0, value=3)
        avg_audio_size = st.number_input('Average Audio Size (MB)', min_value=0.0, value=5.0)

        num_pdfs = st.number_input('Number of PDFs', min_value=0, value=1)
        avg_pdf_size = st.number_input('Average PDF Size (MB)', min_value=0.0, value=10.0)

    safety_margin_percent = st.slider('Safety Margin (%)', min_value=0, max_value=100, value=30)

    if st.button('Estimate Manual Size'):
        size_mb, size_with_margin_mb = estimate_manual_size(
            num_images, avg_image_size,
            num_videos, avg_video_size,
            num_audio, avg_audio_size,
            num_pdfs, avg_pdf_size,
            safety_margin_percent
        )

        size_gb = size_mb / 1024
        size_with_margin_gb = size_with_margin_mb / 1024

        st.success('✅ Size Estimation Completed!')
        st.subheader('Manual Size Estimation')
        st.write(f"**Raw Content Size:** {size_mb:.2f} MB ({size_gb:.2f} GB)")
        st.write(
            f"**Recommended Minimum Disk Space (with {safety_margin_percent}% margin):** {size_with_margin_mb:.2f} MB ({size_with_margin_gb:.2f} GB)")


run()
