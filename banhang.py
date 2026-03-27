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
COLS_ORDER = [
    "Ngày", "Họ Tên", "SĐT", "CCCD", "Địa chỉ", "Xe", "Bản", "Màu", "Chính Sách", "Quà Tặng",
    "Giá Sau Ưu Đãi", "Tổng Tiền", "Trạng Thái", "Ghi Chú"
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
    # Thêm một dòng mẫu để bạn dễ hình dung
        df_empty.loc[0] = ["Tặng bộ phụ kiện 5 món", 0, "Kích hoạt"]
        df_empty.to_csv(KM_FILE, index=False)

init_data()

# --- 2. QUẢN LÝ TRẠNG THÁI ---
if 'page' not in st.session_state: st.session_state.page = "Tiếp Nhận"
if 'current_customer' not in st.session_state: st.session_state.current_customer = {}

# --- 3. MENU ĐIỀU HƯỚNG ---
st.markdown(f"### BAN HANG VINFAST | {datetime.now().strftime('%d/%m/%Y')}")

# Chia lại thành 6 cột để thêm tab Theo Dõi
c_nav1, c_nav2, c_nav3, c_nav4, c_nav5, c_nav6 = st.columns(6)

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

st.divider()

# --- 3. TRANG TIẾP NHẬN ---
if st.session_state.page == "Tiếp Nhận":
    st.subheader("📝 Phiếu Tiếp Nhận Khách Hàng")
    df_p = pd.read_csv(PRICE_FILE)
    df_po = pd.read_csv(POLICY_FILE)
    df_i = pd.read_csv(INSURANCE_FILE)
    col_policy_name = "Tên Chương Trình" if "Tên Chương Trình" in df_po.columns else df_po.columns[0]
    if 'reset_key' not in st.session_state:
        st.session_state.reset_key = 0
    k = st.session_state.reset_key
    with st.container(border=True):
        st.markdown("#### 👤 I. Thông tin khách hàng")
        c1, c2, c3 = st.columns(3)
        r_name = c1.text_input("Họ và Tên", key=f"name_{k}")
        r_phone = c1.text_input("Số điện thoại (10 số)", key=f"phone_{k}", max_chars=10)
        if r_phone:
            if not r_phone.isdigit():
                st.error("⚠️ SĐT chỉ được nhập số!")
            elif len(r_phone) != 10:
                st.warning("👉 SĐT phải có đúng 10 số.")
        r_address = c2.text_input("Địa chỉ (Quận/Huyện)", key=f"address_{k}")
        r_cccd = c2.text_input("Số CCCD (12 số)", key=f"cccd_{k}", max_chars=12)
        if r_cccd:
            if not r_cccd.isdigit():
                st.error("⚠️ CCCD chỉ được nhập số!")
            elif len(r_cccd) != 12:
                st.warning("👉 CCCD phải có đúng 12 số.")
        r_mail = c3.text_input("Email", key=f"mail_{k}")
        r_date = c3.date_input("Ngày tiếp nhận", value=datetime.now(), key=f"date_{k}")

        st.divider()
        st.markdown("#### 🚗 II. Xe quan tâm & Chính sách")
        cx1, cx2, cx3 = st.columns(3)
        r_car = cx1.selectbox("Dòng xe", df_p['Dòng Xe'].unique().tolist())
        r_ver = cx1.selectbox("Phiên bản", df_p[df_p['Dòng Xe'] == r_car]['Phiên Bản'].tolist())
        r_policy = cx2.selectbox("Chương trình ưu đãi", df_po[col_policy_name].tolist())
        r_ins_label = cx2.selectbox("Loại Bảo hiểm DS", df_i['Loại xe'].tolist())
        r_color = cx3.text_input("Màu sắc ngoại thất", key=f"color_{k}")
        r_status = cx3.selectbox("Trạng thái", ["Tư vấn", "Đã cọc", "Tiền mặt"], index=0)

    if st.button("💰 XEM BÁO GIÁ CHI TIẾT", type="primary"):
        pol_val = int(df_po[df_po[col_policy_name] == r_policy].iloc[0, 1])
        ins_val = int(df_i[df_i['Loại xe'] == r_ins_label].iloc[0, 1])
        
        st.session_state.current_customer = {
            "name": r_name, "phone": r_phone, "address": r_address, "cccd": r_cccd,
            "mail": r_mail, "date": r_date, "car": r_car, "ver": r_ver,
            "policy_name": r_policy, "policy_val": pol_val, 
            "ins_label": r_ins_label, "ins_price": ins_val,
            "color": r_color, "status": r_status
        }
        st.session_state.page = "Báo Giá"; st.rerun()

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
        st.markdown("### Thông tin chi tiết ")
        
        with st.expander("1. Giá xe & Ưu đãi", expanded=True):
            edit_base = st.number_input("Giá niêm yết (VNĐ)", value=base_price_init, step=1000000)
            edit_discount_main = st.number_input("Ưu đãi/Voucher (VNĐ)", value=q.get('policy_val', 0), step=500000)
            edit_discount_extra = st.number_input("Giảm giá % (VNĐ)", value=q.get('add_discount', 0), step=500000)
            gia_ban_sau_uu_dai = edit_base - edit_discount_main - edit_discount_extra

    # Đọc dữ liệu gốc
        # --- PHẦN KHUYẾN MÃI TỰ ĐỘNG ---
        with st.expander("🎁 2. Chương trình Khuyến mãi & Quà tặng", expanded=True):
            selected_km_data = []
            
            # 1. Đọc dữ liệu từ file khuyến mãi
            try:
                df_km = pd.read_csv('chuong_trinh_khuyen_mai.csv')
            except:
                df_km = pd.DataFrame(columns=['Tên chương trình', 'Giá trị (VNĐ)'])

            # 2. Tự động tạo Checkbox cho từng dòng trong file CSV
            c_km1, c_km2 = st.columns(2)
            for i, (idx, row) in enumerate(df_km.iterrows()):
                km_name = row['Tên chương trình']
                try:
                    km_val = int(pd.to_numeric(row['Giá trị (VNĐ)'], errors='coerce'))
                    if pd.isna(km_val): km_val = 0
                except:
                    km_val = 0
                
                # Chia 2 cột hiển thị cho gọn
                target_col = c_km1 if i % 2 == 0 else c_km2
                
                # Hiển thị Checkbox
                label_display = f"{km_name}" if km_val == 0 else f"{km_name} (Trị giá: {km_val:,} VNĐ)"
# Thêm key='qt_' để nút lưu tự quét được
                if target_col.checkbox(label_display, value=False, key=f"qt_{km_name}"): 
                    selected_km_data.append({"label": km_name, "value": km_val})
            # Lưu vào session_state để trang Hợp Đồng sử dụng 
            st.session_state.selected_km_list = selected_km_data

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

       
        with st.expander("4. Phương thức Ngân hàng", expanded=True):
            vay_percent = st.slider("Tỷ lệ vay (%)", 0, 100, 85)
            so_tien_vay = int(gia_ban_sau_uu_dai * vay_percent / 100)
            tra_truoc_xe = gia_ban_sau_uu_dai - so_tien_vay

        st.session_state['gia_sau_uu_dai_shared'] = gia_ban_sau_uu_dai 

        # 2. Lưu đúng TỔNG CHI PHÍ ĐĂNG KÝ (Dòng 20 Quyết toán)
        st.session_state['chi_phi_dk_shared'] = tong_chi_phi_dk
        
        # 3. Lưu thông tin vay vốn (Để hiện bên Tab Ngân hàng)
        st.session_state['so_tien_vay_shared'] = so_tien_vay
        st.session_state['tra_truoc_xe_shared'] = tra_truoc_xe
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
        tong_tien_mat = gia_ban_sau_uu_dai + tong_chi_phi_dk
        # Giả sử bạn đã có biến so_tien_vay, tra_truoc_xe, vay_percent từ phần code trước đó
        tong_tra_truoc_nh_ = tra_truoc_xe + tong_chi_phi_dk

        # --- NỘI DUNG TAB TIỀN MẶT ---
        with tab_cash:
            st.write(f"1. Tiền xe (1): **{gia_ban_sau_uu_dai:,} VNĐ**")
            st.write(f"2. Chi phí đăng ký (2): **{tong_chi_phi_dk:,} VNĐ**")
            st.markdown(f"<h3 style='color: red;'>TỔNG CỘNG (1)+(2): {tong_tien_mat:,} VNĐ</h3>", unsafe_allow_html=True)

        # --- NỘI DUNG TAB NGÂN HÀNG (ĐÃ THÊM CODE VÀO ĐÂY) ---
        with tab_bank:
            st.write(f"1. Ngân hàng hỗ trợ ({vay_percent}%): **{so_tien_vay:,} VNĐ**")
            st.write(f"2. Khách trả trước xe ({100-vay_percent}%): **{tra_truoc_xe:,} VNĐ**")
            st.write(f"3. Chi phí đăng ký: **{tong_chi_phi_dk:,} VNĐ**")
            st.markdown(f"<h3 style='color: #1E90FF;'>TỔNG TIỀN TRẢ TRƯỚC: {tong_tra_truoc_nh_:,} VNĐ</h3>", unsafe_allow_html=True)
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
    if st.button("💾 LƯU HỒ SƠ & QUAY LẠI TIẾP NHẬN", type="primary", width="stretch"):
        try:
            # 1. LẤY CHÍNH SÁCH LINH ĐỘNG
            q = st.session_state.current_customer
            # Lấy tên chương trình ưu đãi (Vd: VF3 Giảm TC 1) đang hiện ở bảng trên
            str_chinh_sach = q.get('policy_name', "Ưu đãi VinFast")

            # 2. GÔM QUÀ TẶNG LINH ĐỘNG (Quét mọi checkbox có key bắt đầu bằng qt_)
            list_qt = [k.replace("qt_", "") for k, v in st.session_state.items() if k.startswith("qt_") and v == True]
            str_qua_tang = ", ".join(list_qt) if list_qt else "Không có"
            
            raw_date = q.get('date', datetime.now())
            try:
                str_ngay = raw_date.strftime("%d/%m/%Y")
            except:
                str_ngay = str(raw_date)
            # 3. LƯU VÀO BỘ NHỚ TẠM (Để trang Quyết Toán và Theo Dõi bốc đi)
            st.session_state['temp_chinh_sach'] = str_chinh_sach
            st.session_state['temp_qua_tang'] = str_qua_tang

            # 4. TẠO DÒNG DỮ LIỆU TỔNG HỢP
            final_data = {
                "Ngày": str_ngay,
                "Họ Tên": q.get('name', 'N/A'),
                "SĐT": q.get('phone', ''),
                "CCCD": q.get('cccd', ''),
                "Địa Chỉ": q.get('address', ''),
                "Xe": q.get('car', ''),
                "Bản": q.get('ver', ''),
                "Màu": q.get('color', ''),
                "Chính Sách": str_chinh_sach, 
                "Quà Tặng": str_qua_tang,
                "Giá Sau Ưu Đãi": gia_ban_sau_uu_dai,
                "Tổng Tiền": tong_tien_mat,
                "Trạng Thái": "Đã báo giá",
                "Ghi Chú": ""
            }

            # 5. GHI VÀO FILE CSV CHUNG
            new_row_df = pd.DataFrame([final_data])
            new_row_df.to_csv(DATA_FILE, mode='a', index=False, header=not os.path.exists(DATA_FILE), encoding='utf-8-sig')

            st.success(f"🎉 Đã lưu khách hàng {q.get('name')}!")
            
            time.sleep(1)
            st.session_state.page = "Tiếp Nhận"
            st.rerun()

        except Exception as e:
            st.error(f"Lỗi khi lưu dữ liệu linh động: {e}")
# --- 6. TRANG QUẢN LÝ ---
elif st.session_state.page == "Quản Lý Giá":
    st.subheader("⚙️ Cấu Hình Thông Số")
    t1, t2, t3, t4, t5 = st.tabs(["🚗 Bảng Giá Xe", "📜 Chi Phí Đăng Ký", "🎁 Chính Sách", "🛡️ Bảng Phí Bảo Hiểm", "Chương trình khuyến mãi "])
    
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

elif st.session_state.page == "Quyết Toán":
    q = st.session_state.current_customer
    st.subheader(f"📑 QUYẾT TOÁN VỚI CÔNG TY - {q.get('name', 'KHÁCH HÀNG').upper()}")

    # --- LOGIC TỰ ĐỘNG LẤY GIÁ THEO XE ---
    # Đọc file giá xe
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

    # Ô nhập A duy nhất (Dùng key động để nhảy số khi đổi khách)
    A = st.number_input(
        "1. Giá Niêm Yết (A)", 
        value=int(gia_mac_dinh_a), 
        step=1000000,
        key=f"fixed_A_{q.get('Họ Tên', 'none')}"
    )

    col_input, col_table = st.columns([1.1, 1])
    # ... các phần code Checkbox chung hàng phía dưới giữ nguyên ...

    with col_input:
        with st.expander("🏢 Cấu hình Giá & Giảm trừ hóa đơn", expanded=True):
            # 1. Giá niêm yết (Luôn hiện)
            # --- MỤC GIẢM GIÁ (HIỂN THỊ GỌN TRÊN 1 HÀNG) ---
        
        # Dòng 2: Giảm 6%
            c2_1, c2_2 = st.columns([1, 1]) # Chia đôi hàng
            ck_b = c2_1.checkbox("2. Giảm 6% (B)")
            val_b = c2_2.number_input("Số tiền B", value=int(A*0.06), step=100000, label_visibility="collapsed") if ck_b else 0
            # Chú thích: label_visibility="collapsed" để ẩn chữ "Số tiền B" cho gọn

            # Dòng 3: Giảm 10% VF8/9
            c3_1, c3_2 = st.columns([1, 1])
            ck_b10 = c3_1.checkbox("3. Giảm 10% VF8, 9")
            val_b10 = c3_2.number_input("Số tiền 10%", value=int(A*0.1), step=100000, label_visibility="collapsed") if ck_b10 else 0

            # Dòng 7: Xăng Sang Điện
            c7_1, c7_2 = st.columns([1, 1])
            ck_d = c7_1.checkbox("7. Xăng Sang Điện (D)")
            val_d = c7_2.number_input("Số tiền D", value=30000000, step=1000000, label_visibility="collapsed") if ck_d else 0

            # Dòng 9: VinClub 1%
            c9_1, c9_2 = st.columns([1, 1])
            ck_e = c9_1.checkbox("9. VinClub 1% (E)")
            val_e = c9_2.number_input("Số tiền E", value=int((A-val_b-val_d)*0.01), step=100000, label_visibility="collapsed") if ck_e else 0

            # Dòng 10: Giảm Khung
            c10_1, c10_2 = st.columns([1, 1])
            ck_f = c10_1.checkbox("10. Giảm Khung (F)")
            val_f = c10_2.number_input("Số tiền F", value=5000000, step=1000000, label_visibility="collapsed") if ck_f else 0
    with col_table:
        # --- BƯỚC 3: TÍNH TOÁN (Lúc này máy đã biết A là gì rồi) ---
        G = A - val_b - val_d - val_e - val_f
        
        st.markdown("#### 📋 CHI TIẾT BẢNG TÍNH")
        
        # Chỉ đưa vào bảng những dòng đã được tích chọn
        rows = [["1", "Giá Niêm Yết (A)", f"{A:,}", "A"]]
        if ck_b:   rows.append(["2", "Giảm 6%", f"-{val_b:,}", "B"])
        if ck_b10: rows.append(["3", "Giảm 10% VF8/9", f"-{val_b10:,}", ""])
        if ck_d:   rows.append(["7", "Xăng Sang Điện", f"-{val_d:,}", "D"])
        if ck_e:   rows.append(["9", "VinClub 1%", f"-{val_e:,}", "E"])
        if ck_f:   rows.append(["10", "Giảm Khung", f"-{val_f:,}", "F"])
        
        # Dòng tổng chốt luôn hiện
        rows.append(["11", "**GIÁ HĐ ( XHĐ )**", f"**{G:,}**", "**G=A-B-D-E-F**"])
        
        st.table(pd.DataFrame(rows, columns=["STT", "Nội dung", "Số tiền (VNĐ)", "Note"]))
        st.error(f"### TỔNG CÔNG TY THU (G): {G:,} VNĐ")

        # Hiển thị Tổng cộng to rõ
        

    if st.button("💾 LƯU QUYẾT TOÁN CÔNG TY", width="stretch"):
        st.success(f"Đã lưu bảng tính hóa đơn cho khách {q.get('name')}!")

#    G = A - val_b - val_d - val_e - val_f
#    I = G - 0  # Nếu có giảm trừ thêm thì trừ ở đây, nếu không I = G

    # --- MỤC II: QUYẾT TOÁN VỚI KHÁCH HÀNG ---
    st.markdown("---")
    st.subheader(f"👤 II. QUYẾT TOÁN VỚI KHÁCH HÀNG")

    col_kh_in, col_kh_out = st.columns([1.1, 1])

    with col_kh_in:
        with st.expander("📝 Chi phí Đăng ký & Đối ứng", expanded=True):
            # Lấy giá chốt từ Báo Giá sang (ép kiểu int)
            # Lấy giá từ bộ nhớ (Lúc này sẽ là 281,060,000)
            gia_xe_moi = st.session_state.get('gia_sau_uu_dai_shared', 0)

            # Dùng key có chứa giá trị để ép làm mới ô nhập
            gia_chot_kh = st.number_input(
                "17. Giá Chốt KH",
                value=int(gia_xe_moi),
                step=1000000,
                key=f"force_fix_price_{gia_xe_moi}" # CỰC KỲ QUAN TRỌNG: Giá đổi -> Key đổi -> Số nhảy
            )

            # 18. Ngân hàng (Mặc định lấy từ Báo giá nếu có)
            val_vay_mac_dinh = st.session_state.get('so_tien_vay_shared', 0)
            c18_1, c18_2 = st.columns([1, 1])
            ck_vay = c18_1.checkbox("18. Ngân hàng cho vay", value=True if val_vay_mac_dinh > 0 else False)
            val_vay = c18_2.number_input("Số tiền vay", value=int(val_vay_mac_dinh), step=1000000, label_visibility="collapsed") if ck_vay else 0

            # 20. Chi phí đăng ký (Lấy từ Báo giá)
            val_dk_mac_dinh = st.session_state.get('chi_phi_dk_shared', 0)
            c20_1, c20_2 = st.columns([1, 1])
            ck_dk = c20_1.checkbox("20. Chi Phí Đăng Ký (Thu hộ)", value=True if val_dk_mac_dinh > 0 else False)
            val_dk = c20_2.number_input("Số tiền ĐK", value=int(val_dk_mac_dinh), step=100000, label_visibility="collapsed") if ck_dk else 0

            # 21. Tiền Cọc
            c21_1, c21_2 = st.columns([1, 1])
            ck_coc = c21_1.checkbox("21. Tiền khách đã Cọc")
            val_coc = c21_2.number_input("Số tiền cọc", value=10000000, step=1000000, label_visibility="collapsed") if ck_coc else 0
    with col_kh_out:
        # TÍNH TOÁN TIỀN KH THANH TOÁN (Dòng 22)
        tien_xe_con_lai = gia_chot_kh - val_vay - val_coc
        tong_kh_dong = tien_xe_con_lai + val_dk

        st.markdown("#### 📋 CHI TIẾT THU TIỀN KHÁCH")
        
        # Bắt đầu khởi tạo danh sách hàng cho bảng
        # Dòng 17 (Giá chốt) luôn hiện vì là gốc
        rows_kh = [["17", "Giá Chốt KH", f"{gia_chot_kh:,}", ""]]

        # Chỉ thêm các dòng khác vào bảng nếu checkbox ĐÃ ĐƯỢC TÍCH
        if ck_vay:
            rows_kh.append(["18",  "Số Tiền Vay", f"-{val_vay:,}", "Ngân hàng"])
        
        if ck_dk:
            rows_kh.append(["20", "Chi Phí ĐK", f"{val_dk:,}", "Thu hộ"])
            
        if ck_coc:
            rows_kh.append(["21", "Tiền Cọc", f"-{val_coc:,}", "Đã thu"])

        # Dòng 22: TỔNG THANH TOÁN luôn hiện ở cuối
        rows_kh.append(["22", "**KH THANH TOÁN (CK)**", f"**{tong_kh_dong:,}**", "Chốt"])

        # Tạo DataFrame và hiển thị bảng (Ẩn cột index 0, 1, 2 rườm rà)
        import pandas as pd
        df_kh = pd.DataFrame(rows_kh, columns=["STT", "Nội dung", "Số tiền (VNĐ)", "Ghi chú"])
        
        # Sử dụng st.table để giao diện giống y hệt phần Công ty
        st.table(df_kh)

        # HIỆN TỔNG THU KHÁCH TRONG KHUNG CẢNH BÁO
        st.warning(f"### 💰 TỔNG THU KHÁCH: {tong_kh_dong:,} VNĐ")
    # NÚT XUẤT FILE HOẶC LƯU
   # --- PHẦN KẾT THÚC: LƯU DỮ LIỆU & CHUYỂN TRANG ---
    st.divider()
    col_btn1, col_btn2 = st.columns(2)

    # Nút 1: Xác nhận và nhảy sang trang Danh Sách
    # --- TẠI TRANG QUYẾT TOÁN ---
    if col_btn1.button("✅ XÁC NHẬN & XEM DANH SÁCH", width="stretch", type="primary"):
        try:
            # 1. CẬP NHẬT TRẠNG THÁI VÀO FILE TỔNG (DATA_FILE)
            if os.path.exists(DATA_FILE):
                df_all = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
                q = st.session_state.current_customer
                # Ưu tiên lấy 'name' vì thường bạn đặt biến ở Tiếp Nhận là name
                ten_kh = q.get('name') or q.get('Họ Tên') 
                
                if ten_kh in df_all['Họ Tên'].values:
                    mask = df_all['Họ Tên'] == ten_kh
                    df_all.loc[mask, 'Trạng Thái'] = "Đã Quyết Toán"
                    df_all.loc[mask, 'Giá Sau Ưu Đãi'] = gia_chot_kh
                    df_all.loc[mask, 'Tổng Tiền'] = tong_kh_dong
                    df_all.loc[mask, 'Ngày QT'] = datetime.now().strftime("%d/%m/%Y")
                    df_all.loc[mask, 'Tiền Cọc'] = val_coc if locals().get('ck_coc') else 0
                    df_all.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

            # 2. GHI VÀO FILE THEO DÕI RIÊNG (TRACKING_FILE)
            tracking_row = {
                "Khách Hàng": q.get('Họ Tên') or q.get('name') or "Khách chưa có tên", 
    
    # SỬA Ở ĐÂY: Thay 'car' bằng 'Xe' cho khớp với Ảnh 1 của bạn
                "Loại Xe": f"{q.get('Xe') or q.get('car') or 'Chưa chọn xe'} {q.get('Bản') or q.get('ver') or ''}",
                "Ngày CỌC": datetime.now().strftime("%d/%m/%Y"),
                "Ngày XHĐ": "", "Ngày Giao Xe": "", 
                "Số Tiền HĐ": G if 'G' in locals() else 0,
                "Số Tiền Thực Thu": tong_kh_dong,
                "Số Tiền Chốt Khách": gia_chot_kh,
                "Tiền Cọc": val_coc if locals().get('ck_coc') else 0,
                "Chính Sách": st.session_state.get('temp_chinh_sach', "Ưu đãi VinFast"),
                "Quà Tặng": st.session_state.get('temp_qua_tang', "Không có"),
                "Trạng Thái Giao": "Chờ giao",
                "Ghi Chú": ""
            }
            
            df_new = pd.DataFrame([tracking_row])
            df_new.to_csv(TRACKING_FILE, mode='a', index=False, header=not os.path.exists(TRACKING_FILE), encoding='utf-8-sig')
            
            # 3. THÀNH CÔNG & CHUYỂN TRANG
            st.success(f"🎉 Đã chốt xong hồ sơ khách {ten_kh}!")
            
            # Chỉ cần rerun 1 lần là đủ
            st.session_state.page = "Theo Dõi"
            st.rerun()

        except Exception as e:
            st.error(f"Lỗi lưu dữ liệu: {e}")
            # 3. CHUYỂN TRANG
            
    
# --- 7. TRANG DANH SÁCH ---
elif st.session_state.page == "Danh Sách":
    st.subheader("📊 Quản lý Danh Sách Khách Hàng")
    
    if os.path.exists(DATA_FILE):
        try:
            # 1. Đọc dữ liệu từ file CSV
            df_list = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
            
            # --- PHẦN CHỌN KHÁCH HÀNG QUYẾT TOÁN ---
            st.markdown("### 📑 Chốt Quyết Toán")
            col_select, col_btn = st.columns([3, 1])
            
            list_names = df_list['Họ Tên'].tolist()
            selected_name = col_select.selectbox(
                "Chọn khách hàng:", 
                list_names, 
                index=None, 
                placeholder="Chọn tên khách để quyết toán..."
            )
          
            if col_btn.button("🚀 Sang Quyết Toán", width="stretch") and selected_name:
                row_kh = df_list[df_list['Họ Tên'] == selected_name].iloc[0]
                
                # Lấy con số 281tr từ cột mới lưu
                gia_xe_chuan = row_kh.get('Giá Sau Ưu Đãi', row_kh.get('Tổng Tiền', 0))
                
                st.session_state.current_customer = row_kh.to_dict()
                st.session_state.gia_sau_uu_dai_shared = gia_xe_chuan # Gửi 281tr đi
                st.session_state.page = "Quyết Toán"
                st.rerun()
            
            st.divider()

            # --- PHẦN HIỂN THỊ BẢNG SỬA/XÓA (GIỮ NGUYÊN) ---
            st.markdown("### 📝 Chỉnh sửa danh sách")
            edited = st.data_editor(
                df_list, 
                num_rows="dynamic", 
                width="stretch", 
                hide_index=True,
                column_config={
                    "Tổng Tiền": st.column_config.NumberColumn(format="%,d"),
                    "Giá Sau Ưu Đãi": st.column_config.NumberColumn(format="%,d")
                }
            )
            
            if st.button("💾 CẬP NHẬT THAY ĐỔI", width="stretch"):
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
        # Đọc dữ liệu từ file riêng, không dùng DATA_FILE chung nữa
        df_follow = pd.read_csv(TRACKING_FILE, encoding='utf-8-sig')

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
                "Trạng Thái Giao": st.column_config.SelectboxColumn(
                    "Trạng Thái Giao",
                    options=["Chờ giao", "Đã giao"],
                    required=True,
                ),
                "Số Tiền HĐ": st.column_config.NumberColumn(format="%,d"),
                "Số Tiền Thực Thu": st.column_config.NumberColumn(format="%,d"),
                "Số Tiền Chốt Khách": st.column_config.NumberColumn(format="%,d"),
                "Tiền Cọc": st.column_config.NumberColumn(format="%,d"),
            }
        )

        # 4. NÚT LƯU CẬP NHẬT (Lưu những gì bạn vừa sửa trong bảng)
        # --- TẠI TRANG QUYẾT TOÁN ---
        # 4. NÚT LƯU CẬP NHẬT (Lưu lại những gì bạn sửa trực tiếp trên bảng như Ngày XHĐ, Ngày Giao)
        if st.button("💾 CẬP NHẬT THAY ĐỔI TRÊN BẢNG", type="primary", use_container_width=True):
            try:
                # LƯU Ý: Ở đây ta lưu biến 'edited_df' (dữ liệu bạn vừa sửa trên màn hình)
                edited_df.to_csv(TRACKING_FILE, index=False, encoding='utf-8-sig')
                st.success("✅ Đã cập nhật thông tin bàn giao xe thành công!")
                
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi lưu cập nhật: {e}")
                
    else:
        # Đoạn này xử lý khi chưa có file (Thụt lề đúng 1 Tab so với 'if os.path.exists')
        st.info("Chưa có hồ sơ nào được chốt sang bảng Theo Dõi.")
        st.caption("Hãy hoàn tất bước 'Quyết Toán' cho khách hàng để đưa họ vào danh sách này.")
