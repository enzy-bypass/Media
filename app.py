import streamlit as st
import os
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip

# Cấu hình giao diện App gọn gàng trên điện thoại
st.set_page_config(page_title="App Tải & Đổi Nhạc", page_icon="🎵", layout="centered")

st.title("🎵 App Tải & Chuyển Đổi Media")
st.caption("Ứng dụng cá nhân của riêng bạn - Không quảng cáo")

# Tạo thư mục lưu tạm trên Cloud
SAVE_DIR = "downloads"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- TÍNH NĂNG 1 & 3: TẢI MP3 / MP4 TỪ LINK ---
st.header("1. Tải từ Đường Dẫn (Link)")
url = st.text_input("Dán link video (YouTube, TikTok, FB...) vào đây:", placeholder="https://...")
format_type = st.radio("Bạn muốn tải định dạng nào?", ("Tải MP3 (Chỉ lấy nhạc)", "Tải MP4 (Video đầy đủ)"))

if st.button("🚀 Bắt Đầu Tải Từ Link"):
    if not url:
        st.warning("Vui lòng dán đường link vào trước!")
    else:
        with st.spinner("Hệ thống đang tải và xử lý dữ liệu, vui lòng đợi..."):
            try:
                outtmpl = os.path.join(SAVE_DIR, '%(title)s.%(ext)s')
                ydl_opts = {'outtmpl': outtmpl}
                
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
                        st.success("🎉 Đã xử lý xong!")
                        st.download_button(
                            label="📥 BẤM VÀO ĐÂY ĐỂ LƯU FILE VỀ MÁY",
                            data=f,
                            file_name=os.path.basename(filename),
                            mime="audio/mpeg" if format_type == "Tải MP3 (Chỉ lấy nhạc)" else "video/mp4"
                        )
            except Exception as e:
                st.error(f"Lỗi hệ thống: {str(e)}")

st.markdown("---")

# --- TÍNH NĂNG 2: CHUYỂN FILE MP4 SANG MP3 ---
st.header("2. Đổi đuôi MP4 sang MP3")
uploaded_file = st.file_uploader("Chọn file video .mp4 từ thư viện điện thoại:", type=["mp4"])

if uploaded_file is not None:
    if st.button("🎵 Bắt Đầu Tách Nhạc Sang MP3"):
        with st.spinner("Đang tách âm thanh khỏi video..."):
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
                    st.success("🎉 Chuyển đổi thành công!")
                    st.download_button(
                        label="📥 BẤM VÀO ĐÂY ĐỂ LƯU FILE MP3",
                        data=f,
                        file_name=output_filename,
                        mime="audio/mpeg"
                    )
                
                os.remove(input_path)
                os.remove(output_path)
                
            except Exception as e:
                st.error(f"Lỗi chuyển đổi: {str(e)}")
                  
