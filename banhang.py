import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time
import io
import csv
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
CS_FILE = 'data_chăm_soc.csv'
COLS_ORDER = [
    "Ngày", "Họ Tên", "SĐT", "CCCD","Email", "Địa chỉ", "Xe", "Bản", "Màu", "Chính Sách", "Quà Tặng",
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
c_nav1, c_nav2, c_nav3, c_nav4, c_nav5, c_nav6, c_nav7, c_nav8 = st.columns(8)

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
if c_nav8.button("📈 CHĂM SÓC", use_container_width=True): 
    st.session_state.page = "Chăm Sóc"; st.rerun()
st.divider()

# --- 3. TRANG TIẾP NHẬN ---

# Thêm quoting=csv.QUOTE_ALL vào lệnh lưu
#new_row_df.to_csv(DATA_FILE, mode='a', index=False, header=not os.path.exists(DATA_FILE), encoding='utf-8-sig', quoting=csv.QUOTE_ALL)
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
            # 1. Đọc file
            # Sửa dòng đọc file thành thế này:
            df_history = pd.read_csv(DATA_FILE, encoding='utf-8-sig', dtype={'SĐT': str, 'CCCD': str, 'Số điện thoại': str})
            df_history.columns = [c.strip() for c in df_history.columns] # Xóa khoảng trắng tiêu đề

            # --- BỘ LỌC TÊN THÔNG MINH (THÊM VÀO ĐÂY) ---
            # Nếu file chỉ có 'Khách Hàng', ta tạo thêm cột 'Họ Tên' để code bên dưới không lỗi
            if 'Khách Hàng' in df_history.columns and 'Họ Tên' not in df_history.columns:
                df_history['Họ Tên'] = df_history['Khách Hàng']
            # Ngược lại, nếu file có 'Họ Tên' mà thiếu 'Khách Hàng', ta tạo luôn cho đồng bộ
            if 'Họ Tên' in df_history.columns and 'Khách Hàng' not in df_history.columns:
                df_history['Khách Hàng'] = df_history['Họ Tên']
            
            # Đảm bảo cột SĐT luôn tồn tại để không lỗi split
            if 'SĐT' not in df_history.columns:
                df_history['SĐT'] = '0'
            # --------------------------------------------

            # Tạo danh sách Tên - SĐT (Lúc này chắc chắn đã có cột 'Họ Tên')
            list_khach = (df_history['Họ Tên'].astype(str) + " - " + df_history['SĐT'].astype(str)).unique().tolist()
            
            khach_chon = st.selectbox(
                "🔍 Tìm kiếm khách hàng cũ (Gõ tên hoặc SĐT):", 
                options=list_khach,
                index=None, 
                placeholder="Gõ để tìm nhanh khách cũ...",
                key=f"search_box_{k}"
            )
            
            if khach_chon:
                t_name = khach_chon.split(" - ")[0]
                t_phone = khach_chon.split(" - ")[1]
                match = df_history[(df_history['Họ Tên'].astype(str) == t_name) & (df_history['SĐT'].astype(str) == t_phone)]
                
                if not match.empty:
                    info_khach = match.iloc[-1].to_dict()
                    
                    # Điền dữ liệu vào form (Các key 'Họ Tên', 'SĐT'... giờ đã an toàn)
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
        # 1. Lấy dữ liệu từ túi nhớ ra, ép về kiểu chữ và bỏ dấu .0 nếu có
        sdt_tam = str(st.session_state.get(f"phone_{k}", "")).split('.')[0]

        # 2. CHỐT HẠ: Nếu thiếu số 0 thì bù vào ngay lập tức
        sdt_chuan = sdt_tam if sdt_tam.startswith('0') or not sdt_tam else "0" + sdt_tam

        # 3. Giữ nguyên code của đại ca, chỉ thêm tham số 'value'
        r_phone = c1.text_input(
            "Số điện thoại ", 
            value=sdt_chuan,      # Ép nó hiện số 0 ở đây
            key=f"phone_{k}", 
            max_chars=10          # Để 10 cho chuẩn SĐT Việt Nam
        )

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
            worksheet.write(row_idx+3, 0, 'Chi phí đăng ký (2)', label_fmt)
            worksheet.write(row_idx+3, 2, tong_chi_phi_dk, money_fmt)
            worksheet.write(row_idx+4, 1, 'Tổng số tiền trả trước (1) + (ĐK)', total_yellow)
            worksheet.write(row_idx+4, 2, tong_tra_truoc_nh_, total_yellow)

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
            
            # --- BƯỚC 1: LẤY DỮ LIỆU & CHUẨN HÓA SĐT NGAY LẬP TỨC ---
            q = st.session_state.current_customer
            ten_kh = str(q.get('Khách Hàng', q.get('Họ Tên', ''))).strip()
            # Hàm nội bộ để cứu SĐT (Trị lỗi E+08 và mất số 0)
            def fix_my_sdt(val):
                s = str(val).strip()

                # bỏ dấu phẩy + khoảng trắng
                s = s.replace(',', '').replace(' ', '')

                # bỏ .0
                if '.' in s:
                    s = s.split('.')[0]

                if not s or s.lower() == "nan":
                    return ""

                # xử lý dạng E+
                if "e+" in s.lower():
                    try:
                        s = str(int(float(s)))
                    except:
                        pass

                # thêm số 0 nếu thiếu
                if len(s) == 9 and s.isdigit():
                    s = "0" + s

                return s

            sdt_kh = fix_my_sdt(q.get('SĐT') or q.get('phone') or "")
            v_gia_chot_kh = gia_chot_kh if 'gia_chot_kh' in locals() else 0
            v_tong_kh_dong = tong_kh_thanh_toan if 'tong_kh_thanh_toan' in locals() else 0
            
            # Lấy tiền đăng ký từ session
            is_checked = st.session_state.get("ck_dk_final", False)
            v_tien_dk_tu_o_nhap = st.session_state.get(f"val_dk_logic_{val_dk_shared}", 0)
            tien_dk_de_luu = v_tien_dk_tu_o_nhap if is_checked else 0

            # --- BƯỚC 2: CẬP NHẬT FILE TỔNG (DATA_FILE) ---
            if os.path.exists(DATA_FILE):
                df_all = pd.read_csv(DATA_FILE, encoding='utf-8-sig', dtype=str).fillna("")
                # CỰC QUAN TRỌNG: dtype=str để không bị mất số 0 khi đọc
                df_all.columns = df_all.columns.str.strip()
                df_all['SĐT'] = df_all['SĐT'].apply(fix_my_sdt)
                # Đồng bộ tên cột khách hàng
                if 'Khách Hàng' not in df_all.columns and 'Họ Tên' in df_all.columns:
                    df_all['Khách Hàng'] = df_all['Họ Tên']
                elif 'Họ Tên' not in df_all.columns and 'Khách Hàng' in df_all.columns:
                    df_all['Họ Tên'] = df_all['Khách Hàng']
                if 'Khách Hàng' in df_all.columns and ten_kh in df_all['Khách Hàng'].values:
                    mask = df_all['SĐT'] == sdt_kh
                    df_all.loc[mask, 'Trạng Thái'] = "Đã Quyết Toán"
                    df_all.loc[mask, 'SĐT'] = sdt_kh # Ghi đè SĐT đã chuẩn hóa
                    df_all.loc[mask, 'Giá Sau Ưu Đãi'] = v_gia_chot_kh
                    df_all.loc[mask, 'Tổng Tiền'] = v_tong_kh_dong
                    df_all.loc[mask, 'Ngày QT'] = datetime.now().strftime("%d/%m/%Y")
                    df_all.to_csv(DATA_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)

            # --- BƯỚC 3: GHI FILE THEO DÕI (TRACKING_FILE) ---
            # --- 2. GHI VÀO FILE THEO DÕI (TRACKING_FILE) ---
            tracking_row = {
                "Khách Hàng": ten_kh, 
                "SĐT": sdt_kh,
                "Loại Xe": f"{q.get('Xe') or q.get('car') or 'Xe'} {q.get('Bản') or q.get('ver') or ''}",
                "Ngày CỌC": datetime.now().strftime("%d/%m/%Y"),
                "Số Tiền HĐ": st.session_state.get('nho_gia_chot', 0),
                "Số Tiền Thực Thu": v_tong_kh_dong,
                "Số Tiền Chốt Khách": v_gia_chot_kh,
                
                # --- CHỖ NÀY LÀ MẤU CHỐT: Lấy từ ô nhập liệu đại ca vừa gõ ---
                "Chương Trình": st.session_state.get('val_ctrinh', ""), 
                "Quà Tặng": st.session_state.get('val_quatang', ""),
                # -----------------------------------------------------------
                
                "Trạng Thái Giao": "Chờ giao",
                "Ghi Chú": ""
            }
            if os.path.exists(TRACKING_FILE):
                df_track = pd.read_csv(TRACKING_FILE, encoding='utf-8-sig', on_bad_lines='skip')
                if 'SĐT' in df_track.columns:
                    df_track['SĐT'] = df_track['SĐT'].apply(fix_my_sdt)
                df_track = df_track[df_track['SĐT'] != sdt_kh]
                df_track = pd.concat([df_track, pd.DataFrame([tracking_row])], ignore_index=True)
            else:
                df_track = pd.DataFrame([tracking_row])
            
            df_track.to_csv(TRACKING_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)

            # --- 3. GHI VÀO FILE LỢI NHUẬN (LN_FILE) ---
            trang_thai = tracking_row.get("Trạng Thái Giao", "Chờ giao")

# ===== DANH SÁCH LOẠI BỎ =====
            TRANG_THAI_LOAI = ["Cần chăm sóc", "Hủy cọc"]

            # ===== NẾU KHÔNG HỢP LỆ → KHÔNG VÀO LỢI NHUẬN =====
            if trang_thai in TRANG_THAI_LOAI:
                
                # --- GHI SANG FILE CHĂM SÓC ---
                cs_row = {
                    "Ngày": datetime.now().strftime("%d/%m/%Y"),
                    "Khách Hàng": ten_kh,
                    "SĐT": sdt_kh,
                    "Giá Chốt": v_gia_chot_kh,
                    "Trạng Thái": trang_thai,
                    "Ghi Chú": tracking_row.get("Ghi Chú", "")
                }

                CS_FILE = "cham_soc.csv"

                if os.path.exists(CS_FILE):
                    df_cs = pd.read_csv(CS_FILE, encoding='utf-8-sig')
                    df_cs = df_cs[df_cs['SĐT'] != sdt_kh]
                    df_cs = pd.concat([df_cs, pd.DataFrame([cs_row])], ignore_index=True)
                else:
                    df_cs = pd.DataFrame([cs_row])

                df_cs.to_csv(CS_FILE, index=False, encoding='utf-8-sig')

            else:
                # ===== CHỈ NHỮNG KHÁCH HỢP LỆ MỚI VÀO LỢI NHUẬN =====
                ln_row = {
                    "STT": 0, 
                    "NGÀY XHĐ": datetime.now().strftime("%d/%m/%Y"),
                    "Khách Hàng": ten_kh,
                    "SĐT": sdt_kh,
                    "Giá Chốt": v_gia_chot_kh,
                    "Tiền Đăng Ký": tien_dk_de_luu,
                    "Hoa Hồng Bank": 0,
                    "Hoa Hồng": 0,
                    "LỢI NHUẬN": 0,
                    "Trạng Thái Giao": trang_thai
                }

                if os.path.exists(LN_FILE):
                    df_ln = pd.read_csv(LN_FILE, encoding='utf-8-sig')
                    df_ln = df_ln[df_ln['SĐT'] != sdt_kh]
                    df_ln = pd.concat([df_ln, pd.DataFrame([ln_row])], ignore_index=True)
                    df_ln['STT'] = range(1, len(df_ln) + 1)
                else:
                    df_ln = pd.DataFrame([ln_row])
                    df_ln['STT'] = 1
                df_ln['SĐT'] = df_ln['SĐT'].apply(fix_my_sdt)
                df_ln.to_csv(LN_FILE, index=False, encoding='utf-8-sig')

            st.success(f"🎉 Chốt xong! SĐT: {sdt_kh}")
            time.sleep(1)
            st.session_state.page = "Theo Dõi"
            st.rerun()

        except Exception as e:
            st.error(f"Lỗi: {e}")
            
    

# --- 7. TRANG DANH SÁCH ---
elif st.session_state.page == "Danh Sách":
    st.subheader("📊 Quản lý Danh Sách Khách Hàng")
    
    if os.path.exists(DATA_FILE):
        try:
            # 1. Đọc dữ liệu từ file CSV
            df_list = pd.read_csv(DATA_FILE, encoding='utf-8-sig', dtype={'SĐT': str, 'CCCD': str, 'Số điện thoại': str})
            
            # Chuẩn hóa tên cột (tránh lỗi dấu cách)
            df_list.columns = df_list.columns.str.strip()

            # ===== 2. XỬ LÝ CỘT HỌ TÊN (TRỊ TẬN GỐC LỖI KHUYẾT TÊN) =====
            # Đảm bảo cột Họ Tên luôn tồn tại
            if 'Họ Tên' not in df_list.columns:
                df_list['Họ Tên'] = ""

            # Chuyển các giá trị rỗng/lỗi thành None để chuẩn bị "trám" dữ liệu
            df_list['Họ Tên'] = df_list['Họ Tên'].astype(str).str.strip().replace(['nan', 'None', ''], None)

            # Quét các cột tên dự phòng, hễ chỗ nào Họ Tên bị trống thì lấy cột khác đắp vào
            possible_name_cols = ['Khách Hàng', 'Ho Ten', 'Tên khách hàng', 'Tên Khách Hàng']
            for col in possible_name_cols:
                if col in df_list.columns:
                    temp_col = df_list[col].astype(str).str.strip().replace(['nan', 'None', ''], None)
                    df_list['Họ Tên'] = df_list['Họ Tên'].fillna(temp_col)

            # Đổi None về lại chuỗi rỗng
            df_list['Họ Tên'] = df_list['Họ Tên'].fillna("")

            # ===== 3. XỬ LÝ CỘT SĐT (Chỉ chạy 1 lần) =====
            def fix_sdt_vn(val):
                s = str(val).strip().replace(',', '').split('.')[0]
                if not s or s.lower() == "nan": return ""
                if "E+" in s.upper():
                    try: s = str(int(float(s)))
                    except ValueError: pass
                if len(s) == 9 and s.isdigit(): s = "0" + s
                return s

            if 'SĐT' in df_list.columns:
                df_list['SĐT'] = df_list['SĐT'].apply(fix_sdt_vn)
            elif 'Số điện thoại' in df_list.columns:
                # Nếu chỉ có 'Số điện thoại', đổi tên luôn thành 'SĐT' cho đồng nhất
                df_list['SĐT'] = df_list['Số điện thoại'].apply(fix_sdt_vn)
            else:
                df_list['SĐT'] = ""

            # --- BỘ LỌC BÙ TÊN NẾU TRỐNG (Chỉ chạy khi thật sự KHÔNG CÓ tên ở mọi cột) ---
            mask_empty_name = (df_list['Họ Tên'] == "") & (df_list['SĐT'] != "")
            df_list.loc[mask_empty_name, 'Họ Tên'] = "KH_" + df_list.loc[mask_empty_name, 'SĐT'].astype(str)
            
            # Đồng bộ ngược lại cột Khách Hàng để dữ liệu các tab khác không bị mâu thuẫn
            if 'Khách Hàng' in df_list.columns:
                df_list['Khách Hàng'] = df_list['Họ Tên']

            # --- 4. CHỌN KHÁCH HÀNG ĐỂ QUYẾT TOÁN ---
            st.markdown("### 📑 Chốt Quyết Toán")
            col_select, col_btn = st.columns([3, 1])
            
            # Tạo danh sách hiển thị
            list_names = (df_list['Họ Tên'] + " - " + df_list['SĐT']).tolist()
            
            selected_name = col_select.selectbox(
                "Chọn khách hàng:", 
                list_names, 
                index=None, 
                placeholder="Chọn tên khách để quyết toán..."
            )

            if col_btn.button("🚀 Sang Quyết Toán", use_container_width=True, key="btn_sang_qt") and selected_name:
                
                # Cắt lấy SĐT để đối chiếu
                sdt_selected = selected_name.split(" - ")[-1]
                row_kh = df_list[df_list['SĐT'] == sdt_selected].iloc[0]
                
                # Lấy giá trị an toàn, fallback về 0 nếu dữ liệu rỗng (tránh crash)
                try:
                    gia_xe_chuan = float(row_kh.get('Giá Sau Ưu Đãi', 0) or 0)
                    phi_dk_da_luu = float(row_kh.get('Tiền Đăng Ký', 0) or 0)
                except ValueError:
                    gia_xe_chuan = 0
                    phi_dk_da_luu = 0

                tien_vay_de_sang_qt = int(gia_xe_chuan * 0.85) 

                # Lưu vào session_state
                st.session_state['so_tien_vay_shared'] = tien_vay_de_sang_qt
                st.session_state['chi_phi_dk_shared'] = int(phi_dk_da_luu)
                st.session_state['current_customer'] = row_kh.to_dict()
                
                st.session_state.page = "Quyết Toán"
                st.rerun()            
                
            st.divider()

            # --- 5. PHẦN HIỂN THỊ BẢNG SỬA/XÓA ---
            st.markdown("### 📝 Chỉnh sửa danh sách")
            
            # Chỉ hiển thị các cột thực sự tồn tại để tránh lỗi cấu hình NumberColumn
            conf_cols = {}
            for c in ["Giá Sau Ưu Đãi", "Tiền Đăng Ký", "Tổng Tiền"]:
                if c in df_list.columns:
                    conf_cols[c] = st.column_config.NumberColumn(format="%,d")

            edited = st.data_editor(
                df_list, 
                column_order=COLS_ORDER, 
                num_rows="dynamic", 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    **conf_cols,
                    "SĐT": st.column_config.TextColumn()
                }
            )
            
            if st.button("💾 CẬP NHẬT THAY ĐỔI", use_container_width=True):
                # Chuẩn hóa lại SĐT đề phòng người dùng nhập sai định dạng khi sửa trực tiếp
                if 'SĐT' in edited.columns:
                    edited['SĐT'] = edited['SĐT'].apply(fix_sdt_vn)

                edited.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                st.success("Đã cập nhật thay đổi thành công!")
                st.rerun()

        except Exception as e:
            st.error(f"Đã xảy ra lỗi khi tải hoặc hiển thị dữ liệu: {e}")
            
    else:
        st.info("Chưa có dữ liệu khách hàng. Vui lòng thêm khách hàng mới.")
elif st.session_state.page == "Theo Dõi":
    st.markdown("### 📋 QUẢN LÝ XE CHỜ GIAO & BÀN GIAO")
    
    TRACKING_FILE = "data_theo_doi_xe.csv" 

    if os.path.exists(TRACKING_FILE):
        try:
            # 1. Đọc file với dtype=str để không mất số 0 điện thoại
            df_follow = pd.read_csv(TRACKING_FILE, encoding='utf-8-sig', dtype=str).fillna("")
            
            # --- BƯỚC QUAN TRỌNG: TỰ ĐỘNG BÙ CỘT THIẾU ---
            # Danh sách tất cả các trường đại ca cần (để không bị mất trường)
            all_cols = [
                "Khách Hàng", "SĐT", "Loại Xe", # Đưa lên đầu cho dễ nhìn
                "Ngày CỌC", "Ngày XHĐ", "Ngày Giao Xe", 
                "Số Tiền HĐ", "Số Tiền Thực Thu", "Số Tiền Chốt Khách" 
                 ,"Trạng Thái Giao", "Ghi Chú"
            ]
            for c in all_cols:
                if c not in df_follow.columns:
                    df_follow[c] = "" # Nếu thiếu cột nào thì tự tạo cột trống đó
            # --- MỤC TÌM KIẾM MỚI ---
            st.markdown("#### 🔍 Tìm kiếm nhanh")
            search_col1, search_col2 = st.columns([2, 1])
            with search_col1:
                search_term = st.text_input(
                    "Nhập tên khách hàng hoặc số điện thoại...", 
                    placeholder="Tìm kiếm",
                    label_visibility="collapsed"
                )
            
            # Thực hiện lọc dữ liệu nếu có nhập từ khóa
            if search_term:
                df_follow = df_follow[
                    df_follow['Khách Hàng'].astype(str).str.contains(search_term, case=False, na=False) |
                    df_follow['SĐT'].astype(str).str.contains(search_term, case=False, na=False)
                ]
            # 2. Xử lý ngày tháng để hiện lịch chọn
            for col in ["Ngày CỌC", "Ngày XHĐ", "Ngày Giao Xe"]:
                df_follow[col] = pd.to_datetime(df_follow[col], errors='coerce', dayfirst=True)
                    
        except Exception as e:
            st.error(f"⚠️ Lỗi cấu hình file: {e}")
            df_follow = pd.DataFrame()

        # 2. THỐNG KÊ
        if not df_follow.empty:
            da_giao = len(df_follow[df_follow['Trạng Thái Giao'] == "Đã giao"])
            cho_giao = len(df_follow[df_follow['Trạng Thái Giao'] == "Chờ giao"])
            
            c1, c2, c3 = st.columns(3)
            c1.metric("🔵 TỔNG XE", f"{len(df_follow)}")
            c2.info(f"🟢 ĐÃ GIAO: **{da_giao}**")
            c3.warning(f"🟡 CHỜ GIAO: **{cho_giao}**")

            st.divider()

            # 3. HIỂN THỊ BẢNG
            st.markdown("#### 📑 Chi tiết danh sách xe bàn giao")
            
            # Cấu hình hiển thị cột
            conf_follow = {
                "Khách Hàng": st.column_config.TextColumn("Khách Hàng", pinned=True, width="medium"),
                "SĐT": st.column_config.TextColumn("Số Điện Thoại"),
                "Ngày XHĐ": st.column_config.DateColumn("Ngày XHĐ", format="DD/MM/YYYY"),
                "Ngày Giao Xe": st.column_config.DateColumn("Ngày Giao Xe", format="DD/MM/YYYY"),
                "Ngày CỌC": st.column_config.DateColumn("Ngày CỌC", format="DD/MM/YYYY"),
                "Trạng Thái Giao": st.column_config.SelectboxColumn(
                    "Trạng Thái", options=["Chờ giao", "Đã giao"], required=True
                ),
                "Ghi Chú": st.column_config.SelectboxColumn(
                    "Ghi Chú", options=["Đã cọc", "Tiền mặt", "Cần chăm sóc", "Hủy cọc", "Chờ đăng ký"]
                ),
            }
            # Định dạng các cột tiền
            for c in ["Số Tiền HĐ", "Số Tiền Thực Thu", "Số Tiền Chốt Khách"]:
                conf_follow[c] = st.column_config.NumberColumn(format="%,d")

            edited_df = st.data_editor(
                df_follow,
                column_order=all_cols, # Ép hiện đúng thứ tự các cột
                use_container_width=True,
                num_rows="dynamic",
                hide_index=True,
                column_config=conf_follow,
                key="editor_theo_doi_final"
            )

            # 4. NÚT LƯU
            if st.button("💾 CẬP NHẬT THAY ĐỔI", type="primary", use_container_width=True):
                try:
                    import csv
                    # 1. Tạo bản sao dữ liệu từ bảng Editor
                    df_temp = edited_df.copy()

                    # 2. Xử lý định dạng ngày tháng chuẩn để lưu file
                    for col in ["Ngày CỌC", "Ngày XHĐ", "Ngày Giao Xe"]:
                        if col in df_temp.columns:
                            df_temp[col] = pd.to_datetime(df_temp[col]).dt.strftime('%d/%m/%Y')
                            df_temp[col] = df_temp[col].replace('NaT', '')

                    # --- BƯỚC PHÂN LUỒNG QUAN TRỌNG ---
                    # Danh sách trạng thái bị "đuổi" khỏi bảng chính
                    danh_sach_loai = ["Cần chăm sóc", "Hủy cọc"]

                    # Lọc ra những khách thuộc diện bị loại (để đưa sang CS_FILE)
                    df_move_to_care = df_temp[df_temp['Ghi Chú'].isin(danh_sach_loai)]

                    # Lọc ra những khách ở lại bảng chính (Đã cọc, Tiền mặt, Đã giao...)
                    df_stay_here = df_temp[~df_temp['Ghi Chú'].isin(danh_sach_loai)]

                    # 3. Ghi lại file Theo Dõi (Chỉ còn những người ở lại)
                    df_stay_here.to_csv(TRACKING_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)

                    # 4. Nếu có khách bị loại -> Ghi nối đuôi vào file Chăm Sóc
                    if not df_move_to_care.empty:
                        # Ghi thêm SĐT cho chắc chắn để không mất số 0
                        if os.path.exists(CS_FILE):
                            df_old_care = pd.read_csv(CS_FILE, dtype=str).fillna("")
                            df_final_care = pd.concat([df_old_care, df_move_to_care], ignore_index=True)
                            # Xóa trùng SĐT (nếu lỡ bấm lưu 2 lần)
                            df_final_care = df_final_care.drop_duplicates(subset=['SĐT'], keep='last')
                        else:
                            df_final_care = df_move_to_care
                        
                        # Lưu file Chăm Sóc
                        df_final_care.to_csv(CS_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)
                        st.toast(f"🚚 Đã chuyển {len(df_move_to_care)} khách sang kho Chăm Sóc!")

                    st.success("✅ Đã cập nhật và đồng bộ danh sách thành công!")
                    time.sleep(1)
                    st.rerun()

                except Exception as e:
                    st.error(f"Lỗi khi lưu và phân loại: {e}")
    else:
        st.info("Chưa có hồ sơ nào trong danh sách Theo Dõi.")
elif st.session_state.page == "Lợi Nhuận":
    st.header("📊 QUẢN LÝ TÀI CHÍNH CHI TIẾT")
    
    # 1. CẤU HÌNH CỘT
    thu_cols = ['Giá Vốn', 'Tiền Đăng Ký', 'Hoa Hồng Bank', 'Hoa Hồng HTX', 'Hoa Hồng', 'Thưởng Chỉ Tiêu']
    chi_cols = ['Ép Biển', 'Lệ Phí C.An', 'BHTNNS', 'BH VCX', 'Đăng Kiểm', 'HTX', 'Xe Thớt', 'Chi Giới Thiệu', 'HH-MG', 'Phí Hồ Sơ Bank', 'Phí Giao Xe']
    file_path = DATA_FILE 

    if os.path.exists(file_path):
        # --- BƯỚC 1: ĐỌC VÀ CHUẨN HÓA GỐC ---
        df_full = pd.read_csv(file_path, encoding='utf-8-sig', dtype=str).fillna("")
        df_full.columns = [c.strip() for c in df_full.columns]
        df_full = df_full.loc[:, ~df_full.columns.duplicated()] # Xóa cột trùng tên gây lỗi Index

        if 'Họ Tên' in df_full.columns and 'Khách Hàng' not in df_full.columns:
            df_full = df_full.rename(columns={'Họ Tên': 'Khách Hàng'})

        # Làm sạch dữ liệu rác
        df_full['Khách Hàng'] = df_full['Khách Hàng'].astype(str).str.strip()
        df_full = df_full[~df_full['Khách Hàng'].str.lower().isin(['', 'nan', 'none', '0', 'null'])]

        # --- BƯỚC 2: LOẠI TRỪ KHÁCH TRONG KHO CHĂM SÓC ---
        list_sdt_cham_soc = []
        if os.path.exists(CS_FILE):
            df_cs_check = pd.read_csv(CS_FILE, dtype=str).fillna("")
            if 'SĐT' in df_cs_check.columns:
                list_sdt_cham_soc = df_cs_check['SĐT'].tolist()

        # --- BƯỚC 3: LOGIC LỌC TÀI CHÍNH ---
        df_full['Trạng Thái'] = df_full['Trạng Thái'].astype(str).str.lower().str.strip()
        df_full['Ghi Chú'] = df_full['Ghi Chú'].astype(str).str.lower().str.strip()
        
        mask_quyet_toan = df_full['Trạng Thái'].isin(['đã quyết toán', 'da quyet toan'])
        dk_hop_le = ["tiền mặt", "đã cọc", "ck", "chuyển khoản", "cọc"]
        mask_ghi_chu = df_full['Ghi Chú'].apply(lambda x: any(k in str(x) for k in dk_hop_le))
        
        mask_loai_bo = False
        if 'Trạng Thái Giao' in df_full.columns:
            mask_loai_bo = df_full['Trạng Thái Giao'].astype(str).str.lower().isin(["cần chăm sóc", "hủy cọc"])

        # Tạo bảng tài chính (Loại trừ người trong list_sdt_cham_soc)
        df_tai_chinh = df_full[
            (mask_quyet_toan | mask_ghi_chu) & 
            ~mask_loai_bo & 
            ~df_full['SĐT'].isin(list_sdt_cham_soc)
        ].copy()

        # Ép kiểu số để hiển thị và tính toán
        ten_cot_dk = 'Tiền đăng kí' if 'Tiền đăng kí' in df_full.columns else 'Tiền Đăng Ký'
        for c in thu_cols + chi_cols + [ten_cot_dk]:
            if c in df_tai_chinh.columns:
                df_tai_chinh[c] = pd.to_numeric(df_tai_chinh[c].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

        # --- BƯỚC 4: MỤC TÌM KIẾM (HIỆN LIỀN) ---
        search_prof = st.text_input("🔍 Tìm kiếm trong tài chính", placeholder="Nhập tên khách hoặc SĐT...")
        df_display = df_tai_chinh.copy()
        if search_prof:
            df_display = df_display[
                (df_display['Khách Hàng'].str.contains(search_prof, case=False, na=False)) |
                (df_display['SĐT'].str.contains(search_prof, case=False, na=False))
            ]

        # --- BƯỚC 5: GIAO DIỆN TABS ---
        tab_thu, tab_chi, tab_tong_ket = st.tabs(["🟢 TỔNG THU", "🔵 TỔNG CHI", "🟡 TỔNG KẾT"])

        with tab_thu:
            st.subheader("1. Các khoản thu thêm & Tiền đăng ký")
            cols_thu_show = ['Khách Hàng', 'SĐT', ten_cot_dk] + [c for c in thu_cols if c in df_display.columns and c != 'Giá Vốn' and c != ten_cot_dk]
            edited_thu = st.data_editor(df_display[cols_thu_show], key="ed_thu_final_v2", hide_index=True, use_container_width=True,
                                        column_config={c: st.column_config.NumberColumn(format="%,d") for c in cols_thu_show if c not in ['Khách Hàng', 'SĐT']})

        with tab_chi:
            st.subheader("2. Các khoản chi phí nội bộ")
            cols_chi_show = ['Khách Hàng', 'SĐT'] + [c for c in chi_cols if c in df_display.columns]
            edited_chi = st.data_editor(df_display[cols_chi_show], key="ed_chi_final_v2", hide_index=True, use_container_width=True,
                                        column_config={c: st.column_config.NumberColumn(format="%,d") for c in cols_chi_show if c not in ['Khách Hàng', 'SĐT']})
        
        with tab_tong_ket:
            st.subheader("3. Kết quả kinh doanh thực tế")
            t_thu = edited_thu.select_dtypes(include=['number']).sum().sum()
            t_chi = edited_chi.select_dtypes(include=['number']).sum().sum()
            c1, c2, c3 = st.columns(3)
            c1.metric("Tổng Thu Thêm", f"{t_thu:,.0f} đ")
            c2.metric("Tổng Chi Phí", f"{t_chi:,.0f} đ")
            c3.metric("Lợi Nhuận Ròng", f"{(t_thu - t_chi):,.0f} đ")

        st.divider()
        # --- BƯỚC 6: NÚT LƯU CỰC KỲ AN TOÀN ---
        if st.button("🚀 CẬP NHẬT & LƯU DỮ LIỆU TÀI CHÍNH", type="primary", use_container_width=True):
            try:
                # Đọc lại file gốc để tránh ghi đè thiếu người
                df_root = pd.read_csv(file_path, encoding='utf-8-sig', dtype=str).fillna("")
                df_root.columns = [c.strip() for c in df_root.columns]
                df_root = df_root.loc[:, ~df_root.columns.duplicated()]

                # Cập nhật dựa trên SĐT (SĐT là duy nhất, Khách Hàng có thể trùng)
                for _, row in edited_thu.iterrows():
                    mask = (df_root['SĐT'] == str(row['SĐT']))
                    for col in edited_thu.columns:
                        if col in df_root.columns and col not in ['Khách Hàng', 'SĐT']:
                            df_root.loc[mask, col] = str(row[col])
                
                for _, row in edited_chi.iterrows():
                    mask = (df_root['SĐT'] == str(row['SĐT']))
                    for col in edited_chi.columns:
                        if col in df_root.columns and col not in ['Khách Hàng', 'SĐT']:
                            df_root.loc[mask, col] = str(row[col])

                df_root.to_csv(file_path, index=False, encoding='utf-8-sig')
                st.success("✅ Đã cập nhật lợi nhuận thành công!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi lưu: {e}")

    # --- PHẦN 2: BẢNG RIÊNG BIỆT 28 CỘT (Dựa trên detailed_contracts.csv) ---
    # --- PHẦN 2: BẢNG RIÊNG BIỆT 28 CỘT (Dựa trên detailed_contracts.csv) ---
    st.divider()
    st.subheader("📋 QUẢN LÝ HỢP ĐỒNG CHI TIẾT")
    
    COLS_28 = [
        "ID", "Khách Hàng", "SĐT", "Loại Xe", "Số Khung", "Số Máy", 
        "Ngày Cọc", "Ngày Xuất HĐ", "Ngày Giao Xe", "Tiền Cọc", 
        "Giá Trị HĐ", "Trạng Thái Giao",   # ✅ THÊM DÒNG NÀY
        "Ghi Chú", 
        "Thu_Đăng Ký", "Thu_Hoa Hồng Bank", "Thu_Hoa Hồng HTX", "Thu_Hoa Hồng", 
        "Chi_Ép Biển", "Chi_Lệ Phí CA", "Chi_BHTNNS", "Chi_BH VCX", 
        "Chi_Đăng Kiểm", "Chi_HTX", "Chi_Xe Thớt", "Chi_Giới Thiệu", 
        "Chi_Quà Tặng", "Lợi Nhuận"
    ]
    
    MASTER_FILE = "detailed_contracts.csv"
    SOURCE_FILE = "danh_sach_khach_hang.csv"
    TRACKING_FILE = "data_theo_doi_xe.csv"
    # 1. Tự động nạp dữ liệu cũ (nếu có)

    if 'df_master_28' not in st.session_state:
        if os.path.exists(MASTER_FILE):
            df_init = pd.read_csv(MASTER_FILE, encoding='utf-8-sig', dtype=str).fillna(0)
            st.session_state['df_master_28'] = df_init
        else:
            st.session_state['df_master_28'] = pd.DataFrame(columns=COLS_28)

    # 2. NÚT ĐỒNG BỘ: Bốc dữ liệu từ file 34 cột sang 28 cột
    if st.button("🔗 ĐỒNG BỘ DỮ LIỆU", use_container_width=True):
        if os.path.exists(SOURCE_FILE) and os.path.exists(TRACKING_FILE):
            try:
                # 1. Đọc dữ liệu ép kiểu Chữ (String) để không mất số 0
                df_source = pd.read_csv(SOURCE_FILE, encoding='utf-8-sig', dtype=str).fillna("")
                df_track = pd.read_csv(TRACKING_FILE, encoding='utf-8-sig', dtype=str).fillna("")
                if 'SĐT' in df_source.columns:
                    df_source['SĐT'] = df_source['SĐT'].astype(str).str.replace(',', '')

                if 'SĐT' in df_track.columns:
                    df_track['SĐT'] = df_track['SĐT'].astype(str).str.replace(',', '')
                # 2. Làm sạch tên cột
                df_source.columns = df_source.columns.str.strip()
                df_track.columns = df_track.columns.str.strip()

                # 3. Đồng bộ cột Khách Hàng để khớp dữ liệu
                if 'Họ Tên' in df_source.columns:
                    df_source['Khách Hàng'] = df_source['Họ Tên']
                
                # Merge 2 bảng lại làm 1
                df_src = pd.merge(df_source, df_track, on='Khách Hàng', how='outer', suffixes=('_src', '_trk'))
                
                new_data = []
    
                # 1. Hàm vá SĐT cực mạnh (Trị mọi loại E+08, mất số 0)
                def clean_sdt_final(val):
                    s = str(val).strip().replace(',', '').split('.')[0]
                    if not s or s.lower() == "nan": return ""
                    if "E+" in s.upper():
                        try: s = str(int(float(s)))
                        except: pass
                    if len(s) == 9 and s.isdigit():
                        s = "0" + s
                    return s

                for _, row in df_src.iterrows():
                    ten_chuan = str(row.get('Khách Hàng', '')).strip()
                    if not ten_chuan: ten_chuan = str(row.get('Họ Tên', '')).strip()
                    if not ten_chuan: continue # Bỏ qua dòng trống
                    # ===== LẤY TRẠNG THÁI =====
                    trang_thai = str(row.get('Trạng Thái Giao', '')).strip()
                    if trang_thai.lower() == "nan":
                        trang_thai = ""
                    ghi_chu = str(row.get('Ghi Chú', '')).strip()

                    # ===== 1. CHĂM SÓC / HỦY CỌC =====
                    if trang_thai in ["Cần chăm sóc", "Hủy cọc"]:

                        sdt_cs = clean_sdt_final(row.get('SĐT_src', row.get('SĐT_trk', row.get('SĐT', ''))))
                        
                        # --- FIX: BỐC QUÀ TẶNG & CHÍNH SÁCH TỪ BẢNG GỐC SANG ---
                        def safe_get(row, *cols):
                            for c in cols:
                                if c in row and str(row[c]).strip() not in ["", "nan", "None"]:
                                    return str(row[c]).strip()
                            return ""

                        chinh_sach = safe_get(row, 'Chính Sách', 'Chương Trình', 'Chương Trình_src', 'Chương Trình_trk')
                        qua_tang   = safe_get(row, 'Quà Tặng', 'Quà Tặng_src', 'Quà Tặng_trk', 'val_quatang')

                        if not chinh_sach:
                            chinh_sach = "Không áp dụng"
                        if not qua_tang:
                            qua_tang = "Không có"
                        if chinh_sach.lower() == 'nan' or not chinh_sach: chinh_sach = "Không áp dụng"
                        if qua_tang.lower() == 'nan' or not qua_tang: qua_tang = "Không có"
                        cs_row = {
                            "Ngày": datetime.now().strftime("%d/%m/%Y"),
                            "Khách Hàng": ten_chuan, 
                            "SĐT": sdt_cs,
                            "Loại Xe": row.get('Xe', row.get('Loại Xe', '')),
                            "Số Tiền HĐ": row.get('Giá Sau Ưu Đãi', row.get('Giá Trị HĐ', 0)),
                            "Số Tiền Thực Thu": row.get('Tổng Tiền', 0),
                            "Số Tiền Chốt Khách": row.get('Tổng Tiền', 0),
                            "Chương Trình": None,  # <-- Đã được bơm dữ liệu
                            "Quà Tặng": None,        # <-- Đã được bơm dữ liệu
                            "Trạng Thái Giao": "Chờ giao",
                            "Trạng Thái": trang_thai, 
                            "Ghi Chú": ghi_chu
                        }

                        CS_FILE = "cham_soc.csv"

                        if os.path.exists(CS_FILE):
                            df_cs = pd.read_csv(CS_FILE, encoding='utf-8-sig')
                            df_cs = df_cs[df_cs['SĐT'] != sdt_cs]
                            df_cs = pd.concat([df_cs, pd.DataFrame([cs_row])], ignore_index=True)
                        else:
                            df_cs = pd.DataFrame([cs_row])

                        df_cs.to_csv(CS_FILE, index=False, encoding='utf-8-sig')

                        continue  # ❗ rất quan trọng

                    # ===== 2. CHỈ NHẬN CHỜ GIAO / ĐÃ GIAO =====
                    if trang_thai not in ["Chờ giao", "Đã giao"]:
                        continue

                    # ===== 3. ĐIỀU KIỆN GHI CHÚ =====
                    DIEU_KIEN_OK = ["tiền mặt", "đã cọc", "chờ đăng ký"]

                    ghi_chu_lower = ghi_chu.lower()

                    DIEU_KIEN_OK = ["tiền mặt", "đã cọc", "chờ đăng ký", "ck", "chuyển khoản"]

                    # ✔️ cho phép ghi chú rỗng vẫn chạy
                    hop_le_ghi_chu = (
                        ghi_chu_lower == "" or
                        any(x in ghi_chu_lower for x in DIEU_KIEN_OK)
                    )

                    if not hop_le_ghi_chu:
                        print("❌ BỎ:", ten_chuan, "| ghi chú:", ghi_chu)
                        continue
                    sdt_final = clean_sdt_final(row.get('SĐT_src', row.get('SĐT_trk', row.get('SĐT', ''))))
                                # TẠO DÒNG 28 CỘT (Chỉ chứa dữ liệu chữ/số)
                    item = {
                        "ID": f"VF-{datetime.now().strftime('%d%m%H%M')}",
                        "Khách Hàng": ten_chuan,
                        "SĐT": str(sdt_final), # <--- Giờ nó là Chữ chuẩn rồi
                        "Loại Xe": row.get('Xe', row.get('Loại Xe', '')),
                        "Số Khung": row.get('Số Khung', ''),
                        "Số Máy": row.get('Số Máy', ''),
                        "Ngày Cọc": row.get('Ngày', row.get('Ngày CỌC', '')),
                        "Ngày Xuất HĐ": row.get('Ngày XHĐ', ''),
                        "Ngày Giao Xe": row.get('Ngày Giao Xe', ''),
                        "Giá Trị HĐ": row.get('Giá Sau Ưu Đãi', row.get('Số Tiền Chốt Khách', 0)),
                        "Trạng Thái Giao": trang_thai,
                        "Thu_Đăng Ký": row.get('Tiền Đăng Ký', 0),
                        "Thu_Hoa Hồng Bank": row.get('Hoa Hồng Bank', 0),
                        "Thu_Hoa Hồng HTX": row.get('Hoa Hồng HTX', 0),
                        "Thu_Hoa Hồng": row.get('Hoa Hồng', 0),
                        "Chi_Ép Biển": row.get('Ép Biển', 0),
                        "Chi_Lệ Phí CA": row.get('Lệ Phí C.An', 0),
                        "Chi_BHTNNS": row.get('BHTNNS', 0),
                        "Chi_BH VCX": row.get('BH VCX', 0),
                        "Chi_Đăng Kiểm": row.get('Đăng Kiểm', 0),
                        "Chi_HTX": row.get('HTX', 0),
                        "Chi_Xe Thớt": row.get('Xe Thớt', 0),
                        "Chi_Giới Thiệu": row.get('Chi Giới Thiệu', 0),
                        "Chi_Quà Tặng": row.get('val_quatang', 0),
                    }
                    
                    # Điền nốt các cột còn lại trong COLS_28 nếu còn thiếu
                    for c in COLS_28:
                        if c not in item:
                            val = row.get(c, 0)
                            # Nếu là cột tiền thì ép về số nguyên
                            if any(k in c for k in ["Thu_", "Chi_", "Giá", "Tiền", "Lợi Nhuận"]):
                                try: item[c] = int(float(str(val).replace(',', '')))
                                except: item[c] = 0
                            else:
                                item[c] = val

                    new_data.append(item)
                    if len(new_data) == 0:
                        st.error("❌ Không có dữ liệu hợp lệ → check lại:")
                        st.write(df_src[['Khách Hàng','Trạng Thái Giao','Ghi Chú']].head(10))
                        st.stop()
                    # Xuất kết quả
                df_final = pd.DataFrame(new_data)

                # đảm bảo đủ cột
                for col in COLS_28:
                    if col not in df_final.columns:
                        df_final[col] = ""

                df_final = df_final[COLS_28]

                st.session_state['df_master_28'] = df_final

                # ✅ sửa ở đây
                df_final.to_csv(MASTER_FILE, index=False, encoding='utf-8-sig')
                st.success("✅ Đã đồng bộ sạch sẽ! Nhớ bấm LƯU ở dưới nhé."); st.rerun()
                
            except Exception as e:
                st.error(f"Lỗi đồng bộ: {e}")

    # 3. Hiển thị bảng và tính Lợi Nhuận
    if 'df_master_28' in st.session_state:
        df_edit = st.session_state['df_master_28'].copy()
        df_edit['SĐT'] = df_edit['SĐT'].astype(str)
        # Ép kiểu số để tính Lợi Nhuận
        for c in COLS_28:
            if any(k in c for k in ["Tiền", "Giá", "Thu_", "Chi_", "Lợi Nhuận"]):
                df_edit[c] = pd.to_numeric(df_edit[c], errors='coerce').fillna(0)
        
        # Công thức tính Lợi Nhuận
        for idx, r in df_edit.iterrows():
    
            trang_thai = str(r.get('Trạng Thái Giao', '')).strip()

            # CHỈ TÍNH LN KHI ĐÃ GIAO XE
            if trang_thai != "Đã giao":
                df_edit.at[idx, 'Lợi Nhuận'] = 0
                continue
            t_thu = sum([r[c] for c in COLS_28 if "Thu_" in c])
            t_chi = sum([r[c] for c in COLS_28 if "Chi_" in c])
            df_edit.at[idx, 'Lợi Nhuận'] = t_thu - t_chi

        edited_28 = st.data_editor(
            df_edit, use_container_width=True, hide_index=True,
            column_config={
                **{c: st.column_config.NumberColumn(format="%,d") 
                for c in COLS_28 if c not in ['Khách Hàng', 'SĐT']},
                "SĐT": st.column_config.TextColumn()
            }
        )
        
        if st.button("💾 LƯU BẢNG ", type="primary", use_container_width=True):
            edited_28.to_csv(MASTER_FILE, index=False, encoding='utf-8-sig')
            st.success("✅ Đã lưu dữ liệu ")
elif st.session_state.page == "Chăm Sóc":
    st.subheader("📁 KHO LƯU TRỮ KHÁCH HÀNG HỦY & CẦN CHĂM SÓC")
    
    if os.path.exists(CS_FILE):
        df_cs = pd.read_csv(CS_FILE, dtype=str).fillna("")
        # --- PHẦN 1: MỤC TÌM KIẾM (BẤM LÀ HIỆN LIỀN) ---
        search_cs = st.text_input("🔍 Tìm kiếm khách hàng", placeholder="Nhập tên khách hoặc số điện thoại để lọc nhanh...")
        
        # Tạo bản sao để lọc hiển thị
        df_display_cs = df_cs.copy()
        if search_cs:
            mask = (df_display_cs['Khách Hàng'].str.contains(search_cs, case=False, na=False)) | \
                   (df_display_cs['SĐT'].str.contains(search_cs, case=False, na=False))
            df_display_cs = df_display_cs[mask]

        st.info(f"💡 Đang hiển thị {len(df_display_cs)} khách hàng.")      
        # Bảng hiển thị ở đây cho phép đại ca sửa lại nếu khách "quay xe" mua lại
        edited_cs = st.data_editor(
            df_cs,
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "Khách Hàng": st.column_config.TextColumn("Khách Hàng", pinned=True),
                "SĐT": st.column_config.TextColumn("Số Điện Thoại"),

                # CHUYỂN SELECTBOX SANG CỘT GHI CHÚ
                "Ghi Chú": st.column_config.SelectboxColumn(
                    "Trạng Thái (Ghi chú)",
                    options=["Cần chăm sóc", "Hủy cọc", "Đã cọc lại"]
                ),

                # Ẩn hết các cột không cần thiết (Bao gồm cả Quà tặng & Chương trình nếu có lỡ lưu trong file)
                "Chương Trình": None,
                "Quà Tặng": None,
                "Trạng Thái": None, 
                "Ngày XHĐ": None,
                "Ngày Giao Xe": None
            }
        )
        
        if st.button("💾 CẬP NHẬT KHO CHĂM SÓC", use_container_width=True):
            import csv
            
            df_to_tracking = edited_cs[edited_cs['Ghi Chú'] == "Đã cọc lại"].copy()
            df_stay_cs = edited_cs[edited_cs['Ghi Chú'] != "Đã cọc lại"].copy()
            
            # Lưu lại kho chăm sóc
            df_stay_cs.to_csv(CS_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)
            
            if not df_to_tracking.empty:
                TRACKING_FILE = "data_theo_doi_xe.csv"
                
                # Cập nhật thông tin cho việc đẩy sang Tracking
                df_to_tracking['Trạng Thái Giao'] = "Chờ giao"
                df_to_tracking['Ghi Chú'] = "Đã cọc lại"
                
                if 'Ngày' in df_to_tracking.columns:
                    df_to_tracking = df_to_tracking.rename(columns={'Ngày': 'Ngày CỌC'})

                if os.path.exists(TRACKING_FILE):
                    df_track = pd.read_csv(TRACKING_FILE, encoding='utf-8-sig', dtype=str).fillna("")
                    
                    # Cập nhật hoặc thêm mới khách hàng vào Tracking
                    for _, row in df_to_tracking.iterrows():
                        sdt_kh = row['SĐT']
                        if sdt_kh in df_track['SĐT'].values:
                            df_track.loc[df_track['SĐT'] == sdt_kh, 'Trạng Thái Giao'] = "Chờ giao"
                            df_track.loc[df_track['SĐT'] == sdt_kh, 'Ghi Chú'] = "Đã cọc lại"
                        else:
                            df_track = pd.concat([df_track, pd.DataFrame([row])], ignore_index=True)
                            
                else:
                    df_track = df_to_tracking
                
                df_track.to_csv(TRACKING_FILE, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)
                st.success(f"🎉 Khách hàng quay lại! Đã chuyển {len(df_to_tracking)} hồ sơ về bảng Theo Dõi.")
            else:
                st.success("Đã lưu thay đổi trong kho chăm sóc!")
                
            time.sleep(0.5)
            if not df_to_tracking.empty:
                st.session_state.page = "Theo Dõi"
            st.rerun()
    else:
        st.info("Kho chăm sóc hiện đang trống.")
