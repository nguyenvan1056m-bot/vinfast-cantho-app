import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time
import io
# --- 1. CẤU HÌNH FILE DỮ LIỆU ---
st.set_page_config(page_title="VFG CT-SERVICE - VinFast", layout="wide")

PRICE_FILE = "gia_xe_master.csv"
REG_FILE = "chi_phi_dang_ky.csv"    
POLICY_FILE = "chinh_sach_uu_dai.csv" 
DATA_FILE = "danh_sach_khach_hang.csv"
INSURANCE_FILE = "bang_phi_bao_hiem.csv"
KM_FILE = "chuong_trinh_khuyen_mai.csv"
TRACKING_FILE = "data_theo_doi_xe.csv"
LN_FILE = "data_loi_nhuan.csv"
QT_FILE = "data_quyet_toan.csv"
CPK_FILE = 'data_chi_phi_khac.csv'
COLS_ORDER = [
    "Ngày", "Họ Tên", "SĐT", "CCCD", "Địa chỉ", "Xe", "Bản", "Màu", "Chính Sách", "Quà Tặng",
    "Giá Sau Ưu Đãi","Tiền Đăng Ký", "Tổng Tiền", "Trạng Thái", "Ghi Chú"
]
def init_data():
    if not os.path.exists(PRICE_FILE):
        df_p = pd.DataFrame([
            {"Dòng Xe": "VF 3", "Phiên Bản": "Base", "Giá Niêm Yết": 322000000},
            {"Dòng Xe": "VF 7", "Phiên Bản": "Plus", "Giá Niêm Yết": 999000000}
        ])
        df_p.to_csv(PRICE_FILE, index=False, encoding='utf-8-sig')
    
    if not os.path.exists(REG_FILE):
        df_r = pd.DataFrame([
            {"Hạng mục": "Lệ phí trước bạ (%)", "Giá trị": 0},
            {"Hạng mục": "Phí biển số (Cần Thơ)", "Giá trị": 1000000},
            {"Hạng mục": "Phí đăng kiểm", "Giá trị": 340000},
            {"Hạng mục": "Phí đường bộ (1 năm)", "Giá trị": 1560000}
        ])
        df_r.to_csv(REG_FILE, index=False, encoding='utf-8-sig')

    if not os.path.exists(POLICY_FILE):
        df_po = pd.DataFrame([
            {"Tên Chương Trình": "Không Áp Dụng", "Số Tiền": 0},
            {"Tên Chương Trình": "VF3 Giảm TC 1", "Số Tiền": 3000000}
        ])
        df_po.to_csv(POLICY_FILE, index=False, encoding='utf-8-sig')

    if not os.path.exists(INSURANCE_FILE):
        df_i = pd.DataFrame([
            {"Loại xe": "Xe dưới 6 chỗ", "Mức phí (VNĐ)": 480700},
            {"Loại xe": "Xe từ 6 - 11 chỗ", "Mức phí (VNĐ)": 873400}
        ])
        df_i.to_csv(INSURANCE_FILE, index=False, encoding='utf-8-sig')
    if not os.path.exists(KM_FILE):
        df_empty = pd.DataFrame(columns=['Tên chương trình', 'Giá trị (VNĐ)', 'Trạng thái'])
        df_empty.loc[0] = ["Tặng bộ phụ kiện 5 món", 0, "Kích hoạt"]
        df_empty.to_csv(KM_FILE, index=False)
    

# Đường dẫn file của bạn
    #QT_FILE = 'data_quyet_toan.csv'

    # Kiểm tra: Nếu file tồn tại thì đọc, nếu chưa có thì tạo mới
    if not os.path.exists(QT_FILE):
        df_t = pd.DataFrame(columns=['Tên quyết toán ', 'Giá trị (VNĐ)'])
        # Lưu file rỗng này xuống ổ cứng
        df_t.to_csv(QT_FILE, index=False, encoding='utf-8-sig')
    # Thêm một dòng mẫu để bạn dễ hình dung
    if not os.path.exists(CPK_FILE):
        df_t = pd.DataFrame(columns=['Nội dung ', 'Số tiền (VNĐ)'])
        # Lưu file rỗng này xuống ổ cứng
        df_t.to_csv(CPK_FILE, index=False, encoding='utf-8-sig')   

init_data()

# --- 2. QUẢN LÝ TRẠNG THÁI ---
if 'page' not in st.session_state: st.session_state.page = "Tiếp Nhận"
if 'current_customer' not in st.session_state: st.session_state.current_customer = {}

# --- 3. MENU ĐIỀU HƯỚNG ---
st.markdown(f"### BAN HANG VINFAST | {datetime.now().strftime('%d/%m/%Y')}")

# Chia lại thành 6 cột để thêm tab Theo Dõi
c_nav1, c_nav2, c_nav3, c_nav4, c_nav5, c_nav6, c_nav7 = st.columns(7)

if c_nav1.button("👋 TIẾP NHẬN", use_container_width=True): 
    st.session_state.page = "Tiếp Nhận"; st.rerun()
if c_nav2.button("💰 BÁO GIÁ", use_container_width=True): 
    st.session_state.page = "Báo Giá"; st.rerun()
if c_nav3.button("⚙️ QUẢN LÝ", use_container_width=True): 
    st.session_state.page = "Quản Lý Giá"; st.rerun()
if c_nav4.button("📊 QUYẾT TOÁN", use_container_width=True): 
    st.session_state.page = "Quyết Toán"; st.rerun()
if c_nav5.button("📝 DANH SÁCH", use_container_width=True): 
    st.session_state.page = "Danh Sách"; st.rerun()
# TAB MỚI THÊM VÀO ĐÂY
if c_nav6.button("📈 THEO DÕI XE", use_container_width=True): 
    st.session_state.page = "Theo Dõi"; st.rerun()
if c_nav7.button("📈 LỢI NHUẬN", use_container_width=True): 
    st.session_state.page = "Lợi Nhuận"; st.rerun()
st.divider()

# --- 3. TRANG TIẾP NHẬN ---
if st.session_state.page == "Tiếp Nhận":
    st.subheader("📝 Phiếu Tiếp Nhận Khách Hàng")
    
    # --- 1. KHỞI TẠO BIẾN 'k' ĐẦU TRANG ---
    if 'reset_key' not in st.session_state:
        st.session_state.reset_key = 0
    k = st.session_state.reset_key

    # --- 2. ĐỌC DỮ LIỆU GỐC ---
    df_p = pd.read_csv(PRICE_FILE)
    df_po = pd.read_csv(POLICY_FILE)
    df_i = pd.read_csv(INSURANCE_FILE)
    col_policy_name = "Tên Chương Trình" if "Tên Chương Trình" in df_po.columns else df_po.columns[0]

    # --- 3. PHẦN TÌM KIẾM & ÉP DỮ LIỆU (CHỐNG LỖI TYPE ERROR) ---
    info_khach = {}
    if os.path.exists(DATA_FILE):
        try:
            df_history = pd.read_csv(DATA_FILE)
            # Tạo danh sách Tên - SĐT
            list_khach = (df_history['Họ Tên'].astype(str) + " - " + df_history['SĐT'].astype(str)).unique().tolist()
            
            khach_chon = st.selectbox(
                "🔍 Tìm kiếm khách hàng cũ (Gõ tên hoặc SĐT):", 
                options=list_khach,
                index=None, 
                placeholder="Gõ để tìm nhanh khách cũ...",
                key=f"search_box_{k}"
            )
            
            # KHI CHỌN KHÁCH: ÉP DỮ LIỆU CHUỖI ĐỂ HẾT LỖI DÒNG 173
            if khach_chon:
                t_name = khach_chon.split(" - ")[0]
                t_phone = khach_chon.split(" - ")[1]
                match = df_history[(df_history['Họ Tên'].astype(str) == t_name) & (df_history['SĐT'].astype(str) == t_phone)]
                
                if not match.empty:
                    info_khach = match.iloc[-1].to_dict()
                    
                    # Dùng str(... or '') để biến các ô trống (NaN) thành chữ, tránh lỗi TypeError
                    st.session_state[f"name_{k}"] = str(info_khach.get('Họ Tên') or '')
                    st.session_state[f"phone_{k}"] = str(info_khach.get('SĐT') or '')
                    st.session_state[f"address_{k}"] = str(info_khach.get('Địa Chỉ') or '')
                    st.session_state[f"cccd_{k}"] = str(info_khach.get('CCCD') or '')
                    st.session_state[f"mail_{k}"] = str(info_khach.get('Email') or '')
                    st.session_state[f"color_{k}"] = str(info_khach.get('Màu') or '')
                    
                    st.toast(f"✅ Đã nhận diện khách: {t_name}")
        except Exception as e:
            st.error(f"Lỗi đọc file khách cũ: {e}")

    # --- 4. FORM NHẬP LIỆU (SỬ DỤNG KEY ĐÃ ĐƯỢC ÉP DỮ LIỆU) ---
    with st.container(border=True):
        st.markdown("#### 👤 I. Thông tin khách hàng")
        c1, c2, c3 = st.columns(3)
        
        r_name = c1.text_input("Họ và Tên", key=f"name_{k}")
        r_phone = c1.text_input("Số điện thoại (10 số)", key=f"phone_{k}", max_chars=10)
        
        if r_phone:
            if not r_phone.isdigit(): st.error("⚠️ SĐT chỉ được nhập số!")
            elif len(r_phone) != 10: st.warning("👉 SĐT phải có đúng 10 số.")
                
        r_address = c2.text_input("Địa chỉ (Quận/Huyện)", key=f"address_{k}")
        r_cccd = c2.text_input("Số CCCD (12 số)", key=f"cccd_{k}", max_chars=12)
        
        r_mail = c3.text_input("Email", key=f"mail_{k}")
        r_date = c3.date_input("Ngày tiếp nhận", value=datetime.now(), key=f"date_{k}")

        st.divider()
        st.markdown("#### 🚗 II. Xe quan tâm & Chính sách")
        cx1, cx2, cx3 = st.columns(3)
        
        # Nhảy Dòng xe & Phiên bản (Selectbox dùng index)
        list_xe = df_p['Dòng Xe'].unique().tolist()
        xe_cu = info_khach.get('Xe', '')
        idx_xe = list_xe.index(xe_cu) if xe_cu in list_xe else 0
        r_car = cx1.selectbox("Dòng xe", list_xe, index=idx_xe)
        
        list_ver = df_p[df_p['Dòng Xe'] == r_car]['Phiên Bản'].tolist()
        ver_cu = info_khach.get('Bản', '')
        idx_ver = list_ver.index(ver_cu) if ver_cu in list_ver else 0
        r_ver = cx1.selectbox("Phiên bản", list_ver, index=idx_ver)
        
        r_policy = cx2.selectbox("Chương trình ưu đãi", df_po[col_policy_name].tolist())
        r_ins_label = cx2.selectbox("Loại Bảo hiểm DS", df_i['Loại xe'].tolist())
        
        # Ô màu sắc (Dòng 173 đã được bảo vệ bởi str or '')
        r_color = cx3.text_input("Màu sắc ngoại thất", key=f"color_{k}")
        r_status = cx3.selectbox("Trạng thái", ["Tư vấn", "Đã cọc", "Tiền mặt"], index=0)

    # 5. NÚT BẤM XEM BÁO GIÁ
    if st.button("💰 XEM BÁO GIÁ CHI TIẾT", type="primary", use_container_width=True):
        if not r_name or not r_phone:
            st.error("⚠️ Vui lòng nhập Họ tên và Số điện thoại!")
        else:
            pol_val = int(df_po[df_po[col_policy_name] == r_policy].iloc[0, 1])
            ins_val = int(df_i[df_i['Loại xe'] == r_ins_label].iloc[0, 1])
            
            st.session_state.current_customer = {
                "name": r_name, "phone": r_phone, "address": r_address, "cccd": r_cccd,
                "mail": r_mail, "date": r_date, "car": r_car, "ver": r_ver,
                "policy_name": r_policy, "policy_val": pol_val, 
                "ins_label": r_ins_label, "ins_price": ins_val,
                "color": r_color, "status": r_status
            }
            st.session_state.page = "Báo Giá"
            st.rerun()

# --- 4. TRANG BÁO GIÁ (GIAO DIỆN CHUYÊN NGHIỆP THEO MẪU EXCEL) ---
elif st.session_state.page == "Báo Giá":
    q = st.session_state.current_customer

    customer_name = q.get('name', "Khách hàng VIP")
    
    st.subheader(f"📊 BẢNG DỰ TOÁN CHI TIẾT - {customer_name.upper()}")
    # Tại trang Báo giá
    
    df_p = pd.read_csv(PRICE_FILE)
    df_r = pd.read_csv(REG_FILE)
    
    # Lấy giá niêm yết gốc
    base_price_init = 0
    if q.get('car'):
        row = df_p[(df_p['Dòng Xe'] == q['car']) & (df_p['Phiên Bản'] == q['ver'])]
        base_price_init = int(row['Giá Niêm Yết'].values[0]) if not row.empty else 0

    # Hàm bổ trợ lấy số chuẩn từ bảng (khớp tên 100% với bảng Quản lý)
    def get_master_fee(item_name):
        try:
            val = df_r[df_r['Hạng mục'] == item_name]['Giá trị'].values[0]
            return int(val)
        except:
            return 0

    # --- BẮT ĐẦU CHIA CỘT TÍNH TOÁN ---
    col_input, col_display = st.columns([1, 2])

    with col_input:
        st.markdown("### ⚙️ Cài đặt thông số")
        
        with st.expander("1. Giá xe & Ưu đãi", expanded=True):
            edit_base = st.number_input("Giá niêm yết (VNĐ)", value=base_price_init, step=1000000)
            edit_discount_main = st.number_input("Ưu đãi/Voucher (VNĐ)", value=q.get('policy_val', 0), step=500000)
            edit_discount_extra = st.number_input("Giảm giá % (VNĐ)", value=q.get('add_discount', 0), step=500000)
            gia_ban_sau_uu_dai = edit_base - edit_discount_main - edit_discount_extra

    # Đọc dữ liệu gốc
        # --- PHẦN KHUYẾN MÃI TỰ ĐỘNG ---
        with st.expander("🎁 2. Chương trình", expanded=True):
            selected_km_data = []
            tong_tri_gia_qt = 0 # Biến để tính tổng tiền quà tặng
            
            # 1. Đọc dữ liệu từ file khuyến mãi
            try:
                df_km = pd.read_csv('chuong_trinh_khuyen_mai.csv')
            except:
                df_km = pd.DataFrame(columns=['Tên chương trình', 'Giá trị (VNĐ)'])

            if df_km.empty:
                st.info("Chưa có quà tặng nào được cấu hình.")
            else:
                # TẠO TIÊU ĐỀ CỘT (Giống ảnh bạn muốn)
                h1, h2 = st.columns([3, 1])
                h1.caption("TÊN CHƯƠNG TRÌNH")
                h2.caption("SỐ TIỀN (VNĐ)")
                st.divider()

                # 2. Duyệt từng dòng để tạo hàng (Row)
                for i, (idx, row) in enumerate(df_km.iterrows()):
                    km_name = str(row['Tên chương trình'])
                    # Xử lý ép kiểu số an toàn
                    km_val = pd.to_numeric(row['Giá trị (VNĐ)'], errors='coerce')
                    km_val = int(km_val) if pd.notna(km_val) else 0
                    
                    # CHIA CỘT THEO TỶ LỆ 3:1
                    c_left, c_right = st.columns([3, 1])
                    
                    # Cột trái: Checkbox chọn quà
                    with c_left:
                        # Dùng key='qt_' để nút lưu tự quét được
                        is_checked = st.checkbox(km_name, value=False, key=f"qt_{km_name}")
                    
                    # Cột phải: Hiển thị số tiền tương ứng
                    with c_right:
                        if is_checked:
                            st.write(f"**{km_val:,.0f}**")
                            tong_tri_gia_qt += km_val
                            selected_km_data.append({"label": km_name, "value": km_val})
                        else:
                            st.write("0")
                
                # 3. HIỂN THỊ TỔNG CỘNG Ở DƯỚI CÙNG
                

            # Lưu vào session_state để sử dụng cho các trang khác
            st.session_state.selected_km_list = selected_km_data
            st.session_state.total_km_value = tong_tri_gia_qt
        # --- HIỂN THỊ BẢNG TỔNG HỢP QUÀ TẶNG ---
        
        with st.expander("3. Chi phí đăng ký ", expanded=True):
            # Khởi tạo danh sách phí được chọn và tổng tiền
            selected_fees_data = []
            tong_chi_phi_dk = 0
            
            # 1. Lấy riêng Thuế trước bạ vì nó tính theo % giá xe
            try:
                thue_row = df_r[df_r['Hạng mục'].str.contains("Thuế trước bạ|Lệ phí trước bạ", case=False, na=False)]
                thue_pct = int(thue_row['Giá trị'].values[0])
                thue_val = int(gia_ban_sau_uu_dai * thue_pct / 100)
                
                if st.checkbox(f"Thuế trước bạ ({thue_pct}%) - {thue_val:,} VNĐ", value=True, key="cb_thue"):
                    selected_fees_data.append({"label": "Thuế trước bạ", "value": thue_val})
                    tong_chi_phi_dk += thue_val
            except: pass

            st.divider() # Ngăn cách giữa Thuế và các phí cố định

            # 2. Tự động tạo Checkbox cho TẤT CẢ các hàng còn lại trong file CSV
            # Bỏ qua dòng Thuế (vì đã tính ở trên) và dòng có giá trị bằng 0
            # 2. Tự động quét TẤT CẢ các hàng còn lại từ bảng Quản lý
            df_other_fees = df_r[~df_r['Hạng mục'].str.contains("%", na=False)]
            
            c_auto1, c_auto2 = st.columns(2)
            for i, (idx, row) in enumerate(df_other_fees.iterrows()):
                item_name = row['Hạng mục']
                
                # --- ĐOẠN SỬA LỖI TẠI ĐÂY ---
                try:
                    # Dùng pd.to_numeric để xử lý ô trống (NaN) biến nó thành 0
                    item_val = int(pd.to_numeric(row['Giá trị'], errors='coerce'))
                    if pd.isna(item_val): item_val = 0
                except:
                    item_val = 0
                # -----------------------------

                if item_val >= 0: # Hiện cả những mục có giá trị 0 nếu cần
                    target_col = c_auto1 if i % 2 == 0 else c_auto2
                    # Tạo checkbox cho từng hạng mục
                    if target_col.checkbox(f"{item_name} ({item_val:,} VNĐ)", value=False, key=f"auto_cb_{idx}"):
                        selected_fees_data.append({"label": item_name, "value": item_val})
                        tong_chi_phi_dk += item_val
            # 3. Thêm Bảo hiểm TNDS (lấy từ trang Tiếp nhận)
            bhds_val = q.get('ins_price', 0)
            if bhds_val > 0:
                if st.checkbox(f"Bảo hiểm TNDS ({bhds_val:,} VNĐ)", value=True, key="cb_bhds"):
                    selected_fees_data.append({"label": "Bảo hiểm TNDS", "value": bhds_val})
                    tong_chi_phi_dk += bhds_val
        gia_thuc_te_xe = q.get('Giá Sau Ưu Đãi', 0)
       
        with st.expander("4. Phương thức Ngân hàng", expanded=True):
            vay_percent = st.slider("Tỷ lệ vay (%)", 0, 100, 85)
            so_tien_vay = int(gia_ban_sau_uu_dai * vay_percent / 100)
            tra_truoc_xe = gia_ban_sau_uu_dai - so_tien_vay
            st.session_state['so_tien_vay_shared'] = so_tien_vay
            st.session_state['tra_truoc_xe_shared'] = tra_truoc_xe
        st.session_state['gia_sau_uu_dai_shared'] = gia_ban_sau_uu_dai 

        # 2. Lưu đúng TỔNG CHI PHÍ ĐĂNG KÝ (Dòng 20 Quyết toán)
        st.session_state['chi_phi_dk_shared'] = tong_chi_phi_dk
        
        # 3. Lưu thông tin vay vốn (Để hiện bên Tab Ngân hàng)
        
        st.session_state['vay_percent_shared'] = vay_percent

    with col_display:
        # --- PHẦN 1: GIÁ BÁN ---
        st.markdown(f"#### 🚗 DÒNG XE: {q.get('car', '...')} ({q.get('ver', '...')})")
        df_price_summary = pd.DataFrame({
            "DIỄN GIẢI": ["GIÁ NIÊM YẾT", f"Ưu đãi ({q.get('policy_name', 'Chương trình')})", "Giảm thêm khuyến mãi", "GIÁ BÁN SAU ƯU ĐÃI (1)"],
            "THÀNH TIỀN (VNĐ)": [f"{edit_base:,}", f" {edit_discount_main:,}", f" {edit_discount_extra:,}", f"{gia_ban_sau_uu_dai:,}"]
        })
        st.table(df_price_summary)

        # --- PHẦN 2: CHI PHÍ ĐĂNG KÝ ---
       
        if selected_km_data:
            st.markdown("#### 🎁 CHI TIẾT QUÀ TẶNG & KHUYẾN MÃI")
            df_km_display = pd.DataFrame({
                "STT": range(1, len(selected_km_data) + 1),
                "NỘI DUNG ƯU ĐÃI": [x['label'] for x in selected_km_data],
                "GHI CHÚ": ["Đã áp dụng" for _ in selected_km_data]
            })
            st.data_editor(
                df_km_display,
                column_config={
                    "STT": st.column_config.NumberColumn("STT", width=30),
                    "NỘI DUNG ƯU ĐÃI": st.column_config.TextColumn(
                        label="NỘI DUNG ƯU ĐÃI",
                        width=900
                    ),
                },
                hide_index=True,
                use_container_width=True,
                disabled=True
            )
            
            col_total_label, col_total_val = st.columns([3, 1])
            col_total_label.markdown("### 🏆 TỔNG TRỊ GIÁ QUÀ TẶNG:")
            col_total_val.markdown(f"### {tong_tri_gia_qt:,.0f} đ")
            st.divider()
        # --- PHẦN HIỂN THỊ BẢNG (CHUẨN THẨM MỸ SHOWROOM) ---
        st.markdown("#### 📝 CHI TIẾT CÁC KHOẢN LỆ PHÍ ĐÃ CHỌN")
        
        # --- PHẦN HIỂN THỊ BẢNG (ĐÃ THU NHỎ CỘT STT) ---
        # --- PHẦN HIỂN THỊ BẢNG (FIX CỨNG ĐỘ RỘNG) ---
        if selected_fees_data:
            df_final = pd.DataFrame({
                "STT": [str(i) for i in range(1, len(selected_fees_data) + 1)],
                "CÁC KHOẢN LỆ PHÍ": [x['label'] for x in selected_fees_data],
                "THÀNH TIỀN (VNĐ)": [x['value'] for x in selected_fees_data]
            })
            
            st.data_editor(
                df_final,
                column_config={
                    "STT": st.column_config.TextColumn(
                        "STT",
                        width=30,
                        help="Số thứ tự",
                    ),
                    "CÁC KHOẢN LỆ PHÍ": st.column_config.TextColumn(
                        label="CÁC KHOẢN LỆ PHÍ",
                        width=1000 # Cho cột này rộng ra để "gánh" diện tích bảng
                    ),
                    "THÀNH TIỀN (VNĐ)": st.column_config.NumberColumn(
                        label="THÀNH TIỀN (VNĐ)",
                        format="%d",
                        width=180
                    ),
                },
                hide_index=True,
                use_container_width=True, # TẮT TÍNH NĂNG TỰ GIÃN CÁCH ĐỂ WIDTH CÓ TÁC DỤNG
                disabled=True 
            )
        else:
            st.info("Chưa chọn khoản lệ phí nào.")
        # --- PHẦN 3: PHƯƠNG THỨC THANH TOÁN ---
        tab_cash, tab_bank = st.tabs(["💵 I. PHƯƠNG THỨC TIỀN MẶT", "🏦 II. PHƯƠNG THỨC NGÂN HÀNG"])

# --- CHUẨN BỊ DỮ LIỆU CHUNG (Tính toán trước khi vào Tab) ---
        q = st.session_state.current_customer
        tong_tien_mat = gia_ban_sau_uu_dai + tong_chi_phi_dk + tong_tri_gia_qt
        # Giả sử bạn đã có biến so_tien_vay, tra_truoc_xe, vay_percent từ phần code trước đó
        tong_tra_truoc_nh_ = tra_truoc_xe + tong_chi_phi_dk
        st.session_state['nho_gia_chot'] = gia_ban_sau_uu_dai
        st.session_state['nho_phi_dk'] = tong_chi_phi_dk
        st.session_state['nho_tong_tien'] = tong_tien_mat
        # --- NỘI DUNG TAB TIỀN MẶT ---
        with tab_cash:
            st.write(f"1. Tiền xe (1): **{gia_ban_sau_uu_dai:,} VNĐ**")
            st.write(f"2. Chi phí đăng ký (2): **{tong_chi_phi_dk:,} VNĐ**")
            st.write(f"3. Chi phí chương trình (3): **{tong_tri_gia_qt:,} VNĐ**")
            st.markdown(f"<h3 style='color: red;'>TỔNG CỘNG (1)+(2)+(3): {tong_tien_mat:,} VNĐ</h3>", unsafe_allow_html=True)

        # --- NỘI DUNG TAB NGÂN HÀNG (ĐÃ THÊM CODE VÀO ĐÂY) ---
        with tab_bank:
           
    # Tính toán lại một lần nữa cho chắc chắn trước khi hiện
            tong_tra_truoc_nh = tra_truoc_xe + tong_chi_phi_dk
            
            st.write(f"1. Ngân hàng hỗ trợ ({vay_percent}%): **{so_tien_vay:,} VNĐ**")
            st.write(f"2. Khách trả trước xe ({100-vay_percent}%): **{tra_truoc_xe:,} VNĐ**")
            st.write(f"3. Chi phí đăng ký: **{tong_chi_phi_dk:,} VNĐ**")
            
            # Sử dụng đúng tên biến đã tính ở trên
            st.markdown(f"<h3 style='color: #1E90FF;'>TỔNG TIỀN TRẢ TRƯỚC: {tong_tra_truoc_nh:,} VNĐ</h3>", unsafe_allow_html=True)
            st.caption("*(Số tiền này bao gồm phần đối ứng xe và toàn bộ chi phí lăn bánh)*")
                # --- PHẦN XUẤT EXCEL (Đưa ra ngoài Tab để hiện ở dưới cùng của cả 2 phương thức) ---
        import io
        import pandas as pd
        from datetime import datetime

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook  = writer.book
            worksheet = workbook.add_worksheet('Bao_Gia_VinFast')

            # --- ĐỊNH DẠNG (STYLES) ---
            header_fmt = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 14})
            title_blue = workbook.add_format({'bold': True, 'bg_color': '#DDEBF7', 'border': 1, 'align': 'center'})
            label_fmt = workbook.add_format({'border': 1, 'bold': True})
            money_fmt = workbook.add_format({'num_format': '#,##0', 'border': 1, 'align': 'right'})
            total_yellow = workbook.add_format({'bold': True, 'bg_color': '#FFFF00', 'border': 1, 'align': 'right', 'font_color': 'red'})
            italic_fmt = workbook.add_format({'italic': True, 'align': 'center'})

            # --- VẼ GIAO DIỆN EXCEL ---
            worksheet.merge_range('A1:C1', 'BẢNG BÁO GIÁ VÀ DỰ TRÙ CHI PHÍ ĐĂNG KÝ XE', header_fmt)
            worksheet.merge_range('A2:C2', f"Ngày {datetime.now().day} tháng {datetime.now().month} năm {datetime.now().year}", italic_fmt)

            # I. PHẦN GIÁ XE
            worksheet.write('A3', 'DÒNG XE', title_blue)
            worksheet.merge_range('B3:C3', f"{q.get('car', q.get('Xe', '')).upper()}", title_blue)

            worksheet.write('A4', 'GIÁ NIÊM YẾT', label_fmt)
            worksheet.write('B4', edit_base, money_fmt)
            worksheet.write('C4', 'VNĐ', label_fmt)

            worksheet.write('A5', f"Ưu đãi {q.get('policy_name', '')}", label_fmt)
            worksheet.write('B5', edit_discount_main, money_fmt)
            worksheet.write('C5', 'VNĐ', label_fmt)

            worksheet.write('A6', 'GIÁ BÁN SAU ƯU ĐÃI', total_yellow)
            worksheet.write('B6', gia_ban_sau_uu_dai, total_yellow)
            worksheet.write('C6', 'VNĐ', total_yellow)

            # II. CÁC KHOẢN LỆ PHÍ
            worksheet.write('A8', 'STT', title_blue)
            worksheet.write('B8', 'CÁC KHOẢN LỆ PHÍ', title_blue)
            worksheet.write('C8', 'THÀNH TIỀN (VNĐ)', title_blue)

            row_idx = 8
            for i, fee in enumerate(selected_fees_data, 1):
                worksheet.write(row_idx, 0, i, label_fmt)
                worksheet.write(row_idx, 1, fee['label'], label_fmt)
                worksheet.write(row_idx, 2, fee['value'], money_fmt)
                row_idx += 1

            worksheet.write(row_idx, 1, 'TỔNG CHI PHÍ ĐĂNG KÝ', total_yellow)
            worksheet.write(row_idx, 2, tong_chi_phi_dk, total_yellow)

            # III. PHƯƠNG THỨC THANH TOÁN
            row_idx += 2
            worksheet.merge_range(row_idx, 0, row_idx, 2, 'I. PHƯƠNG THỨC MUA TIỀN MẶT', title_blue)
            worksheet.write(row_idx+1, 0, 'Tiền xe (1)', label_fmt)
            worksheet.write(row_idx+1, 2, gia_ban_sau_uu_dai, money_fmt)
            worksheet.write(row_idx+2, 0, 'Chi phí đăng ký (2)', label_fmt)
            worksheet.write(row_idx+2, 2, tong_chi_phi_dk, money_fmt)
            worksheet.write(row_idx+3, 1, 'Tổng cộng (1) + (2)', total_yellow)
            worksheet.write(row_idx+3, 2, tong_tien_mat, total_yellow)

            row_idx += 5
            worksheet.merge_range(row_idx, 0, row_idx, 2, 'II. PHƯƠNG THỨC MUA QUA NGÂN HÀNG', title_blue)
            worksheet.write(row_idx+1, 0, f'Ngân hàng hỗ trợ {vay_percent}%', label_fmt)
            worksheet.write(row_idx+1, 2, so_tien_vay, money_fmt)
            worksheet.write(row_idx+2, 0, f'Trả trước xe (1)', label_fmt)
            worksheet.write(row_idx+2, 2, tra_truoc_xe, money_fmt)
            worksheet.write(row_idx+3, 1, 'Tổng số tiền trả trước (1) + (ĐK)', total_yellow)
            worksheet.write(row_idx+3, 2, tong_tra_truoc_nh_, total_yellow)

            worksheet.set_column('A:A', 25); worksheet.set_column('B:B', 35); worksheet.set_column('C:C', 20)
            worksheet.hide_gridlines(2)

        st.divider()
        st.download_button(
            label="📊 XUẤT BÁO GIÁ MẪU VINFAST",
            data=output.getvalue(),
            file_name=f"Bao_Gia_{q.get('Họ Tên', 'Khach')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
            
    # --- FOOTER ---
    st.divider()
    
    # --- TẠI TRANG BÁO GIÁ (ĐOẠN CUỐI) ---
    if st.button("💾 LƯU HỒ SƠ & QUAY LẠI TIẾP NHẬN", type="primary", use_container_width=True):
        try:
            q = st.session_state.current_customer
            
            # 1. LẤY DỮ LIỆU TỪ BỘ NHỚ TẠM (Đã nạp ở Bước 1)
            # Nếu không có dữ liệu, lấy giá trị 0
            v_gia_chot = st.session_state.get('nho_gia_chot', 0)
            v_phi_dk = st.session_state.get('nho_phi_dk', 0)
            v_tong_tien = st.session_state.get('nho_tong_tien', 0)

            # 2. XỬ LÝ QUÀ TẶNG & NGÀY THÁNG
            list_qt = [k.replace("qt_", "") for k, v in st.session_state.items() if k.startswith("qt_") and v == True]
            str_qua_tang = ", ".join(list_qt) if list_qt else "Không có"
            raw_date = q.get('date', datetime.now())
            str_ngay = raw_date.strftime("%d/%m/%Y") if hasattr(raw_date, 'strftime') else str(raw_date)

            # 3. TẠO DÒNG DỮ LIỆU CHUẨN
            final_data = {
                "Ngày": str_ngay,
                "Họ Tên": q.get('name', 'N/A'),
                "SĐT": q.get('phone', ''),
                "CCCD": q.get('cccd', ''),
                "Địa Chỉ": q.get('address', ''),
                "Xe": q.get('car', ''),
                "Bản": q.get('ver', ''),
                "Màu": q.get('color', ''),
                "Chính Sách": q.get('policy_name', "Ưu đãi"), 
                "Quà Tặng": str_qua_tang,
                
                # GHI CÁC CON SỐ THỰC TẾ (ÉP KIỂU SỐ NGUYÊN)
                "Giá Sau Ưu Đãi": int(v_gia_chot),
                "Tiền Đăng Ký": int(v_phi_dk),
                "Tổng Tiền": int(v_tong_tien),
                "Tiền Vay": int(so_tien_vay),
                "Trạng Thái": "Đã báo giá",
                "Ghi Chú": ""
            }

            # 4. GHI VÀO FILE CSV (Chống nhân bản nhiều hàng)
            new_row_df = pd.DataFrame([final_data])
            new_row_df.to_csv(DATA_FILE, mode='a', index=False, header=not os.path.exists(DATA_FILE), encoding='utf-8-sig')
            
            # 5. GHI VÀO FILE LỢI NHUẬN
            ln_row = {
                "STT": 0, # Bạn có thể dùng len(df)+1 nếu cần
                "NGÀY XHĐ": str_ngay,
                "Khách Hàng": q.get('name', 'N/A'),
                "Giá Chốt": int(v_gia_chot),
                "Tiền Đăng Ký": int(v_phi_dk),
                "Hoa Hồng Bank": 0, "Hoa Hồng HTX": 0, "Hoa Hồng": 0,
                "LỢI NHUẬN": 0
            }
            pd.DataFrame([ln_row]).to_csv(LN_FILE, mode='a', index=False, header=not os.path.exists(LN_FILE), encoding='utf-8-sig')

            st.success(f"✅ Đã lưu khách hàng {q.get('name')} thành công!")
            time.sleep(1)
            # Ngắt logic để không bị lưu lặp lại và quay về trang đầu
            st.session_state.page = "Tiếp Nhận"
            st.rerun()

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")
# --- 6. TRANG QUẢN LÝ ---
elif st.session_state.page == "Quản Lý Giá":
    st.subheader("⚙️ Cấu Hình Thông Số")
    t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🚗 Bảng Giá Xe", "📜 Chi Phí Đăng Ký", "🎁 Chính Sách", "🛡️ Bảng Phí Bảo Hiểm", "Chương trình khuyến mãi","Quyết toán CT","Quyết toán KH"])
    
    with t1:
        df_p = pd.read_csv(PRICE_FILE)
        ed_p = st.data_editor(df_p, num_rows="dynamic", use_container_width=True, key="p_ed")
        if st.button("💾 Lưu Bảng Giá"):
            ed_p.to_csv(PRICE_FILE, index=False, encoding='utf-8-sig'); st.success("Đã lưu!"); time.sleep(0.5); st.rerun()
    with t2:
        df_r = pd.read_csv(REG_FILE)
        ed_r = st.data_editor(df_r,num_rows="dynamic", use_container_width=True, key="r_ed")
        if st.button("💾 Lưu Chi Phí"):
            ed_r.to_csv(REG_FILE, index=False, encoding='utf-8-sig'); st.success("Đã lưu!"); time.sleep(0.5); st.rerun()
    with t3:
        df_po = pd.read_csv(POLICY_FILE)
        ed_po = st.data_editor(df_po, num_rows="dynamic", use_container_width=True, key="po_ed")
        if st.button("💾 Lưu Chính Sách"):
            ed_po.to_csv(POLICY_FILE, index=False, encoding='utf-8-sig'); st.success("Đã lưu!"); time.sleep(0.5); st.rerun()
    with t4:
        df_i = pd.read_csv(INSURANCE_FILE)
        ed_i = st.data_editor(df_i, num_rows="dynamic", use_container_width=True, key="i_ed")
        if st.button("💾 Lưu Bảng Phí Bảo Hiểm"):
            ed_i.to_csv(INSURANCE_FILE, index=False, encoding='utf-8-sig'); st.success("Đã lưu!"); time.sleep(0.5); st.rerun()
    with t5:
        df_k = pd.read_csv(KM_FILE)
        ed_k = st.data_editor(df_k, num_rows="dynamic", use_container_width=True, key="k_ed")
        if st.button("💾 Lưu Chương Trình Khuyến Mãi"):
            ed_k.to_csv(KM_FILE, index=False, encoding='utf-8-sig'); st.success("Đã lưu!"); time.sleep(0.5); st.rerun()
    with t6:
        QT_FILE = 'data_quyet_toan.csv'
        
        # Đọc dữ liệu và ép tên cột về chuẩn ngay lập tức
        if os.path.exists(QT_FILE):
            df_t = pd.read_csv(QT_FILE)
            # Xóa khoảng trắng thừa ở đầu/cuối tên cột
            df_t.columns = df_t.columns.str.strip() 
        else:
            df_t = pd.DataFrame(columns=["Tên quyết toán", "Giá trị (VNĐ)"])

        # Hiển thị bảng sửa đổi
        ed_t = st.data_editor(df_t, num_rows="dynamic", use_container_width=True, key="t_ed_final")

        if st.button("💾 Lưu cấu hình chuẩn"):
            # Lưu lại với tên cột sạch sẽ
            ed_t.to_csv(QT_FILE, index=False, encoding='utf-8-sig')
            st.success("✅ Đã chuẩn hóa file hệ thống!")
            st.rerun()
    with t7:
        CPK_FILE = 'data_chi_phi_khac.csv'
        
        # Đọc dữ liệu và ép tên cột về chuẩn ngay lập tức
        if os.path.exists(CPK_FILE):
            df_cpk = pd.read_csv(CPK_FILE)
            # Xóa khoảng trắng thừa ở đầu/cuối tên cột
            df_cpk.columns = df_cpk.columns.str.strip() 
        else:
            df_cpk = pd.DataFrame(columns=["Nội dung", "Số tiền (VNĐ)"])

        # Hiển thị bảng sửa đổi
        ed_cpk = st.data_editor(df_cpk, num_rows="dynamic", use_container_width=True, key="ed_chi_phi_khac")

        if st.button("💾 Lưu cấu hình chuẩn", key="btn_luu_chi_phi_khac"):
            # Lưu lại với tên cột sạch sẽ
            ed_cpk.to_csv(CPK_FILE, index=False, encoding='utf-8-sig')
            st.success("✅ Đã chuẩn hóa file hệ thống!")
            st.rerun()
elif st.session_state.page == "Quyết Toán":
    q = st.session_state.current_customer
    st.subheader(f"📑 QUYẾT TOÁN VỚI CÔNG TY - {q.get('name', 'KHÁCH HÀNG').upper()}")
    
    # 1. Lấy giá ưu đãi từ dữ liệu khách hàng
    gia_uu_dai_tu_danh_sach = q.get('Giá Sau Ưu Đãi', 0)
    
    # --- KHỐI TRY/EXCEPT PHẢI THẲNG HÀNG VỚI CÁC LỆNH TRÊN ---
    try:
        if isinstance(gia_uu_dai_tu_danh_sach, str):
            # Xóa dấu phẩy hoặc dấu chấm nếu có (497,260,000 -> 497260000)
            gia_xe_moi = int(gia_uu_dai_tu_danh_sach.replace(',', '').replace('.', ''))
        else:
            gia_xe_moi = int(gia_uu_dai_tu_danh_sach)
    except:
        gia_xe_moi = 0

    # 2. Logic dự phòng lấy giá niêm yết từ file nếu không có giá ưu đãi
    gia_mac_dinh_a = 0
    try:
        df_p = pd.read_csv(PRICE_FILE)
        row_xe = df_p[df_p['Dòng Xe'].str.strip() == q.get('Xe', '').strip()]
        if not row_xe.empty:
            gia_mac_dinh_a = int(row_xe['Giá Niêm Yết'].values[0])
        else:
            gia_mac_dinh_a = int(q.get('Giá Niêm Yết', 0))
    except:
        gia_mac_dinh_a = 0

    

    col_input, col_table = st.columns([1.1, 1])

    with col_input:
        with st.expander("🏢 Cấu hình Giá & Giảm trừ hóa đơn", expanded=True):
            import streamlit as st
            import pandas as pd
            import os

            # Đường dẫn file cấu hình
            QT_FILE = 'data_quyet_toan.csv'

            # Chia cột: Cột trái nhập liệu (6), Cột phải xem bảng (4)
            with st.container(border=True): # Dùng container thay vì expander nếu muốn bảng hiện ra ngay
                    st.subheader("🏢 Cấu hình Giá & Giảm trừ")
                    
                    # 1. Nhập Giá Niêm Yết
                    A = st.number_input(
                        "1. Giá Niêm Yết (A)", 
                        value=int(gia_mac_dinh_a), # Lấy giá tự động đã tìm thấy ở trên
                        step=1000000, 
                        format="%d",
                        key=f"niem_yet_{q.get('name', 'default')}" # Key thay đổi theo tên khách -> Tự nhảy số
                    )
                    tong_giam_tru_hd = 0
                    rows = [["1", "Giá Niêm Yết (A)", f"{A:,}", "A"]]
                    c_vay1, c_vay2 = st.columns([1.5, 2])

                    # --- TRONG MỤC I ---
                    # 1. Lấy số từ túi nhớ
                    val_shared = st.session_state.get('so_tien_vay_shared', 0)

                    c_v1, c_v2 = st.columns([1.5, 2])
                    with c_v1:
                        st.write("")
                        # Dùng Key động {val_shared} cho Checkbox
                        ck_vay_kh = st.checkbox("**Số tiền vay**", value=(val_shared > 0), key=f"ck_vay_final_{val_shared}")
                    with c_v2:
                        # Dùng Key động {val_shared} cho ô nhập tiền
                        val_vay_kh = st.number_input(
                            "Tiền vay KH", 
                            value=int(val_shared), 
                            disabled=not ck_vay_kh, 
                            format="%d", 
                            key=f"val_input_final_{val_shared}", # KEY ĐỔI TÊN THÌ SỐ MỚI NHẢY
                            label_visibility="collapsed"
                        )
                    if ck_vay_kh:
    # 1. Cộng vào tổng giảm trừ để tính ra giá G (XHĐ)
                        tong_giam_tru_hd += val_vay_kh
                        # 2. Đẩy dòng này vào bảng "Chi tiết Quyết toán" bên phải
                        rows.append([str(len(rows)+1), "Số tiền vay ngân hàng", f"-{val_vay_kh:,.0f}", "Vay"])
                    if os.path.exists(QT_FILE):
                        df_config_qt = pd.read_csv(QT_FILE)
                        df_config_qt.columns = df_config_qt.columns.str.strip()
                        
                        for index, row in df_config_qt.iterrows():
                            ten_muc = row['Tên quyết toán']
                            gia_mac_dinh = float(row['Giá trị (VNĐ)'])
                            
                            # Tạo hàng cho mỗi mục: Checkbox (trái) và Ô số (phải)
                            c1, c2 = st.columns([1.5, 2])
                            with c1:
                                is_checked = st.checkbox(f"{ten_muc}", key=f"quote_cb_{index}")
                            with c2:
                                # Ô nhập tiền chỉ hiện/cho sửa khi đã tích chọn
                                val_input = st.number_input(
                                    "Số tiền", # Label sẽ bị ẩn
                                    value=gia_mac_dinh,
                                    key=f"quote_val_{index}",
                                    label_visibility="collapsed",
                                    disabled=not is_checked,
                                    format="%0.f"
                                )
                            
                            if is_checked:
                                tong_giam_tru_hd += val_input
                                rows.append([str(len(rows)+1), ten_muc, f"-{val_input:,.0f}", ""])
                    
                    # Tính toán kết quả cuối cùng
                    G = A - tong_giam_tru_hd
                    rows.append(["G", "**GIÁ HĐ ( XHĐ )**", f"**{G:,.0f}**", "**G = A - Ưu đãi**"])
                    
                    # Lưu vào session_state cho các tính toán khác
                    st.session_state['nho_gia_chot'] = G

           
                

            with col_table:
                with st.container(border=True):
                    st.markdown("### 📋 Chi tiết Quyết toán")
                    
                    # Hiển thị bảng (Dùng st.dataframe để giao diện hiện đại hơn st.table)
                    st.table(pd.DataFrame(rows, columns=["STT", "Nội dung", "Số tiền (VNĐ)", "Note"]))
                    
                    # Thông báo tổng tiền
                    st.error(f"### TỔNG THU (G): {G:,.0f} VNĐ")
                    
                    # Nút bấm lưu hồ sơ
                    if st.button("💾 Lưu hồ sơ khách hàng", use_container_width=True, type="primary"):
                        # Thêm code lưu vào file data_khach_hang.csv của bạn ở đây
                        st.toast("Đang lưu hồ sơ...", icon="⏳")
                        st.success("Đã lưu hồ sơ thành công!")
            # Hiển thị Tổng cộng to rõ
#    G = A - val_b - val_d - val_e - val_f
#    I = G - 0  # Nếu có giảm trừ thêm thì trừ ở đây, nếu không I = G

    # --- MỤC II: QUYẾT TOÁN VỚI KHÁCH HÀNG ---
    st.subheader(f"👤 II. QUYẾT TOÁN VỚI KHÁCH HÀNG")
    col_kh_in, col_kh_out = st.columns([1.1, 1], gap="large")

    with col_kh_in:
        with st.expander("📂 Chi phí Đăng ký & Đối ứng", expanded=True):
            tong_kh_giam_tru = 0
            tong_kh_cong_them = 0
            data_selected_cp = []
            gia_uu_dai_tu_danh_sach = q.get('Giá Sau Ưu Đãi', 0)
        
        # --- KHỐI TRY/EXCEPT PHẢI THẲNG HÀNG VỚI CÁC LỆNH TRÊN ---
            try:
                if isinstance(gia_uu_dai_tu_danh_sach, str):
                    # Xóa dấu phẩy hoặc dấu chấm nếu có (497,260,000 -> 497260000)
                    gia_xe_moi = int(gia_uu_dai_tu_danh_sach.replace(',', '').replace('.', ''))
                else:
                    gia_xe_moi = int(gia_uu_dai_tu_danh_sach)
            except:
                gia_xe_moi = 0
        # 1. Lấy giá trị G (Giá sau ưu đãi) đã tính từ phần I
        # Nếu phần I chưa tính xong, mặc định lấy giá trị từ file hoặc 0
            gia_goi_y = st.session_state.get('nho_gia_chot', 0)

            # 2. Ô nhập Giá Chốt KH
            # CỰC KỲ QUAN TRỌNG: Thêm key động dựa trên giá trị gia_goi_y
            # Khi gia_goi_y thay đổi -> Key thay đổi -> Streamlit ép ô này nhận số mới
            gia_chot_kh = st.number_input(
                "17. Giá Chốt KH",
                value=gia_xe_moi,
                format="%d",
                step=1000000,
                key=f"input_chot_kh_{gia_xe_moi}" 
            )
            # 1. Lấy dữ liệu từ bộ nhớ chung (Shared từ Báo giá sang)

            val_vay_shared = st.session_state.get('so_tien_vay_shared', 0)
            val_dk_shared = st.session_state.get('chi_phi_dk_shared', 0)

            # --- MỤC: SỐ TIỀN VAY ---
            c_v1, c_v2 = st.columns([1.5, 2])
            with c_v1:
                st.write("")
                # TỰ ĐỘNG TÍCH CHỌN: Nếu số vay > 0 thì tự hiện dấu tích
                ck_vay_kh = st.checkbox("**Số tiền vay**", value=(val_vay_shared > 0), key=f"ck_vay_logic_{val_vay_shared}")
            with c_v2:
                val_vay_kh = st.number_input(
                    "Tiền vay KH", 
                    value=int(val_vay_shared), 
                    label_visibility="collapsed", 
                    disabled=not ck_vay_kh, 
                    format="%d", 
                    # KEY ĐỘNG {val_vay_shared}: Ép ô này phải hiện số mới từ báo giá
                    key=f"val_vay_logic_{val_vay_shared}" 
                )

            # --- MỤC: CHI PHÍ ĐĂNG KÝ ---
            c_dk1, c_dk2 = st.columns([1.5, 2])
            with c_dk1:
                st.write("")
                # TỰ ĐỘNG TÍCH CHỌN: Nếu có tiền đăng ký từ báo giá
                ck_dk = st.checkbox("**20. Chi phí đăng ký**", value=(val_dk_shared > 0), key="ck_dk_final")
            with c_dk2:
                val_dk = st.number_input(
                    "Tiền đăng ký", 
                    value=int(val_dk_shared), 
                    label_visibility="collapsed", 
                    disabled=not ck_dk, 
                    format="%d", 
                    key="val_dk_final" # Key cố định: "val_dk_final"
                )

            # --- LOGIC CỘNG DỒN VÀO BẢNG TỔNG ---
            if ck_vay_kh:
                tong_kh_giam_tru += val_vay_kh
                data_selected_cp.append(["18", "Số tiền vay ngân hàng", f"{val_vay_kh:,}", "Ngân hàng"])

            if ck_dk:
                tong_kh_cong_them += val_dk
                data_selected_cp.append(["20", "Chi phí đăng ký xe", f"{val_dk:,}", "Theo báo giá"])
            CPK_FILE = 'data_chi_phi_khac.csv'
            if os.path.exists(CPK_FILE):
                df_cpk = pd.read_csv(CPK_FILE)
                
                # XỬ LÝ TRIỆT ĐỂ: Xóa mọi khoảng trắng thừa trong tên cột
                df_cpk.columns = df_cpk.columns.str.strip()
                
                # Tên cột đích bạn muốn tìm
                col_t_cp = 'Nội dung'
                col_v_cp = 'Số tiền (VNĐ)' # Thêm dấu cách cho chuẩn hóa hoặc dùng .str.contains
                
                # Mẹo: Tìm cột có chứa chữ 'Số tiền' để tránh lỗi gõ thiếu dấu cách
                real_col_v = [c for c in df_cpk.columns if 'Số tiền' in c]
                real_col_t = [c for c in df_cpk.columns if 'Nội dung' in c]

                if real_col_t and real_col_v:
                    col_t_cp = real_col_t[0]
                    col_v_cp = real_col_v[0]
                    
                    for index, row in df_cpk.iterrows():
                        ten_cp = row[col_t_cp]
                        gia_cp = float(row[col_v_cp])
                        
                        c1, c2 = st.columns([1.5, 2])
                        with c1:
                            st.write("") 
                            is_on = st.checkbox(f"**{ten_cp}**", key=f"cpk_cb_{index}")
                        with c2:
                            val_cp = st.number_input(
                                f"Tiền {ten_cp}", value=int(gia_cp), key=f"cpk_val_{index}",
                                label_visibility="collapsed", disabled=not is_on, format="%d"
                            )
                        
                        if is_on:
                            # Phân loại trừ tiền (Vay, Cọc, Đối ứng)
                            if any(x in ten_cp.lower() for x in ["vay", "cọc", "đối ứng"]):
                                tong_kh_giam_tru += val_cp
                                data_selected_cp.append([str(index+18), ten_cp, f"-{val_cp:,}", ""])
                            else:
                                tong_kh_cong_them += val_cp
                                data_selected_cp.append([str(index+18), ten_cp, f"{val_cp:,}", ""])
                else:
                    st.warning(f"⚠️ Không tìm thấy cột 'Nội dung' hoặc 'Số tiền'. Hiện có: {list(df_cpk.columns)}")

            # 4. Mục Tiền Cọc cố định (Nhập tay bổ sung)
           
            c1, c2 = st.columns([1.5, 2])
            with c1:
                st.write("")
                ck_coc = st.checkbox("**21. Tiền khách đã Cọc**", value=False, key="chk_coc_manual")
            with c2:
                val_coc = st.number_input("Tiền cọc", value=10000000, label_visibility="collapsed", disabled=not ck_coc, format="%d")
            
            if ck_coc:
                tong_kh_giam_tru += val_coc
                data_selected_cp.append(["21", "Tiền khách đã Cọc", f"-{val_coc:,}", "Đã thu"])

    with col_kh_out:
        # 5. TÍNH TOÁN
        tong_kh_thanh_toan = (gia_chot_kh + tong_kh_cong_them) - tong_kh_giam_tru  

        st.markdown("#### 📋 CHI TIẾT THU TIỀN KHÁCH")
        
        rows_kh = [["17", "Giá Chốt KH", f"{gia_chot_kh:,}", ""]]
        rows_kh.extend(data_selected_cp) 
        rows_kh.append(["22", "**KH THANH TOÁN (CK)**", f"**{tong_kh_thanh_toan:,}**", "Chốt"])

        df_kh = pd.DataFrame(rows_kh, columns=["STT", "Nội dung", "Số tiền (VNĐ)", "Ghi chú"])
        st.table(df_kh)

        st.warning(f"### 💰 TỔNG THU KHÁCH: {tong_kh_thanh_toan:,} VNĐ")
   # --- PHẦN KẾT THÚC: LƯU DỮ LIỆU & CHUYỂN TRANG ---
    st.divider()
    col_btn1, col_btn2 = st.columns(2)

    # Nút 1: Xác nhận và nhảy sang trang Danh Sách
    # --- TẠI TRANG QUYẾT TOÁN ---
    if col_btn1.button("✅ XÁC NHẬN & XEM DANH SÁCH", use_container_width=True, type="primary"):
        try:
            import csv  
            
            # --- BƯỚC 0: LẤY DỮ LIỆU KHÁCH HÀNG ---
            # --- BƯỚC 0: TÍNH TOÁN LẠI BIẾN ---
            q = st.session_state.current_customer
            ten_kh = q.get('name') or q.get('Họ Tên') or "Khách ẩn danh"
            status_kh = q.get('status') or q.get('Trạng Thái') or "Cần chăm sóc"
            
            # Lấy các biến giá chốt và tổng thu
            v_gia_chot_kh = gia_chot_kh if 'gia_chot_kh' in locals() else 0
            v_tong_kh_dong = tong_kh_thanh_toan if 'tong_kh_thanh_toan' in locals() else 0
            
            # --- ĐOẠN QUAN TRỌNG NHẤT ĐỂ LẤY TIỀN ĐĂNG KÝ ---
            # Dùng đúng công thức tạo Key mà bạn đã viết ở phần giao diện
            key_check = f"ck_dk_logic_{val_dk_shared}"
            key_val = f"val_dk_logic_{val_dk_shared}"
            
            # Lấy giá trị trực tiếp từ bộ nhớ Session
            is_checked = st.session_state.get("ck_dk_final", False)
            so_tien_nhap = st.session_state.get("val_dk_final", 0)
            v_tien_dk_tu_o_nhap = st.session_state.get(key_val, 0)
            
            # Quyết định số tiền ghi vào file
            tien_dk_de_luu = v_tien_dk_tu_o_nhap if is_checked else 0

            # --- 1. CẬP NHẬT FILE TỔNG (DATA_FILE) ---
            if os.path.exists(DATA_FILE):
                df_all = pd.read_csv(DATA_FILE, encoding='utf-8-sig', on_bad_lines='skip')
                if ten_kh in df_all['Họ Tên'].values:
                    mask = df_all['Họ Tên'] == ten_kh
                    df_all.loc[mask, 'Trạng Thái'] = "Đã Quyết Toán"
                    df_all.loc[mask, 'Giá Sau Ưu Đãi'] = v_gia_chot_kh
                    df_all.loc[mask, 'Tổng Tiền'] = v_tong_kh_dong
                    df_all.loc[mask, 'Ngày QT'] = datetime.now().strftime("%d/%m/%Y")
                    df_all.to_csv(DATA_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)

            # --- 2. GHI VÀO FILE THEO DÕI (TRACKING_FILE) ---
            tracking_row = {
                "Khách Hàng": ten_kh, 
                "Loại Xe": f"{q.get('Xe') or q.get('car') or 'Xe'} {q.get('Bản') or q.get('ver') or ''}",
                "Ngày CỌC": datetime.now().strftime("%d/%m/%Y"),
                "Ngày XHĐ": "", "Ngày Giao Xe": "", 
                "Số Tiền HĐ": st.session_state.get('nho_gia_chot', 0),
                "Số Tiền Thực Thu": v_tong_kh_dong,
                "Số Tiền Chốt Khách": v_gia_chot_kh,
                "Trạng Thái Giao": "Chờ giao",
                "Ghi Chú": status_kh
            }
            
            if os.path.exists(TRACKING_FILE):
                df_track = pd.read_csv(TRACKING_FILE, encoding='utf-8-sig', on_bad_lines='skip')
                df_track = df_track[df_track['Khách Hàng'] != ten_kh] 
                df_track = pd.concat([df_track, pd.DataFrame([tracking_row])], ignore_index=True)
            else:
                df_track = pd.DataFrame([tracking_row])
            
            df_track.to_csv(TRACKING_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)

            # --- 3. GHI VÀO FILE LỢI NHUẬN (LN_FILE) ---
            ln_row = {
                "STT": 0, 
                "NGÀY XHĐ": datetime.now().strftime("%d/%m/%Y"),
                "Khách Hàng": ten_kh,
                "Giá Chốt": v_gia_chot_kh,
                "Tiền Đăng Ký": tien_dk_de_luu,  # <-- QUAN TRỌNG: Đảm bảo biến này bằng 16580000
                "Hoa Hồng Bank": 0, "Hoa Hồng": 0, "LỢI NHUẬN": 0,
                "Trạng Thái Giao": "Chờ giao"
            }

            if os.path.exists(LN_FILE):
                # Đọc file lợi nhuận lên để kiểm tra
                df_ln = pd.read_csv(LN_FILE, encoding='utf-8-sig', on_bad_lines='skip')
                # Xóa dòng cũ của khách này đi để ghi đè số tiền mới vào
                df_ln = df_ln[df_ln['Khách Hàng'] != ten_kh]
                df_ln = pd.concat([df_ln, pd.DataFrame([ln_row])], ignore_index=True)
                df_ln['STT'] = range(1, len(df_ln) + 1)
            else:
                df_ln = pd.DataFrame([ln_row])
                df_ln['STT'] = 1

            # Ghi đè lại file Lợi nhuận
            df_ln.to_csv(LN_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)

            st.success(f"🎉 Đã chốt hồ sơ {ten_kh}! (Tiền ĐK: {tien_dk_de_luu:,.0f} đ)")
            time.sleep(1)
            st.session_state.page = "Theo Dõi"
            st.rerun()

        except Exception as e:
            st.error(f"Lỗi lưu dữ liệu: {e}")
            
    
# --- 7. TRANG DANH SÁCH ---
elif st.session_state.page == "Danh Sách":
    st.subheader("📊 Quản lý Danh Sách Khách Hàng")
    
    if os.path.exists(DATA_FILE):
        try:
            # 1. Đọc dữ liệu từ file CSV
            df_list = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
            df_list.columns = [c.strip() for c in df_list.columns] # Xóa khoảng trắng thừa

            # --- BỘ LỌC TÊN THÔNG MINH (QUAN TRỌNG NHẤT) ---
            # Nếu file có 'Khách Hàng' mà không có 'Họ Tên', hãy tạo ra cột 'Họ Tên' để các hàm cũ không lỗi
            if 'Khách Hàng' in df_list.columns and 'Họ Tên' not in df_list.columns:
                df_list['Họ Tên'] = df_list['Khách Hàng']
            # Ngược lại, nếu có 'Họ Tên' mà thiếu 'Khách Hàng' (file cũ)
            elif 'Họ Tên' in df_list.columns and 'Khách Hàng' not in df_list.columns:
                df_list['Khách Hàng'] = df_list['Họ Tên']
            # -----------------------------------------------
            
            # --- PHẦN CHỌN KHÁCH HÀNG QUYẾT TOÁN ---
            st.markdown("### 📑 Chốt Quyết Toán")
            col_select, col_btn = st.columns([3, 1])
            
            # Bây giờ df_list chắc chắn đã có cột 'Họ Tên' nhờ bộ lọc trên
            list_names = df_list['Họ Tên'].tolist()
            selected_name = col_select.selectbox(
                "Chọn khách hàng:", 
                list_names, 
                index=None, 
                placeholder="Chọn tên khách để quyết toán..."
            )
          
            if col_btn.button("🚀 Sang Quyết Toán", use_container_width=True) and selected_name:
                row_kh = df_list[df_list['Họ Tên'] == selected_name].iloc[0]
                
                # Lấy giá trị an toàn bằng .get() để tránh lỗi văng app
                gia_xe_chuan = row_kh.get('Giá Sau Ưu Đãi', 0)
                phi_dk_da_luu = row_kh.get('Tiền Đăng Ký', 0)

                tien_vay_de_sang_qt = int(float(gia_xe_chuan) * 0.85) 

                st.session_state['so_tien_vay_shared'] = tien_vay_de_sang_qt
                st.session_state['chi_phi_dk_shared'] = int(phi_dk_da_luu)
                
                st.session_state['current_customer'] = row_kh.to_dict()
                st.session_state.page = "Quyết Toán"
                st.rerun()            
            st.divider()

            # --- PHẦN HIỂN THỊ BẢNG SỬA/XÓA ---
            st.markdown("### 📝 Chỉnh sửa danh sách")
            
            # Chỉ hiển thị các cột thực sự tồn tại để tránh lỗi cấu hình NumberColumn
            conf_cols = {}
            for c in ["Giá Sau Ưu Đãi", "Tiền Đăng Ký", "Tổng Tiền"]:
                if c in df_list.columns:
                    conf_cols[c] = st.column_config.NumberColumn(format="%,d")

            edited = st.data_editor(
                df_list, 
                num_rows="dynamic", 
                use_container_width=True, 
                hide_index=True,
                column_config=conf_cols
            )
            
            if st.button("💾 CẬP NHẬT THAY ĐỔI", use_container_width=True):
                edited.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                st.success("Đã cập nhật!"); st.rerun()

        except Exception as e:
            st.error(f"Lỗi hiển thị danh sách: {e}")
    else:
        st.info("Chưa có dữ liệu khách hàng.")
# --- PHẦN LƯU DỮ LIỆU THEO DÕI ---
elif st.session_state.page == "Theo Dõi":
    st.markdown("### 📋 QUẢN LÝ XE CHỜ GIAO & BÀN GIAO")
    
    # 1. KHAI BÁO FILE RIÊNG (Phải khớp với file bạn lưu ở trang Quyết toán)
    TRACKING_FILE = "data_theo_doi_xe.csv" 

    if os.path.exists(TRACKING_FILE):
    # 1. Sử dụng try-except để bắt lỗi và on_bad_lines để bỏ qua dòng hỏng
        try:
            df_follow = pd.read_csv(
                TRACKING_FILE, 
                encoding='utf-8-sig', 
                on_bad_lines='skip'  # <-- Thêm dòng này để bỏ qua các dòng "lệch cột"
            )
            
            # 2. Xử lý ngày tháng như cũ
            for col in ["Ngày CỌC", "Ngày XHĐ", "Ngày Giao Xe"]:
                if col in df_follow.columns:
                    df_follow[col] = pd.to_datetime(df_follow[col], errors='coerce', dayfirst=True)
                    
        except Exception as e:
            st.error(f"⚠️ Cấu trúc file dữ liệu bị lỗi: {e}")
        # Nếu lỗi quá nặng, cho phép người dùng biết để xử lý file thủ công
        # 2. THỐNG KÊ NHANH (Lấy từ file Theo Dõi)
        da_giao = len(df_follow[df_follow['Trạng Thái Giao'] == "Đã giao"])
        cho_giao = len(df_follow[df_follow['Trạng Thái Giao'] == "Chờ giao"])
        
        c1, c2, c3 = st.columns(3)
        c1.metric("🔵 TỔNG XE CHỐT", f"{len(df_follow)}")
        c2.info(f"🟢 ĐÃ GIAO: **{da_giao}**")
        c3.warning(f"🟡 CHỜ GIAO: **{cho_giao}**")

        st.divider()

        # 3. HIỂN THỊ BẢNG THEO DÕI (Dạng Editor để gõ được Ngày, Ghi chú)
        st.markdown("#### 📑 Chi tiết danh sách xe bàn giao")
        
        # Cấu hình các cột đặc biệt (Selectbox cho Trạng thái, Number cho tiền)
        edited_df = st.data_editor(
            df_follow,
            use_container_width=True,
            hide_index=False,
            column_config={
                # CẤU HÌNH CHỌN NGÀY BẰNG LỊCH
                "Ngày XHĐ": st.column_config.DateColumn(
                    "Ngày XHĐ", format="DD/MM/YYYY"
                ),
                "Ngày Giao Xe": st.column_config.DateColumn(
                    "Ngày Giao Xe", format="DD/MM/YYYY"
                ),
                "Ngày CỌC": st.column_config.DateColumn(
                    "Ngày CỌC", format="DD/MM/YYYY"
                ),
                # Các cấu hình cũ giữ nguyên
                "Trạng Thái Giao": st.column_config.SelectboxColumn(
                    "Trạng Thái Giao", options=["Chờ giao", "Đã giao"], required=True
                ),
                "Ghi Chú": st.column_config.SelectboxColumn(
                    "Ghi Chú", options=["Đã cọc", "Tiền mặt", "Cần chăm sóc", "Hủy cọc", "Chờ đăng ký"]
                ),
                "Số Tiền HĐ": st.column_config.NumberColumn(format="%,d"),
                "Số Tiền Thực Thu": st.column_config.NumberColumn(format="%,d"),
                "Số Tiền Chốt Khách": st.column_config.NumberColumn(format="%,d"),
            }
        )

        # 4. NÚT LƯU CẬP NHẬT (Lưu những gì bạn vừa sửa trong bảng)
        if st.button("💾 CẬP NHẬT THAY ĐỔI TRÊN BẢNG", type="primary", use_container_width=True):
            try:
                # Sao chép để không làm hỏng dữ liệu đang hiển thị
                df_save = edited_df.copy()

                # Định dạng lại ngày tháng thành chữ trước khi ghi vào CSV
                for col in ["Ngày CỌC", "Ngày XHĐ", "Ngày Giao Xe"]:
                    if col in df_save.columns:
                        # Chuyển về dạng ngày/tháng/năm
                        df_save[col] = pd.to_datetime(df_save[col]).dt.strftime('%d/%m/%Y')
                        # Xử lý các ô trống (NaT) thành chuỗi rỗng
                        df_save[col] = df_save[col].replace('NaT', '')

                df_save.to_csv(TRACKING_FILE, index=False, encoding='utf-8-sig')
                st.success("✅ Đã cập nhật ngày tháng và thông tin thành công!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi lưu cập nhật: {e}")
                
    else:
        # Đoạn này xử lý khi chưa có file (Thụt lề đúng 1 Tab so với 'if os.path.exists')
        st.info("Chưa có hồ sơ nào được chốt sang bảng Theo Dõi.")
        st.caption("Hãy hoàn tất bước 'Quyết Toán' cho khách hàng để đưa họ vào danh sách này.")
##lợi nhuận
elif st.session_state.page == "Lợi Nhuận":
        st.header("📊 QUẢN LÝ TÀI CHÍNH CHI TIẾT")
        
        thu_cols = ['Giá Vốn', 'Tiền Đăng Ký', 'Hoa Hồng Bank', 'Hoa Hồng HTX', 'Hoa Hồng', 'Thưởng Chỉ Tiêu']
        chi_cols = ['Ép Biển', 'Lệ Phí C.An', 'BHTNNS', 'BH VCX', 'Đăng Kiểm', 'HTX', 'Xe Thớt', 'Chi Giới Thiệu', 'Quà Tặng', 'HH-MG', 'Phí Hồ Sơ Bank', 'Phí Giao Xe']
        file_path = "danh_sach_khach_hang.csv" 

        if os.path.exists(file_path):
            df_full = pd.read_csv(file_path, encoding='utf-8-sig', on_bad_lines='skip')
            df_full.columns = [c.strip() for c in df_full.columns]
            
            # 1. Định nghĩa biến chung
            col_gia_chuan = 'Giá Sau Ưu Đãi' if 'Giá Sau Ưu Đãi' in df_full.columns else 'Giá Chốt'
            ten_cot_dk = 'Tiền đăng kí' if 'Tiền đăng kí' in df_full.columns else 'Tiền Đăng Ký'
            
            if 'Họ Tên' in df_full.columns:
                df_full = df_full.rename(columns={'Họ Tên': 'Khách Hàng'})

            # 2. Chuẩn hóa số liệu
            for c in thu_cols + chi_cols + [col_gia_chuan, 'Giá Vốn', ten_cot_dk]:
                if c in df_full.columns:
                    df_full[c] = pd.to_numeric(df_full[c], errors='coerce').fillna(0)
                else:
                    df_full[c] = 0

            df = df_full.copy()
            if 'Khách Hàng' in df.columns:
                df = df.drop_duplicates(subset=['Khách Hàng'], keep='last')

            # --- VẼ GIAO DIỆN ---
            tab_thu, tab_chi, tab_tong_ket = st.tabs(["🟢 TỔNG THU", "🔵 TỔNG CHI", "🟡 TỔNG KẾT"])
            
            with tab_thu:
                st.subheader("1. Các khoản thu thêm & Tiền đăng ký")
                uu_tien = ['Khách Hàng', ten_cot_dk]
                cac_cot_khac = [c for c in thu_cols if c in df.columns and c not in uu_tien and c not in ['Giá Vốn', 'Giá Sau Ưu Đãi', 'Giá Chốt']]
                cols_thu_show = uu_tien + cac_cot_khac
                
                edited_thu = st.data_editor(
                    df[cols_thu_show], 
                    key="editor_thu_v_final", 
                    hide_index=True, use_container_width=True,
                    column_config={c: st.column_config.NumberColumn(format="%,d") for c in cols_thu_show if c != 'Khách Hàng'}
                )

            with tab_chi:
                st.subheader("2. Các khoản chi phí nội bộ")
                cols_chi_show = ['Khách Hàng'] + [c for c in chi_cols if c in df.columns]
                edited_chi = st.data_editor(
                    df[cols_chi_show], 
                    key="editor_chi_v_final", 
                    hide_index=True, use_container_width=True,
                    column_config={c: st.column_config.NumberColumn(format="%,d") for c in cols_chi_show if c != 'Khách Hàng'}
                )
            
            with tab_tong_ket:
                st.subheader("3. Kết quả kinh doanh thực tế")
                t_gia_chot = df[col_gia_chuan].sum() 
                t_gia_von = df['Giá Vốn'].sum()
                t_thu_ngoai = edited_thu[[c for c in edited_thu.columns if c != 'Khách Hàng']].sum().sum()
                t_chi = edited_chi[[c for c in edited_chi.columns if c != 'Khách Hàng']].sum().sum()
                t_loi_nhuan = t_thu_ngoai - t_chi

                c1, c2, c3 = st.columns(3)
                c1.metric("Tổng Doanh Thu", f"{ t_thu_ngoai:,.0f} đ")
                c2.metric("Tổng Chi & Vốn", f"{t_chi :,.0f} đ")
                c3.metric("Lợi Nhuận Ròng", f"{t_loi_nhuan:,.0f} đ", delta=f"{t_loi_nhuan:,.0f} đ")

            # --- NÚT LƯU (Phải nằm trong IF os.path.exists) ---
            st.divider()
            if st.button("🚀 CẬP NHẬT & LƯU TẤT CẢ DỮ LIỆU", type="primary", use_container_width=True):
                try:
                    for index, row in edited_thu.iterrows():
                        ten_kh = row['Khách Hàng']
                        mask = df_full['Khách Hàng'] == ten_kh
                        # Cập nhật thu
                        for col in edited_thu.columns:
                            if col in df_full.columns: df_full.loc[mask, col] = row[col]
                        # Cập nhật chi
                        chi_rows = edited_chi[edited_chi['Khách Hàng'] == ten_kh]
                        if not chi_rows.empty:
                            chi_row = chi_rows.iloc[0]
                            for col in edited_chi.columns:
                                if col in df_full.columns: df_full.loc[mask, col] = chi_row[col]

                    df_full.to_csv(file_path, index=False, encoding='utf-8-sig')
                    st.success("✅ Đã cập nhật dữ liệu tài chính!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi khi lưu: {e}")

        else: # ELSE này thẳng hàng với IF os.path.exists
            st.error(f"❌ Không tìm thấy file: {file_path}")
