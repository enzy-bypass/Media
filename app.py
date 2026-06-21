import streamlit as st
import os
from utils import download_media, convert_mp4_to_mp3

st.set_page_config(page_title="Media Pro", page_icon="🎵", layout="centered")

# Khởi tạo bộ nhớ tạm để lưu cấu hình cài đặt của website
if "cookie_data" not in st.session_state:
    st.session_state["cookie_data"] = ""
if "audio_quality" not in st.session_state:
    st.session_state["audio_quality"] = "192"
if "theme_color" not in st.session_state:
    st.session_state["theme_color"] = "Tím Neon"

# Bộ màu sắc chuyển đổi theo cài đặt của người dùng
color_map = {
    "Tím Neon": {"gradient": "linear-gradient(135deg, #ff007f 0%, #764ba2 50%, #4a00e0 100%)", "primary": "#764ba2"},
    "Xanh Lục Bảo": {"gradient": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)", "primary": "#11998e"},
    "Xanh Biển Sâu": {"gradient": "linear-gradient(135deg, #00c6ff 0%, #0072ff 100%)", "primary": "#0072ff"}
}
current_theme = color_map[st.session_state["theme_color"]]

# Nhúng CSS tối ưu bố cục rõ dòng, bo góc mượt mà, không bị to lấn chiếm màn hình
st.markdown(f"""
<style>
    .main {{
        background-color: #f8fafc;
    }}
    .premium-title {{
        background: {current_theme['gradient']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 21pt !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0px;
    }}
    .premium-sub {{
        text-align: center;
        color: #64748b;
        font-size: 8.5pt;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }}
    
    /* Thiết kế hộp chứa (Card) gọn gàng, phân định dòng rõ ràng, mỏng nhẹ */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-left: 5px solid {current_theme['primary']} !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04) !important;
        padding: 15px !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }}
    
    /* Thanh chuyển đổi tính năng (Tab) bo góc cao cấp */
    div[data-testid="stTabBar"] {{
        background: #ffffff;
        border-radius: 10px;
        padding: 2px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    
    /* Nút bấm chức năng */
    div.stButton > button:first-child {{
        background: {current_theme['gradient']} !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 11pt !important;
        width: 100% !important;
    }}
    
    /* Nút lưu tệp màu xanh nổi bật */
    div.stDownloadButton > button:first-child {{
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 11pt !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(56, 239, 125, 0.2) !important;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="premium-title">🎵 MEDIA PREMIUM PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="premium-sub">Hệ thống xử lý media đa nền tảng thế hệ mới</p>', unsafe_allow_html=True)

# 💡 BỘ CẤU TRÚC TAB MỚI: Cực kỳ gọn gàng, bấm chọn nhanh chóng không chiếm diện tích
tab1, tab2, tab3 = st.tabs(["📥 Tải Từ Link", "🔄 Đổi Đuôi Tệp", "⚙️ Cài Đặt Website"])

# --- TAB 1: TẢI TỪ LINK ---
with tab1:
    with st.container(border=True):
        st.subheader("⚡ Tải nhạc & Video từ Link")
        url = st.text_input("Dán link (YouTube, TikTok, FB...):", placeholder="https://...", key="input_url")
        choice = st.radio("Định dạng xuất ra:", ("Tải nhạc MP3", "Tải video MP4"), key="input_format")
        
        format_type = "mp3" if choice == "Tải nhạc MP3" else "mp4"
        
        if st.button("🚀 Kích Hoạt Tải", key="btn_download"):
            if not url:
                st.warning("Vui lòng dán đường link vào trước!")
            else:
                with st.spinner("Đang định tuyến luồng tải không dấu..."):
                    filepath, error = download_media(
                        url=url,
                        format_type=format_type,
                        cookie_text=st.session_state["cookie_data"],
                        audio_quality=st.session_state["audio_quality"]
                    )
                    if error:
                        st.error(f"Lỗi hệ thống: {error}")
                        if "Sign in to confirm you're not a bot" in error:
                            st.info("💡 **Mẹo chống chặn:** YouTube quét máy chủ rất gắt. Hãy qua tab **'Cài Đặt Website'** dán Cookies tài khoản của bạn để mở khóa tải 100% nhé!")
                    else:
                        st.success("🎉 Đã xử lý tệp hoàn tất!")
                        with open(filepath, "rb") as f:
                            st.download_button(
                                label="📥 LƯU FILE VỀ ĐIỆN THOẠI",
                                data=f,
                                file_name=os.path.basename(filepath),
                                mime="audio/mpeg" if format_type == "mp3" else "video/mp4",
                                key="btn_save_download"
                            )
                        try: os.remove(filepath)
                        except: pass

# --- TAB 2: ĐỔI ĐUÔI TỪ VIDEO CÓ SẴN ---
with tab2:
    with st.container(border=True):
        st.subheader("🔄 Trích Xuất Âm Thanh Từ Máy")
        uploaded_file = st.file_uploader("Tải tệp video MP4 từ máy của bạn lên:", type=["mp4"], key="file_extractor")
        
        if uploaded_file is not None:
            if st.button("🎵 Tiến Hành Tách Nhạc", key="btn_convert"):
                with st.spinner("Đang trích xuất tần số âm thanh kỹ thuật số..."):
                    output_path, error = convert_mp4_to_mp3(uploaded_file)
                    if error:
                        st.error(f"Lỗi chuyển đổi: {error}")
                    else:
                        st.success("🎉 Trích xuất nhạc thành công!")
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="📥 LƯU FILE MP3 VỀ MÁY",
                                data=f,
                                file_name=os.path.basename(output_path),
                                mime="audio/mpeg",
                                key="btn_save_convert"
                            )
                        try: os.remove(output_path)
                        except: pass

# --- TAB 3: PHẦN CÀI ĐẶT WEBSITE (TÍNH NĂNG MỚI THEO YÊU CẦU) ---
with tab3:
    with st.container(border=True):
        st.subheader("⚙️ Cấu Hình Website Cá Nhân")
        
        # 1. Cài đặt thay đổi màu chủ đề giao diện trực tiếp
        selected_theme = st.selectbox(
            "Thay đổi tone màu giao diện (Theme):", 
            options=["Tím Neon", "Xanh Lục Bảo", "Xanh Biển Sâu"],
            index=["Tím Neon", "Xanh Lục Bảo", "Xanh Biển Sâu"].index(st.session_state["theme_color"])
        )
        if selected_theme != st.session_state["theme_color"]:
            st.session_state["theme_color"] = selected_theme
            st.rerun() # Tải lại trang ngay lập tức để áp dụng màu mới
        
        # 2. Cài đặt chất lượng âm thanh xuất ra
        st.session_state["audio_quality"] = st.select_slider(
            "Tùy chỉnh chất lượng nhạc MP3 tải về (kbps):",
            options=["128", "192", "256", "320"],
            value=st.session_state["audio_quality"]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🛡️ Cấu Hình Lấy Cookie Chống Chặn Bot")
        st.write("Nếu tải link YouTube bị thông báo lỗi màu hồng (Xác minh bot), bạn làm theo bước sau để xử lý:")
        st.caption("1. Lên máy tính/điện thoại, cài tiện ích mở rộng có tên là **'Get cookies.txt LOCALLY'** trên trình duyệt.")
         Kharên2 = "2. Đăng nhập vào trang youtube.com bằng tài khoản của bạn, bấm vào tiện ích đó rồi copy toàn bộ văn bản hiện ra."
        st.caption(Kharên2)
        st.caption("3. Dán toàn bộ đoạn mã đó vào ô dưới đây để website tự động giả lập tài khoản thật của bạn, vượt qua mọi sự kiểm duyệt.")
        
        cookie_input = st.text_area(
            "Dán nội dung Netscape Cookies vào đây:",
            value=st.session_state["cookie_data"],
            placeholder="# Netscape HTTP Cookie File...",
            height=120,
            key="cookie_textarea"
        )
        if cookie_input != st.session_state["cookie_data"]:
            st.session_state["cookie_data"] = cookie_input
            st.success("✅ Hệ thống đã tiếp nhận bộ Cookies chống chặn thành công!")
                                
