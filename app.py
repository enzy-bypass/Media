import streamlit as st
import os
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip

# 1. Cấu hình giao diện chuẩn Premium cho di động
st.set_page_config(page_title="Media Pro", page_icon="🎵", layout="centered")

# 2. Nhúng mã CSS để thay đổi hoàn toàn giao diện mặc định sang giao diện Cao cấp
st.markdown("""
<style>
    /* Nền ứng dụng mềm mại hơn */
    .main {
        background-color: #f9fbfd;
    }
    
    /* Thiết kế tiêu đề Gradient chuyển màu */
    .premium-title {
        background: linear-gradient(135deg, #ff007f 0%, #764ba2 50%, #4a00e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 24pt !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 5px;
    }
    .premium-sub {
        text-align: center;
        color: #6c757d;
        font-size: 10pt;
        margin-bottom: 25px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Thiết kế các Khối tính năng (Card) rõ dòng, gọn gàng */
    .feature-card {
        background: #ffffff;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        border-left: 5px solid #764ba2; /* Vạch kẻ tím sang trọng định hình dòng */
    }
    
    .feature-card-2 {
        background: #ffffff;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        border-left: 5px solid #ff007f; /* Vạch kẻ hồng trẻ trung */
    }
    
    /* Giao diện nút bấm chức năng (Xử lý) màu Gradient Tím-Xanh */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 11pt !important;
        width: 100% !important;
        box-shadow: 0 4px 10px rgba(118, 75, 162, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:active {
        transform: scale(0.98) !important;
    }
    
    /* Giao diện nút TẢI FILE VỀ MÁY màu Xanh Lá cực nổi bật */
    div.stDownloadButton > button:first-child {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 12pt !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(56, 239, 125, 0.4) !important;
        animation: pulse 2s infinite;
    }
    
    /* Giới hạn kích thước các ô nhập liệu cho vừa vặn màn hình điện thoại */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Phần nội dung hiển thị ứng dụng
st.markdown('<p class="premium-title">🎵 MEDIA PREMIUM</p>', unsafe_allow_html=True)
st.markdown('<p class="premium-sub">Hệ thống tải nhạc & Đổi đuôi cá nhân</p>', unsafe_allow_html=True)

SAVE_DIR = "downloads"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- KHỐI 1: TẢI TỪ LINK ---
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
st.subheader("⚡ Tải nhạc & Video từ Link")

url = st.text_input("Dán link (YouTube, TikTok, FB...) vào đây:", placeholder="https://...")
format_type = st.radio("Chọn định dạng đầu ra:", ("Tải MP3 (Chỉ lấy nhạc)", "Tải MP4 (Video đầy đủ)"))

if st.button("🚀 Bắt Đầu Xử Lý Link"):
    if not url:
        st.warning("Vui lòng dán đường link vào trước!")
    else:
        with st.spinner("Đang tải dữ liệu từ máy chủ..."):
            try:
                outtmpl = os.path.join(SAVE_DIR, '%(title)s.%(ext)s')
                ydl_opts = {
                    'outtmpl': outtmpl,
                    'extractor_args': {'youtube': {'player_client': ['ios', 'android', 'mweb']}},
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1'
                    },
                    'nocheckcertificate': True
                }
                
                if format_type == "Tải MP3 (Chỉ lấy nhạc)":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    })
                else:
                    ydl_opts.update({
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    })
                    
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if format_type == "Tải MP3 (Chỉ lấy nhạc)":
                        filename = os.path.splitext(filename)[0] + '.mp3'
                    
                    with open(filename, "rb") as f:
                        st.success("🎉 Hoàn thành xuất sắc!")
                        st.download_button(
                            label="📥 LƯU FILE VỀ ĐIỆN THOẠI NGAY",
                            data=f,
                            file_name=os.path.basename(filename),
                            mime="audio/mpeg" if format_type == "Tải MP3 (Chỉ lấy nhạc)" else "video/mp4"
                        )
            except Exception as e:
                st.error(f"Lỗi: {str(e)}")
st.markdown('</div>', unsafe_allow_html=True) # Đóng khối 1


# --- KHỐI 2: ĐỔI ĐUÔI MP4 SANG MP3 ---
st.markdown('<div class="feature-card-2">', unsafe_allow_html=True)
st.subheader("🔄 Bộ chuyển đổi MP4 sang MP3")

uploaded_file = st.file_uploader("Chọn video từ máy của bạn:", type=["mp4"])

if uploaded_file is not None:
    if st.button("🎵 Tiến Hành Tách Nhạc"):
        with st.spinner("Đang tách âm thanh, vui lòng đợi..."):
            try:
                input_path = os.path.join(SAVE_DIR, uploaded_file.name)
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                output_filename = os.path.splitext(uploaded_file.name)[0] + ".mp3"
                output_path = os.path.join(SAVE_DIR, output_filename)
                
                video = VideoFileClip(input_path)
                video.audio.write_audiofile(output_path)
                video.close()
                
                with open(output_path, "rb") as f:
                    st.success("🎉 Tách nhạc thành công!")
                    st.download_button(
                        label="📥 LƯU FILE MP3 VỀ MÁY",
                        data=f,
                        file_name=output_filename,
                        mime="audio/mpeg"
                    )
                
                os.remove(input_path)
                os.remove(output_path)
                
            except Exception as e:
                st.error(f"Lỗi chuyển đổi: {str(e)}")
st.markdown('</div>', unsafe_allow_html
