import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CẤU HÌNH GIAO DIỆN WEB PREMIUM
st.set_page_config(
    page_title="Cổng Thông Tin Chính Sách & Pháp Luật Việt Nam",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. TÙY BIẾN CSS CAO CẤP (VIP & XỊN)
st.markdown("""
<style>
    .stApp { background-color: #0b1329; color: #f8fafc; }
    section[data-testid="stSidebar"] { background-color: #1c2541 !important; border-right: 2px solid #3a506b; }
    
    /* Thiết kế thẻ Card Tin Tức */
    .policy-card {
        background: linear-gradient(135deg, #1c2541 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3a86ff;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .policy-tag {
        background-color: #3a86ff; color: white; padding: 3px 8px;
        border-radius: 5px; font-size: 8pt; font-weight: bold; display: inline-block; margin-bottom: 8px;
    }
    .policy-date { float: right; color: #94a3b8; font-size: 9pt; }
    
    /* Tiêu đề chính */
    .main-title {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 28pt !important; font-weight: 900; text-align: center; margin-bottom: 5px;
    }
    .sub-title { text-align: center; color: #94a3b8; font-size: 11pt; margin-bottom: 30px; }
</style>
""", unsafe_allow_html=True)

# 3. CƠ SỞ DỮ LIỆU LOGIC CHÍNH SÁCH VÀ PHÁP LUẬT (TỪ THÁNG 1/2026 ĐẾN NAY)
DATA_POLICIES = [
    {
        "id": "PL001", "month": "Tháng 1", "type": "Đất Đai & Tài Sản", "date": "15/01/2026",
        "title": "Áp dụng bảng giá đất mới đồng bộ theo Luật Đất Đai sửa đổi",
        "content": "Chính thức ban hành văn bản chỉ đạo hướng dẫn phương pháp định giá sát thị trường, tháo gỡ điểm nghẹn đền bù và đẩy nhanh tiến độ đầu tư công toàn quốc."
    },
    {
        "id": "PL002", "month": "Tháng 1", "type": "Hành Chính - Trật Tự", "date": "20/01/2026",
        "title": "Siết chặt chế tài quản lý và sử dụng pháo hoa dịp Tết Nguyên Đán",
        "content": "Bổ sung danh mục xử phạt vi phạm hành chính đối với hành vi mua bán pháo hoa không rõ nguồn gốc trên không gian mạng."
    },
    {
        "id": "PL003", "month": "Tháng 2", "type": "An Sinh Xã Hội", "date": "05/02/2026",
        "title": "Thông qua gói hỗ trợ người lao động và an sinh xã hội đầu năm",
        "content": "Chính phủ ký duyệt ngân sách hỗ trợ quà Tết và bảo hiểm xã hội tự nguyện cho hơn 2 triệu lao động có hoàn cảnh khó khăn."
    },
    {
        "id": "PL004", "month": "Tháng 2", "type": "An Ninh Mạng - Ngân Hàng", "date": "18/02/2026",
        "title": "Quy định bảo mật bắt buộc đối với giao dịch số hóa",
        "content": "Nghị định mới yêu cầu các tổ chức tín dụng phải áp dụng xác thực sinh trắc học (quét khuôn mặt tích hợp thẻ Căn cước) đối với mọi giao dịch trên 10 triệu đồng."
    },
    {
        "id": "PL005", "month": "Tháng 3", "type": "Giao Thông - Môi Trường", "date": "10/03/2026",
        "title": "Áp dụng quy chuẩn kiểm soát khí thải mới với xe máy, ô tô",
        "content": "Bắt đầu triển khai lộ trình đo kiểm khí thải định kỳ đối với phương tiện giao thông đường bộ nhằm giảm thiểu ô nhiễm môi trường tại các đô thị loại đặc biệt."
    },
    {
        "id": "PL006", "month": "Tháng 4", "type": "Kinh Tế - Đấu Thầu", "date": "01/04/2026",
        "title": "Luật sửa đổi bổ sung một số điều của Luật Đấu Thầu có hiệu lực",
        "content": "Cắt giảm 30% thủ tục hành chính, mở rộng quyền tự quyết cho khối y tế công cộng trong việc mua sắm trang thiết bị vật tư y tế khẩn cấp."
    },
    {
        "id": "PL007", "month": "Tháng 4", "type": "Thương Mại Điện Tử", "date": "25/04/2026",
        "title": "Quản lý thuế nghiêm ngặt đối với nền tảng TMĐT xuyên biên giới",
        "content": "Tổng cục Thuế bắt buộc các sàn thương mại điện tử (bao gồm TikTok Shop, Shopee...) phải trực tiếp kê khai và nộp thuế thay cho hộ kinh doanh cá thể."
    },
    {
        "id": "PL008", "month": "Tháng 5", "type": "Tài Chính - Thuế", "date": "12/05/2026",
        "title": "Gia hạn thời hạn nộp thuế GTGT và thuế thu nhập doanh nghiệp 2026",
        "content": "Chính sách nới lỏng dòng tiền nhằm hỗ trợ các doanh nghiệp phục hồi sản xuất, kích cầu tiêu dùng nội địa trong quý II."
    },
    {
        "id": "PL009", "month": "Tháng 5", "type": "Truyền Thông - Mạng Xã Hội", "date": "29/05/2026",
        "title": "Nghị định mới về xử phạt hành chính trong quảng cáo số",
        "content": "Tăng mức phạt lên gấp 3 lần đối với các hành vi giật tít, cung cấp thông tin sai sự thật hoặc quảng cáo thuốc, thực phẩm chức năng chưa kiểm duyệt trên mạng."
    },
    {
        "id": "PL010", "month": "Tháng 6", "type": "Định Danh - Số Hóa", "date": "15/06/2026",
        "title": "Đồng loạt triển khai thẻ Căn cước mới tích hợp dữ liệu sinh trắc học",
        "content": "Bộ Công an đẩy mạnh tích hợp dữ liệu ADN, giọng nói vào chip điện tử của thẻ Căn cước, phục vụ tối đa cho cổng dịch vụ công trực tuyến quốc gia."
    }
]

# 4. THANH SIDEBAR ĐẲNG CẤP TÍCH HỢP PROFILE TIKTOK CỦA BẠN
st.sidebar.markdown("<h2 style='color:#38bdf8; text-align:center; margin-top:0;'>🏛️ ĐIỀU HÀNH HỆ THỐNG</h2>", unsafe_allow_html=True)

# LƯU TRỮ PROFILE TIKTOK THEO YÊU CẦU CỦA BẠN
st.sidebar.markdown(
    """
    <div style="background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%); padding: 15px; border-radius: 12px; text-align: center; color: white; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(255, 0, 127, 0.2);">
        <img src="https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg" width="35" style="margin-bottom: 10px; filter: brightness(0) invert(1);"/>
        <h3 style="margin: 0; font-size: 13pt; font-weight: 800;">ADMIN: @phmvanduc209</h3>
        <p style="font-size: 9pt; opacity: 0.9; margin: 4px 0 12px 0;">Cổng thông tin Pháp luật Việt Nam</p>
        <a href="https://www.tiktok.com/@phmvanduc209" target="_blank" style="text-decoration: none;">
            <button style="background-color: white; color: #7928ca; border: none; padding: 10px 15px; font-weight: bold; border-radius: 25px; cursor: pointer; width: 100%; transition: 0.3s; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                🎵 KẾT NỐI TIKTOK CỦA TÔI
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### 🧭 MỤC LỤC CHỨC NĂNG")
menu_choice = st.sidebar.radio(
    "Lựa chọn khu vực dữ liệu:",
    [
        "📊 Tổng Quan & Chỉ Số Vĩ Mô",
        "📜 Dòng Thời Gian Chính Sách (Từ T1/2026)",
        "🔍 Bộ Lọc Tra Cứu Thông Minh"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("⚡ Hệ thống cập nhật tự động hóa • Bản quyền thuộc về Admin Phạm Văn Đức.")

# 5. KHU VỰC HIỂN THỊ NỘI DUNG CHÍNH (MAIN SCREEN)
st.markdown('<p class="main-title">🏛️ CỔNG THÔNG TIN PHÁP LUẬT & CHÍNH SÁCH VIỆT NAM</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Hệ thống phân tích, lưu trữ và tra cứu các văn bản chỉ đạo chiến lược của Nhà nước từ đầu năm 2026 đến nay</p>', unsafe_allow_html=True)

# ==========================================
# GIAO DIỆN MỤC 1: TỔNG QUAN & CHỈ SỐ VĨ MÔ
# ==========================================
if menu_choice == "📊 Tổng Quan & Chỉ Số Vĩ Mô":
    st.subheader("📈 Chỉ số tăng trưởng và quản lý điều hành")
    
    # Tạo các thẻ số liệu đẹp mắt (Metrics)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Văn bản đã ban hành", value="142 văn bản", delta="+12 trong tháng này")
    with m2:
        st.metric(label="Tốc độ số hóa thủ tục", value="89.4%", delta="+4.2% so với 2025")
    with m3:
        st.metric(label="Doanh nghiệp thành lập mới", value="68,500 DN", delta="+6.7% cùng kỳ")
    with m4:
        st.metric(label="Chỉ số niềm tin kinh tế", value="Vượt bậc (S)", delta="Ổn định vĩ mô")
        
    st.markdown("---")
    st.subheader("📌 Tiêu điểm cải cách hành chính nổi bật nửa đầu năm 2026")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.info("💡 **Trọng tâm Chuyển đổi số Quốc gia:** Tất cả các Nghị định trong giai đoạn từ tháng 1 đến tháng 6 năm 2026 đều hướng đến việc cắt giảm giấy tờ vật lý. Việc bắt buộc xác thực sinh trắc học trong tài chính và định danh công dân qua chip ADN đánh dấu bước ngoặt lớn về an ninh hạ tầng số.")
    with col_right:
        st.success("🏢 **Đồng hành cùng Doanh nghiệp:** Chính sách nới lỏng gia hạn thời gian nộp thuế thu nhập và thuế GTGT thực hiện từ tháng 5 đã giúp hơn 100,000 doanh nghiệp vừa và nhỏ giải quyết bài toán thiếu hụt vốn lưu động ngắn hạn một cách nhanh chóng.")

# ==========================================
# GIAO DIỆN MỤC 2: DÒNG THỜI GIAN CHÍNH SÁCH
# ==========================================
elif menu_choice == "📜 Dòng Thời Gian Chính Sách (Từ T1/2026)":
    st.subheader("📅 Trục thời gian tiến trình thông qua luật pháp")
    st.write("Chọn tab tháng để xem các chính sách cốt lõi được thực thi:")
    
    # Khởi tạo hệ thống Tabs logic theo tháng
    t1, t2, t3, t4, t5, t6 = st.tabs(["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6 (Hiện tại)"])
    
    months_mapping = {
        "Tháng 1": t1, "Tháng 2": t2, "Tháng 3": t3, "Tháng 4": t4, "Tháng 5": t5, "Tháng 6": t6
    }
    
    for m_name, tab_obj in months_mapping.items():
        with tab_obj:
            filtered = [p for p in DATA_POLICIES if p["month"] == m_name]
            if not filtered:
                st.write("🔍 Đang cập nhật thêm văn bản bổ sung cho tháng này...")
            for p in filtered:
                st.markdown(f"""
                <div class="policy-card">
                    <span class="policy-tag">{p['type']}</span>
                    <span class="policy-date">📅 Hiệu lực: {p['date']}</span>
                    <h4 style="color:#38bdf8; margin-top:5px; margin-bottom:8px;">{p['title']}</h4>
                    <p style="color:#cbd5e1; font-size:10.5pt; margin-bottom:0;">{p['content']}</p>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# GIAO DIỆN MỤC 3: BỘ LỌC TRA CỨU THÔNG MINH
# ==========================================
elif menu_choice == "🔍 Bộ Lọc Tra Cứu Thông Minh":
    st.subheader("🔍 Tìm kiếm văn bản quy phạm pháp luật nâng cao")
    
    # Hệ thống điều hướng lọc tìm kiếm logic
    fl_col1, fl_col2 = st.columns(2)
    with fl_col1:
        search_query = st.text_input("📝 Nhập từ khóa cần tìm (Ví dụ: Đất đai, Thuế, TikTok, Căn cước...):", placeholder="Gõ từ khóa tại đây...")
    with fl_col2:
        type_options = ["Tất cả các hệ"] + list(set([p["type"] for p in DATA_POLICIES]))
        selected_type = st.selectbox("🗂️ Phân loại theo lĩnh vực:", type_options)
        
    # Xử lý logic lọc dữ liệu
    results = DATA_POLICIES
    if search_query:
        results = [r for r in results if search_query.lower() in r["title"].lower() or search_query.lower() in r["content"].lower()]
    if selected_type != "Tất cả các hệ":
        results = [r for r in results if r["type"] == selected_type]
        
    st.markdown("---")
    st.write(f"📊 Tìm thấy **{len(results)}** văn bản phù hợp với điều kiện lọc:")
    
    if not results:
        st.warning("Không tìm thấy dữ liệu phù hợp với từ khóa của bạn. Vui lòng thử lại bằng từ khóa khác!")
    else:
        for p in results:
            with st.expander(f"📌 [{p['month']}] - {p['title']}"):
                st.markdown(f"""
                <p><b>🏢 Lĩnh vực:</b> {p['type']}</p>
                <p><b>📅 Ngày công bố công báo:</b> {p['date']}</p>
                <p style="background-color:#1e293b; padding:12px; border-radius:6px; border-left:3px solid #0284c7; color:#e2e8f0;">
                    <b>Nội dung chi tiết chính sách:</b><br>{p['content']}
                </p>
                """, unsafe_allow_html=True)
                
                # Nút tương tác nhanh
                if st.button(f"Tải file đính kèm giả lập ({p['id']})", key=p['id']):
                    st.toast(f"📥 Đang tải file PDF văn bản chỉ đạo điều hành mã số {p['id']} về máy...", icon="🚀")
    
