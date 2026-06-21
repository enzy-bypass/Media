import streamlit as st
import pandas as pd

# Cấu hình trang hiển thị rộng rãi, tối ưu cho giao diện Wiki game
st.set_page_config(
    page_title="Blox Fruits Ultimate Wiki",
    page_icon="🍇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GIẢ LẬP CƠ SỞ DỮ LIỆU BLOX FRUITS (CHUẨN CẬP NHẬT MỚI NHẤT) ---
FRUIT_DATA = [
    # MYTHICAL
    {"name": "Kitsune", "rarity": "Mythical", "type": "Beast", "price_beli": 8000000, "price_robux": 2300, "spawn_chance": "0.05%", "stock_chance": "1%", "tier": "SS", "description": "Trái ác quỷ đắt nhất và bá đạo nhất hiện tại. Tốc độ di chuyển cực nhanh, sát thương diện rộng và khả năng biến hình hồ ly chín đuôi."},
    {"name": "Dragon (Rework)", "rarity": "Mythical", "type": "Beast", "price_beli": 10000000, "price_robux": 2600, "spawn_chance": "0.07%", "stock_chance": "1%", "tier": "SS", "description": "Đang là tâm điểm với bản cập nhật làm lại toàn diện. Sát thương bá đạo, phòng thủ trâu bò khi hóa rồng."},
    {"name": "Leopard", "rarity": "Mythical", "type": "Beast", "price_beli": 5000000, "price_robux": 3000, "spawn_chance": "0.25%", "stock_chance": "1.4%", "tier": "S", "description": "Tốc độ vả đòn cực nhanh, không thể bị phá chiêu khi đang combo. Thích hợp tối đa cho PvP cao cấp."},
    {"name": "T-Rex", "rarity": "Mythical", "type": "Beast", "price_beli": 2700000, "price_robux": 2350, "spawn_chance": "0.3%", "stock_chance": "2%", "tier": "S", "description": "Tạo ra các vết cắn gây sát thương theo thời gian (DoT) và có kỹ năng gầm rú diện rộng rất mạnh."},
    {"name": "Dough", "rarity": "Mythical", "type": "Elemental", "price_beli": 2800000, "price_robux": 2400, "spawn_chance": "1.34%", "stock_chance": "1.4%", "tier": "S (V2)", "description": "Vua Combo PvP khi thức tỉnh (V2). Khả năng trói chân và kéo đối thủ cực kỳ khó chịu."},
    {"name": "Mammoth", "rarity": "Mythical", "type": "Beast", "price_beli": 2700000, "price_robux": 2350, "spawn_chance": "0.3%", "stock_chance": "2%", "tier": "A", "description": "Khả năng dẫm đạp liên tục gây lượng lớn sát thương. Rất trâu bò trong các trận săn Boss Raid."},
    
    # LEGENDARY
    {"name": "Buddha", "rarity": "Legendary", "type": "Beast", "price_beli": 1200000, "price_robux": 1650, "spawn_chance": "6.6%", "stock_chance": "5%", "tier": "SS (Farm)", "description": "Vua farm quái từ Sea 1 đến Sea 3. Tăng kích thước tầm đánh cận chiến lên cực đại và giảm 50% sát thương gánh chịu."},
    {"name": "Portal", "rarity": "Legendary", "type": "Natural", "price_beli": 1900000, "price_robux": 2000, "spawn_chance": "3.5%", "stock_chance": "4%", "tier": "S (PvP/Di chuyển)", "description": "Bá chủ di chuyển bản đồ với các cổng không gian. Kỹ năng khống chế đưa đối thủ vào hư vô để tạo combo đột biến."},
    {"name": "Rumble", "rarity": "Legendary", "type": "Elemental", "price_beli": 2100000, "price_robux": 2100, "spawn_chance": "2.25%", "stock_chance": "4%", "tier": "A", "description": "Trái sấm sét, cung cấp các lượt dịch chuyển nhanh và làm choáng đối thủ bằng dòng điện cực mạnh."},
    {"name": "Blizzard", "rarity": "Legendary", "type": "Elemental", "price_beli": 2400000, "price_robux": 2250, "spawn_chance": "1.2%", "stock_chance": "2%", "tier": "A", "description": "Tạo bão tuyết diện rộng liên tục bám đuổi mục tiêu. Vô cùng hiệu quả khi đi Factory hoặc tháp Sea Event."},
    
    # RARE & UNCOMMON TIÊU BIỂU
    {"name": "Magma", "rarity": "Rare", "type": "Elemental", "price_beli": 850000, "price_robux": 1300, "spawn_chance": "7.2%", "stock_chance": "10%", "tier": "S (Săn Sea)", "description": "Sát thương thô cao nhất trò chơi khi thức tỉnh V2. Đi bộ trên nước và là khắc tinh số một của Seabeast."},
    {"name": "Light", "rarity": "Rare", "type": "Elemental", "price_beli": 650000, "price_robux": 1100, "spawn_chance": "9.1%", "stock_chance": "20%", "tier": "A (Sea 1)", "description": "Trái ác quỷ tốt nhất cho người mới chơi ở Sea 1 nhờ tốc độ bay nhanh nhất game và có vũ khí ánh sáng đánh lan."}
]

# --- TÙY BIẾN CSS PHONG CÁCH GAMING WIKI CAO CẤP ---
st.markdown("""
<style>
    /* Nền tổng thể tối phong cách Discord/Gaming */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    
    /* Thanh bên trái */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* Tiêu đề trang */
    .wiki-title {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32pt !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0px 4px 10px rgba(245, 158, 11, 0.2);
    }
    
    .wiki-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 11pt;
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    /* Thiết kế Hộp Card Trái Ác Quỷ tương tác bấm */
    .fruit-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
    }
    .fruit-card:hover {
        transform: translateY(-3px);
        border-color: #f59e0b;
        box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.15);
    }
    
    /* Huy hiệu độ hiếm */
    .badge-mythical { background-color: #7a1fa2; color: #f3e5f5; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 9pt; }
    .badge-legendary { background-color: #b57c1e; color: #fffde7; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 9pt; }
    .badge-rare { background-color: #1565c0; color: #e3f2fd; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 9pt; }
    
    /* Thiết kế bảng dữ liệu sạch */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 10.5pt;
        background-color: #1e293b;
        border-radius: 8px;
        overflow: hidden;
    }
    .styled-table th {
        background-color: #334155;
        color: #fbbf24;
        text-align: left;
        padding: 12px;
        font-weight: 700;
    }
    .styled-table td {
        padding: 12px;
        border-bottom: 1px solid #334155;
    }
    
    /* Tabs tinh chỉnh màu sắc */
    div[data-testid="stTabBar"] button {
        font-size: 11pt !important;
        font-weight: 700 !important;
        color: #94a3b8 !important;
    }
    div[data-testid="stTabBar"] button[aria-selected="true"] {
        color: #fbbf24 !important;
        border-bottom-color: #fbbf24 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ CHÍNH ---
st.markdown('<p class="wiki-title">🏴‍☠️ BLOX FRUITS GRAND WIKI</p>', unsafe_allow_html=True)
st.markdown('<p class="wiki-subtitle">Cổng thông tin tra cứu tự động - Toàn bộ dữ liệu Trái Ác Quỷ & Cơ chế Game mới nhất</p>', unsafe_allow_html=True)

# --- THANH DIỀU HƯỚNG BÊN TRÁI (SIDEBAR NAVIGATION) ---
st.sidebar.markdown("<h2 style='color:#fbbf24; text-align:center;'>🧭 MỤC LỤC WIKI</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "Lựa chọn danh mục tra cứu:",
    [
        "🏠 Trang Chủ & Tin Tức Mới",
        "🍇 Thư Viện Trái Ác Quỷ (A-Z)",
        "🌲 Tỷ Lệ Spawn & Mẹo Nhặt Trái",
        "⚔️ Bảng Xếp Hạng Sức Mạnh (Tier List)",
        "🧮 Máy Tính Định Giá Giao Dịch (Trade)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Thống Kê Nhanh")
st.sidebar.write("• Tổng số trái ác quỷ: **39 Trái**")
st.sidebar.write("• Bản cập nhật hiện tại: **Update 21+**")
st.sidebar.write("• Tình trạng máy chủ: 🟢 **Hoạt động tốt**")

# ======================================================================================================================
# TAB 1: TRANG CHỦ & TIN TỨC MỚI NHẤT
# ======================================================================================================================
if menu == "🏠 Trang Chủ & Tin Tức Mới":
    st.header("🔥 Bản Tin Cập Nhật Mới Nhất")
    
    with st.container():
        st.markdown("""
        <div style='background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #ef4444;'>
            <h3 style='color: #f59e0b; margin-top:0;'>✨ Sự Kiện Rework Dragon & Cân Bằng Kitsune</h3>
            <p>Hệ thống kỹ năng của <b>Dragon (Long Tộc)</b> đã được thiết kế lại hoàn toàn với đồ họa chiêu thức siêu khủng, tăng mạnh sát thương thiêu đốt toàn bản đồ. Bên cạnh đó, tỷ lệ bán trong shop của <b>Kitsune</b> được tối ưu hóa giúp game trải nghiệm mượt mà hơn.</p>
            <span style='background: #3b82f6; padding: 2px 8px; border-radius: 4px; font-size: 8pt;'>HOT UPDATE</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🎮 Hướng Dẫn Cơ Bản Cho Tân Thủ")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='fruit-card'>
            <h4 style='color: #fbbf24;'>🌊 Đại Dương 1 (Sea 1)</h4>
            <p>Tập trung tìm kiếm trái <b>Light (Ánh Sáng)</b> hoặc <b>Buddha (Phật Tổ)</b> để hoàn thành nhiệm vụ nhanh nhất có thể. Đừng vội pvp ở giai đoạn này.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='fruit-card'>
            <h4 style='color: #f43f5e;'>🌋 Đại Dương 2 (Sea 2)</h4>
            <p>Mở khóa tính năng <b>Thức Tỉnh Trái Ác Quỷ (Awakening)</b> tại vùng đất Băng và Lửa qua các trận Raid căng thẳng cùng đồng đội.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='fruit-card'>
            <h4 style='color: #a855f7;'>🌌 Đại Dương 3 (Sea 3)</h4>
            <p>Tham gia các sự kiện biển lớn (Sea Events), săn Leviathan, đánh rương ma quái và tối ưu hóa điểm số bảng xếp hạng PvP của bạn.</p>
        </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# TAB 2: THƯ VIỆN TRÁI ÁC QUỶ TƯƠNG TÁC CHUẨN
# ======================================================================================================================
elif menu == "🍇 Thư Viện Trái Ác Quỷ (A-Z)":
    st.header("🍇 Bộ Từ Điển Toàn Bộ Trái Ác Quỷ")
    st.write("Sử dụng bộ lọc thông minh bên dưới để tìm kiếm, click chuột để xem thông tin chi tiết của từng trái.")
    
    # Bộ lọc tương tác trực quan
    search_query = st.text_input("🔍 Nhập tên trái ác quỷ cần tìm kiếm gấp:", placeholder="Ví dụ: Kitsune, Buddha, Magma...")
    
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        rarity_filter = st.multiselect("Phân loại theo Độ Hiếm (Rarity):", ["Mythical", "Legendary", "Rare"], default=["Mythical", "Legendary", "Rare"])
    with col_filter2:
        type_filter = st.multiselect("Phân loại theo Hệ (Type):", ["Beast", "Elemental", "Natural"], default=["Beast", "Elemental", "Natural"])
        
    # Lọc dữ liệu dựa trên thao tác click/nhập của người dùng
    filtered_fruits = [
        f for f in FRUIT_DATA
        if (search_query.lower() in f["name"].lower()) and (f["rarity"] in rarity_filter) and (f["type"] in type_filter)
    ]
    
    st.markdown(f"**Kết quả bộ lọc:** Tìm thấy `{len(filtered_fruits)}` trái phù hợp.", unsafe_allow_html=True)
    
    # Hiển thị danh sách dạng hộp Card tương tác cao
    for fruit in filtered_fruits:
        badge_style = "badge-mythical" if fruit["rarity"] == "Mythical" else ("badge-legendary" if fruit["rarity"] == "Legendary" else "badge-rare")
        
        with st.expander(f"⭐ {fruit['name']} [{fruit['rarity']} - Hệ {fruit['type']}] — Xem Chi Tiết Kỹ Năng"):
            st.markdown(f"""
            <div style='background-color: #24324d; padding: 15px; border-radius: 8px; margin-bottom: 10px;'>
                <p><b>✨ Tổng quan:</b> {fruit['description']}</p>
                <table class='styled-table'>
                    <tr>
                        <th>Giá Tiền Beli</th>
                        <th>Giá Mua Robux</th>
                        <th>Tỷ Lệ Nhặt (Spawn)</th>
                        <th>Tỷ Lệ Bán Ở Shop</th>
                        <th>Xếp Hạng (Tier)</th>
                    </tr>
                    <tr>
                        <td style='color: #4ade80;'>💵 {fruit['price_beli']:,} Beli</td>
                        <td style='color: #60a5fa;'>💎 {fruit['price_robux']} Robux</td>
                        <td>{fruit['spawn_chance']}</td>
                        <td>{fruit['stock_chance']}</td>
                        <td><b style='color:#f59e0b;'>{fruit['tier']}</b></td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            # Khởi tạo mô phỏng bộ chiêu thức tương tác
            st.write("🎮 **Hệ thống phím bấm kỹ năng (Moveset Demo):**")
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            with btn_col1:
                if st.button(f"Phím [Z] - Chiêu 1 của {fruit['name']}", key=f"z_{fruit['name']}"):
                    st.toast(f"💥 Kích hoạt chiêu thức khởi động của {fruit['name']}! Gây choáng nhẹ.", icon="⚡")
            with btn_col2:
                if st.button(f"Phím [X] - Chiêu 2 của {fruit['name']}", key=f"x_{fruit['name']}"):
                    st.toast(f"☄️ Kích hoạt chiêu định hướng di chuyển diện rộng!", icon="🔥")
            with btn_col3:
                if st.button(f"Phím [C] - Chiêu 3 của {fruit['name']}", key=f"c_{fruit['name']}"):
                    st.toast(f"🌪️ Chiêu thức khống chế cứng, phá vỡ giáp Haki đối thủ!", icon="🔮")
            with btn_col4:
                if st.button(f"Phím [V] - Kỹ năng Tối Thượng", key=f"v_{fruit['name']}"):
                    st.balloons()
                    st.success(f"👑 BẠN ĐÃ KÍCH HOẠT CHIÊU CUỐI SIÊU CẤP CỦA {fruit['name']}! QUÉT SẠCH BẢN ĐỒ!")

# ======================================================================================================================
# TAB 3: TỶ LỆ SPAWN & CƠ CHẾ NHẶT TRÁI
# ======================================================================================================================
elif menu == "🌲 Tỷ Lệ Spawn & Mẹo Nhặt Trái":
    st.header("🌲 Cơ Chế Xuất Hiện Trái Ác Quỷ Tự Nhiên")
    
    col_spawn1, col_spawn2 = st.columns(2)
    with col_spawn1:
        st.markdown("""
        <div style='background: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #f59e0b;'>
            <h4 style='color:#fbbf24; margin-top:0;'>⏰ Thời Gian Khởi Tạo (Spawn Time)</h4>
            <p>• <b>Ngày thường (Thứ 2 - Thứ 6):</b> Cứ mỗi <b>1 tiếng đồng hồ</b> tròn hệ thống sẽ tự động tạo ra 1 trái ác quỷ ngẫu nhiên dưới gốc cây bất kỳ trên bản đồ.</p>
            <p>• <b>Ngày cuối tuần (Thứ 7 & CN):</b> Thời gian rút ngắn xuống chỉ còn <b>45 phút</b> một trái.</p>
            <p>• <b>Cơ chế biến mất (Despawn):</b> Nếu không có ai tìm thấy và nhặt lên, trái ác quỷ sẽ tự động biến mất hoàn toàn sau đúng <b>20 phút</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_spawn2:
        st.markdown("""
        <div style='background: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #10b981;'>
            <h4 style='color:#10b981; margin-top:0;'>💡 Mẹo Sắp Đặt & Săn Tìm Hiệu Quả</h4>
            <p>1. <b>Sử dụng Gamepass Fruit Notifier:</b> Thiết bị định vị rương/trái ác quỷ tự động báo khoảng cách mét chính xác giúp bạn nhặt ngay trong vài giây.</p>
            <p>2. <b>Săn ở Server Vip:</b> Thuê hoặc dùng server riêng tư để một mình bạn kiểm soát toàn bộ gốc cây, tránh sự tranh giành từ các hacker bay lượn.</p>
            <p>3. <b>Thời gian Server Mới:</b> Khi một server vừa được khởi chạy, một trái ác quỷ luôn có sẵn ngay từ giây đầu tiên.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Bảng Phân Chia Tỷ Lệ Theo Độ Hiếm Toàn Bộ Game")
    
    # Biểu diễn dữ liệu bằng bảng trực quan của Streamlit
    spawn_table_data = {
        "Hạng Trái Ác Quỷ": ["Common (Thường)", "Uncommon (Không phổ biến)", "Rare (Hiếm)", "Legendary (Huyền thoại)", "Mythical (Thần thoại)"],
        "Tỷ Lệ Xuất Hiện Dưới Cây (Spawn)": ["45% - 50%", "28% - 30%", "12% - 15%", "5% - 7%", "Dưới 1% (Cực hiếm)"],
        "Tỷ Lệ Xuất Hiện Ở Cửa Hàng (Stock)": ["Thường xuyên 100%", "70%", "35%", "10%", "1% - 2%"],
        "Trái Tiêu Biểu": ["Rocket, Spin", "Flame, Ice", "Light, Magma", "Buddha, Portal", "Kitsune, Dragon, Dough"]
    }
    df_spawn = pd.DataFrame(spawn_table_data)
    st.table(df_spawn)

# ======================================================================================================================
# TAB 4: BẢNG XẾP HẠNG SỨC MẠNH (TIER LIST)
# ======================================================================================================================
elif menu == "⚔️ Bảng Xếp Hạng Sức Mạnh (Tier List)":
    st.header("⚔️ Bảng Xếp Hạng Trái Ác Quỷ Toàn Diện")
    st.write("Bảng xếp hạng được tổng hợp dựa trên đánh giá của các game thủ chuyên nghiệp hàng đầu tại Sea 3.")
    
    tier_tab1, tier_tab2 = st.tabs(["🔥 Chuyên Dùng Đi PvP/Săn Bounti", "🌾 Chuyên Dùng Để Treo Máy Farm Cấp"])
    
    with tier_tab1:
        st.markdown("""
        <div class='fruit-card'>
            <b style='color:#ef4444; font-size:14pt;'>Tier SS (Vua PvP):</b> Kitsune, Dragon, Dough V2, Leopard.<br>
            <span style='color:#94a3b8;'>→ Giải thích: Chiêu thức tầm đánh rộng, phá thế thủ, sát thương dồn sốc chết mục tiêu lập tức.</span>
        </div>
        <div class='fruit-card'>
            <b style='color:#f59e0b; font-size:14pt;'>Tier A (Bậc Thầy Kỹ Năng):</b> Portal, Rumble, T-Rex, Ice V2.<br>
            <span style='color:#94a3b8;'>→ Giải thích: Đòi hỏi khả năng căn góc phím bấm chính xác để thực hiện chuỗi combo phối hợp kiếm và súng.</span>
        </div>
        """, unsafe_allow_html=True)
        
    with tier_tab2:
        st.markdown("""
        <div class='fruit-card'>
            <b style='color:#10b981; font-size:14pt;'>Tier TOP 1 FARM:</b> Buddha (Phật Tổ Thức Tỉnh).<br>
            <span style='color:#94a3b8;'>→ Giải thích: Không có đối thủ ở mảng cày cuốc level. Bật phím biến khổng lồ lên và nhấn chuột vả cận chiến là quét sạch quái đảo.</span>
        </div>
        <div class='fruit-card'>
            <b style='color:#3b82f6; font-size:14pt;'>Tier TOP 2 FARM:</b> Magma V2, Light, Blizzard.<br>
            <span style='color:#94a3b8;'>→ Giải thích: Kỹ năng định vị mục tiêu tốt, chiêu thức đánh lan không làm đẩy quái ra xa giúp tối ưu hóa thời gian gom cụm quái.</span>
        </div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# TAB 5: MÁY TÍNH ĐỊNH GIÁ GIAO DỊCH TRADING
# ======================================================================================================================
elif menu == "🧮 Máy Tính Định Giá Giao Dịch (Trade)":
    st.header("🧮 Bộ Tính Toán Giá Trị Vật Phẩm Giao Dịch Thông Minh")
    st.write("Tránh bị ép giá hoặc lừa đảo khi thực hiện giao dịch trong khu vực Cafe (Sea 2) hoặc Mansion (Sea 3).")
    
    col_trade1, col_trade2 = st.columns(2)
    
    with col_trade1:
        st.subheader("🛒 Trái Của Bạn Đem Trao Đổi")
        your_fruit = st.selectbox("Chọn trái ác quỷ bạn đang sở hữu:", [f["name"] for f in FRUIT_DATA], key="trade_yours")
        your_amount = st.number_input("Số lượng trái:", min_value=1, max_value=4, value=1, key="amount_yours")
        
        # Tìm giá tương ứng
        your_price = next(f["price_beli"] for f in FRUIT_DATA if f["name"] == your_fruit) * your_amount
        st.metric(label="Tổng trị giá Beli hệ thống của bạn:", value=f"{your_price:,} Beli")
        
    with col_trade2:
  
