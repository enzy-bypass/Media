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
  
import streamlit as st
import pandas as pd

# Cấu hình giao diện Wiki rộng rãi, chuẩn Gaming
st.set_page_config(
    page_title="Blox Fruits Grand Wiki",
    page_icon="🍇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CƠ SỞ DỮ LIỆU TRÁI ÁC QUỶ MỚI NHẤT ---
FRUIT_DATA = [
    # MYTHICAL (THẦN THOẠI)
    {"name": "Kitsune", "rarity": "Mythical", "type": "Beast", "price_beli": 8000000, "price_robux": 2300, "spawn_chance": "0.05%", "stock_chance": "1%", "tier": "SS", "description": "Trái đắt nhất game. Tốc độ chạy cực nhanh, sát thương diện rộng và có thanh nội năng biến hình Hồ Ly 9 đuôi."},
    {"name": "Dragon (Rework)", "rarity": "Mythical", "type": "Beast", "price_beli": 10000000, "price_robux": 2600, "spawn_chance": "0.07%", "stock_chance": "1%", "tier": "SS", "description": "Tâm điểm làm lại toàn diện. Sát thương thiêu đốt bá đạo và khả năng hóa Rồng khổng lồ tăng phòng thủ."},
    {"name": "Leopard", "rarity": "Mythical", "type": "Beast", "price_beli": 5000000, "price_robux": 3000, "spawn_chance": "0.25%", "stock_chance": "1.4%", "tier": "S", "description": "Vua vả đòn tốc độ cao, không thể bị phá chiêu (Unbreakable) khi đang combo pvp."},
    {"name": "Dough", "rarity": "Mythical", "type": "Elemental", "price_beli": 2800000, "price_robux": 2400, "spawn_chance": "1.34%", "stock_chance": "1.4%", "tier": "S (V2)", "description": "Bá chủ Combo PvP khi thức tỉnh V2. Khả năng trói chân và kéo kéo đối thủ cực kỳ khó chịu."},
    {"name": "T-Rex", "rarity": "Mythical", "type": "Beast", "price_beli": 2700000, "price_robux": 2350, "spawn_chance": "0.3%", "stock_chance": "2%", "tier": "S", "description": "Hóa khủng long bạo chúa, có cơ chế cào cấu gây sát thương theo thời gian (DoT) và gầm rú làm choáng."},
    {"name": "Mammoth", "rarity": "Mythical", "type": "Beast", "price_beli": 2700000, "price_robux": 2350, "spawn_chance": "0.3%", "stock_chance": "2%", "tier": "A", "description": "Hóa voi ma mút, có chiêu húc liên tục cực trâu bò, chuyên dùng để càn quét Boss Raid."},
    
    # LEGENDARY (HUYỀN THOẠI)
    {"name": "Buddha", "rarity": "Legendary", "type": "Beast", "price_beli": 1200000, "price_robux": 1650, "spawn_chance": "6.6%", "stock_chance": "5%", "tier": "SS (Farm)", "description": "Vua cày cấp (Farm level) từ Sea 1 đến Sea 3. Biến khổng lồ tăng 800% tầm đánh cận chiến và giảm 50% sát thương nhận vào."},
    {"name": "Portal", "rarity": "Legendary", "type": "Natural", "price_beli": 1900000, "price_robux": 2000, "spawn_chance": "3.5%", "stock_chance": "4%", "tier": "S (Di Chuyển)", "description": "Trái cổng không gian, giúp dịch chuyển tức thời mọi đảo và đưa đối thủ vào chiều không gian hư vô để tạo đột biến."},
    {"name": "Rumble", "rarity": "Legendary", "type": "Elemental", "price_beli": 2100000, "price_robux": 2100, "spawn_chance": "2.25%", "stock_chance": "4%", "tier": "A", "description": "Trái sấm sét, cho phép lướt nhanh 3 lần liên tiếp và tạo các cột sét làm choáng diện rộng cực lâu."},
    
    # RARE (HIẾM)
    {"name": "Magma", "rarity": "Rare", "type": "Elemental", "price_beli": 850000, "price_robux": 1300, "spawn_chance": "7.2%", "stock_chance": "10%", "tier": "S (Săn Sea)", "description": "Sát thương thô cao nhất trò chơi khi thức tỉnh V2. Có khả năng đi bộ trên mặt nước, khắc tinh số 1 của Sea Beast."},
    {"name": "Light", "rarity": "Rare", "type": "Elemental", "price_beli": 650000, "price_robux": 1100, "spawn_chance": "9.1%", "stock_chance": "20%", "tier": "A (Sea 1)", "description": "Trái tốt nhất cho tân thủ Sea 1 nhờ tốc độ bay nhanh nhất game và có kiếm ánh sáng để đánh lan."}
]

# --- TÙY BIẾN CSS ĐỂ WEBSITE ĐẸP NHƯ WIKI CHUYÊN NGHIỆP ---
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    section[data-testid="stSidebar"] { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    .main-title {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 34pt !important; font-weight: 900; text-align: center; margin-bottom: 0px;
    }
    .sub-title { text-align: center; color: #94a3b8; font-size: 11pt; margin-bottom: 30px; }
    .card { background: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; margin-bottom: 12px; }
    .styled-table { width: 100%; border-collapse: collapse; margin: 10px 0; background-color: #111827; border-radius: 8px; overflow: hidden; }
    .styled-table th { background-color: #1f2937; color: #f59e0b; text-align: left; padding: 10px; }
    .styled-table td { padding: 10px; border-bottom: 1px solid #374151; }
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ TRANG CHỦ ---
st.markdown('<p class="main-title">⚔️ BLOX FRUITS WIKI A-Z ⚔️</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Hệ thống tra cứu dữ liệu Trái Ác Quỷ, Tỷ lệ Spawn & Cơ chế Game mới nhất hiện tại</p>', unsafe_allow_html=True)

# --- THANH DIỀU HƯỚNG SIDEBAR (BỐ CỤC RÕ RÀNG) ---
st.sidebar.markdown("<h2 style='color:#f59e0b; text-align:center;'>🧭 MỤC LỤC TRA CỨU</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "Chọn nội dung bạn cần xem:",
    [
        "🔥 Tin Tức & Cập Nhật Mới Nhất",
        "🍇 Thư Viện Toàn Bộ Trái Ác Quỷ",
        "🌲 Tỷ Lệ Spawn Trái Tự Nhiên",
        "⚔️ Bảng Xếp Hạng Sức Mạnh (Tier List)",
        "🧮 Máy Tính Định Giá Trade Trái"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Thông tin phiên bản")
st.sidebar.info("• Phiên bản: **Update 21 / 22 Rework**\n• Dữ liệu: **Chuẩn chuẩn 100%**\n• Trạng thái hệ thống: 🟢 Sẵn sàng")

# ======================================================================================================================
# DANH MỤC 1: TIN TỨC MỚI NHẤT
# ======================================================================================================================
if menu == "🔥 Tin Tức & Cập Nhật Mới Nhất":
    st.header("📣 Tin tức tiêu điểm hiện tại")
    st.markdown("""
    <div class='card' style='border-left: 5px solid #ef4444;'>
        <h3 style='color:#f59e0b; margin-top:0;'>✨ Sự kiện Dragon Rework & Trái Ác Quỷ Mới</h3>
        <p>Bản cập nhật mới nhất tập trung vào việc làm lại hoàn toàn bộ kỹ năng của <b>Trái Dragon (Rồng)</b> với hiệu ứng đồ họa bùng nổ, biến hình cực ngầu và bổ sung thêm các cơ chế pvp tối thượng. Trái <b>Kitsune</b> vẫn giữ ngôi vương về độ đắt đỏ và toàn diện.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🗺️ Hành trình vượt Đại Dương (Dành cho Tân thủ)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'><h4>🌊 Sea 1 (Biển Cũ)</h4><p>Tập trung cày cấp bằng trái <b>Light</b>. Hãy mua thuyền đi làm nhiệm vụ theo đúng cấp độ cấp bậc ở các đảo.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><h4>🌋 Sea 2 (Tân Thế Giới)</h4><p>Chuyển sang dùng trái <b>Buddha V2</b> để đi Raid. Mở khóa tính năng Trade trái ác quỷ tại quán Cafe.</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'><h4>🌌 Sea 3 (Biển Cuối)</h4><p>Tham gia săn Sea Events, săn Boss Leviathan lấy nguyên liệu chế tạo và tối ưu hóa điểm Bounty PvP.</p></div>", unsafe_allow_html=True)

# ======================================================================================================================
# DANH MỤC 2: THƯ VIỆN TOÀN BỘ TRÁI ÁC QUỶ (CLICK CHUẨN TƯƠNG TÁC)
# ======================================================================================================================
elif menu == "🍇 Thư Viện Toàn Bộ Trái Ác Quỷ":
    st.header("🍇 Từ Điển Tra Cứu Trái Ác Quỷ Tương Tác")
    st.write("Dưới đây là danh sách đầy đủ. Bạn hãy gõ tìm kiếm hoặc bấm click vào từng trái để mở bung thông tin chi tiết kỹ năng bên dưới!")
    
    # Thanh tìm kiếm thông minh
    search_fruit = st.text_input("🔍 Nhập tên trái cần tra cứu nhanh (Ví dụ: Kitsune, Buddha...):", placeholder="Gõ tên trái vào đây...")
    
    # Lọc dữ liệu theo từ khóa nhập
    filtered_list = [f for f in FRUIT_DATA if search_fruit.lower() in f["name"].lower()]
    
    for fruit in filtered_list:
        # Click để mở rộng chi tiết (Expander tương tác)
        with st.expander(f"⭐ Trái {fruit['name']} ({fruit['rarity']} — Hệ {fruit['type']})"):
            st.markdown(f"""
            <div style='background-color: #111827; padding: 15px; border-radius: 8px;'>
                <p><b>📝 Mô tả sức mạnh:</b> {fruit['description']}</p>
                <table class='styled-table'>
                    <tr>
                        <th>💵 Giá Tiền (Beli)</th>
                        <th>💎 Giá Mua (Robux)</th>
                        <th>🌲 Tỷ lệ nhặt dưới cây</th>
                        <th>🏪 Tỷ lệ bán ở Shop</th>
                        <th>🏆 Xếp hạng sức mạnh</th>
                    </tr>
                    <tr>
                        <td style='color:#4ade80;'>{fruit['price_beli']:,} Beli</td>
                        <td style='color:#60a5fa;'>{fruit['price_robux']} Robux</td>
                        <td>{fruit['spawn_chance']}</td>
                        <td>{fruit['stock_chance']}</td>
                        <td style='color:#f59e0b; font-weight:bold;'>Tier {fruit['tier']}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            # NÚT BẤM INTERACTIVE - TƯƠNG TÁC CLICK PHÍM CHIÊU THỨC GIẢ LẬP
            st.write("🎮 **Click để TEST thử chiêu thức (Demo Moveset):**")
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                if st.button(f"Chiêu [Z] của {fruit['name']}", key=f"z_{fruit['name']}"):
                    st.toast(f"💥 {fruit['name']} kích hoạt chiêu Z: Gây sát thương tầm gần, phá Haki quan sát!", icon="⚡")
            with b2:
                if st.button(f"Chiêu [X] của {fruit['name']}", key=f"x_{fruit['name']}"):
                    st.toast(f"☄️ {fruit['name']} kích hoạt chiêu X: Chiêu định hướng tầm xa diện rộng cực đau!", icon="🔥")
            with b3:
                if st.button(f"Chiêu [C] của {fruit['name']}", key=f"c_{fruit['name']}"):
                    st.toast(f"🌪️ {fruit['name']} kích hoạt chiêu C: Khống chế cứng đối thủ tụ lại một chỗ!", icon="🔮")
            with b4:
                if st.button(f"KÍCH HOẠT CHIÊU CUỐI [V]", key=f"v_{fruit['name']}"):
                    st.balloons() # Hiệu ứng pháo hoa bóng bay khi bấm chiêu cuối
                    st.success(f"👑 BẠN ĐÃ GIẢI PHÓNG SỨC MẠNH TỐI THƯỢNG CỦA TRÁI {fruit['name']}! QUÉT SẠCH SERVER!")

# ======================================================================================================================
# DANH MỤC 3: TỶ LỆ SPAWN TRÁI ÁC QUỶ
# ======================================================================================================================
elif menu == "🌲 Tỷ Lệ Spawn Trái Tự Nhiên":
    st.header("🌲 Cơ chế xuất hiện Trái ác quỷ tự nhiên dưới gốc cây")
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("""
        <div class='card' style='border-left: 5px solid #fbbf24;'>
            <h4 style='color:#fbbf24; margin-top:0;'>⏰ Thời gian Spawn chuẩn</h4>
            <p>• <b>Ngày trong tuần (Thứ 2 đến Thứ 6):</b> Cứ mỗi <b>1 tiếng (60 phút)</b> hệ thống sẽ tự động tạo ra 1 trái ngẫu nhiên dưới gốc cây bất kỳ trên bản đồ.</p>
            <p>• <b>Ngày cuối tuần (Thứ 7 và Chủ Nhật):</b> Thời gian rút ngắn xuống còn <b>45 phút</b> một trái.</p>
            <p>• <b>Cơ chế biến mất (Despawn):</b> Nếu không có ai tìm thấy và nhặt, trái ác quỷ sẽ tự động biến mất sau đúng <b>20 phút</b> kể từ lúc xuất hiện.</p>
        </div>
        """, unsafe_allow_html=True)
    with sc2:
        st.markdown("""
        <div class='card' style='border-left: 5px solid #10b981;'>
            <h4 style='color:#10b981; margin-top:0;'>💡 Mẹo săn trái cực nhanh</h4>
            <p>1. <b>Mua Gamepass Fruit Notifier:</b> Bản đồ sẽ tự động hiện thông báo khoảng cách (ví dụ: 1200m) dẫn thẳng tới gốc cây có trái ác quỷ.</p>
            <p>2. <b>Săn tại Server VIP (Private Server):</b> Một mình bạn một server sẽ không sợ bị các người chơi khác hoặc hacker bay nhặt mất.</p>
            <p>3. <b>Canh Server Mới:</b> Khi một server mới tinh vừa khởi chạy, hệ thống luôn sinh ra sẵn một trái ác quỷ ngay lập tức.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.subheader("📊 Bảng thống kê tỷ lệ phân phối theo độ hiếm")
    spawn_data = {
        "Độ Hiếm Trái": ["Common (Thường)", "Uncommon (Không phổ biến)", "Rare (Hiếm)", "Legendary (Huyền thoại)", "Mythical (Thần thoại)"],
        "Tỷ Lệ Xuất Hiện Tự Nhiên": ["~ 50%", "~ 30%", "~ 12% đến 15%", "~ 5% đến 7%", "Dưới 1% (Cực kỳ hiếm)"],
        "Trái Tiêu Biểu": ["Rocket, Spin, Chop", "Flame, Ice, Sand", "Light, Magma, Ghost", "Buddha, Portal, Rumble", "Kitsune, Dragon, Dough, T-Rex"]
    }
    st.table(pd.DataFrame(spawn_data))

# ======================================================================================================================
# DANH MỤC 4: BẢNG XẾP HẠNG TIER LIST
# ======================================================================================================================
elif menu == "⚔️ Bảng Xếp Hạng Sức Mạnh (Tier List)":
    st.header("⚔️ Bảng Xếp Hạng Trái Ác Quỷ Toàn Diện")
    st.write("Bảng xếp hạng dựa trên meta thực tế mới nhất từ các game thủ chuyên nghiệp.")
    
    t1, t2 = st.tabs(["🔥 Chuyên đi PvP / Săn Bounty", "🌾 Chuyên đi Treo Máy Cày Cấp (Farm Level)"])
    
    with t1:
        st.markdown("""
        <div class='card'><b>Tier SS (Bá chủ):</b> Kitsune, Dragon, Dough V2, Leopard.<br><span style='color:#94a3b8;'>→ Ưu điểm: Bộ chiêu thức sát thương khủng, dễ trúng, phá giáp chân đối phương, rất khó bị khắc chế.</span></div>
        <div class='card'><b>Tier A (Tốt):</b> Portal, Rumble, T-Rex, Ice V2.<br><span style='color:#94a3b8;'>→ Ưu điểm: Đòi hỏi kỹ năng combo căn phím tay nhanh, kết hợp linh hoạt giữa Kiếm và Súng.</span></div>
        """, unsafe_allow_html=True)
        
    with t2:
        st.markdown("""
        <div class='card' style='border-left: 5px solid #10b981;'><b>HẠNG 1 TUYỆT ĐỐI: Buddha (Phật Tổ Thức Tỉnh)</b><br><span style='color:#94a3b8;'>→ Ưu điểm: Đứng im một chỗ bật nút biến khổng lồ lên rồi bấm chuột click vả liên thanh, quét sạch quái đảo cực kỳ an toàn và nhanh chóng. Không có trái nào thay thế được.</span></div>
        <div class='card'><b>HẠNG 2: Magma V2, Light, Blizzard</b><br><span style='color:#94a3b8;'>→ Ưu điểm: Có nhiều chiêu thức đánh lan diện rộng (AoE), gom quái nhanh mà không làm đẩy quái ra xa.</span></div>
        """, unsafe_allow_html=True)

# ======================================================================================================================
# DANH MỤC 5: MÁY TÍNH GIAO DỊCH (TRADE CALCULATOR)
# ======================================================================================================================
elif menu == "🧮 Máy Tính Định Giá Trade Trái":
    st.header("🧮 Trình máy tính kiểm tra biên độ giá Giao dịch (Trade)")
    st.write("Trong Blox Fruits, bạn không được phép giao dịch hai bên lệch nhau quá **40% giá trị tiền mặt sàn**. Hãy nhập thử để kiểm tra hệ thống!")
    
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("🛒 Phía Trái Của Bạn")
        my_choice = st.selectbox("Bạn bỏ trái gì vào bàn cân:", [f["name"] for f in FRUIT_DATA], key="my_f")
        my_qty = st.number_input("Số lượng (1-4):", min_value=1, max_value=4, value=1, key="my_q")
        my_total = next(f["price_beli"] for f in FRUIT_DATA if f["name"] == my_choice) * my_qty
        st.metric("Tổng giá trị Beli sàn của bạn:", f"{my_total:,} Beli")
        
    with c_right:
        st.subheader("🤝 Phía Trái Đối Phương")
        their_choice = st.selectbox("Đối phương bỏ trái gì vào đổi:", [f["name"] for f in FRUIT_DATA], key="th_f")
        their_qty = st.number_input("Số lượng (1-4):", min_value=1, max_value=4, value=1, key="th_q")
        their_total = next(f["price_beli"] for f in FRUIT_DATA if f["name"] == their_choice) * their_qty
        st.metric("Tổng giá trị Beli sàn đối phương:", f"{their_total:,} Beli")
        
    st.markdown("---")
    st.subheader("⚖️ Kết quả kiểm tra từ Thẩm định viên Wiki")
    
    # Tính toán phần trăm chênh lệch
    diff = abs(my_total - their_total)
    max_val = max(my_total, their_total)
    percent = (diff / max_val) * 100
    
    if percent > 40:
        st.error(f"❌ KHÔNG HỢP LỆ: Hai bên đang chênh lệch giá sàn lên tới {percent:.1f}%. Hệ thống game Blox Fruits sẽ chặn nút CONFIRM và KHÔNG cho bạn trade kèo này!")
    else:
        st.success(f"✅ HỢP LỆ: Mức độ chênh lệch chỉ {percent:.1f}% (Nằm trong biên độ cho phép < 40%). Bạn hoàn toàn có thể bấm xác nhận giao dịch trong game.")
