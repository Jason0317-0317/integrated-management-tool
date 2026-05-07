import streamlit as st
import pandas as pd
import io
from datetime import datetime
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import numpy as np

# ========================
# 頁面設定
# ========================
st.set_page_config(page_title="整合管理工具", layout="wide")

# ========================
# Session State 初始化
# ========================
if "role" not in st.session_state:
    st.session_state.role = None
if "feature" not in st.session_state:
    st.session_state.feature = None

# ========================
# 步驟 1: 選擇身份
# ========================
if st.session_state.role is None:
    st.markdown("""
    <style>
    .main-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 100px;'>春不老薪資計算系統</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #999; font-size: 16px;'>請選擇您的角色登入系統</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("店長登入", key="manager_btn", use_container_width=True):
                st.session_state.role = "manager"
                st.rerun()
        
        with col_btn2:
            if st.button("小編登入", key="editor_btn", use_container_width=True):
                st.session_state.role = "editor"
                st.rerun()
        


# ========================
# 步驟 2: 選擇功能
# ========================
elif st.session_state.feature is None:
    # 頂部返回按鈕
    col_back, col_title = st.columns([1, 10])
    with col_back:
        if st.button("返回", key="back_to_role"):
            st.session_state.role = None
            st.session_state.feature = None
            st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.role == "manager":
            st.markdown("<h1 style='text-align: center; margin-top: 50px;'>店長功能選擇</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #999; font-size: 16px;'>請選擇您要使用的功能</p>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                if st.button("預約報表統計", key="lesson_report", use_container_width=True):
                    st.session_state.feature = "lesson_report"
                    st.rerun()
            
            with col_f2:
                if st.button("業績報表轉換", key="sales_report", use_container_width=True):
                    st.session_state.feature = "sales_report"
                    st.rerun()
        
        else:  # editor
            st.markdown("<h1 style='text-align: center; margin-top: 50px;'>小編功能選擇</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #999; font-size: 16px;'>請選擇您要使用的功能</p>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("業務獎金計算", key="editor_bonus", use_container_width=True):
                st.session_state.feature = "editor_bonus"
                st.rerun()

# ========================
# 步驟 3: 顯示功能
# ========================
else:
    # 頂部導航
    col_back, col_title, col_empty = st.columns([1, 10, 1])
    with col_back:
        if st.button("返回", key="back_to_feature"):
            st.session_state.feature = None
            st.rerun()
    
    # ===== 預約報表統計 =====
    if st.session_state.feature == "lesson_report":
        st.title("預約報表自動統計系統")
        st.markdown("此版本會將 **課程項目顯示於直排**，**老師姓名顯示於橫排**。")
        
        # 1. 定義老師排序順序與轉換字典
        NAME_CONVERSION = {
            "意潔": "林意潔", "Cammy": "陳怡廷", "Vivi": "陳秀蓉", "怡廷": "陳怡廷", 
            "秀蓉": "陳秀蓉", "佳蓁": "鍾佳蓁 Rita", "宛婷": "黃宛婷", "WanTing": "黃宛婷",
            "小在": "楊子慧(小在)", "Jae": "楊子慧(小在)", "LOUIS": "許力尹 LOUIS", 
            "許力尹": "許力尹 LOUIS", "顥顥": "顥顥", "睿絃": "洪睿絃", "儒蓁": "紀儒蓁",
            "翎瑋": "李翎瑋", "奕伶": "郭奕伶", "品均": "郭品均", "妍語": "邴妍語", 
            "鈞弼": "張鈞弼", "竣升": "蕭竣升", "萃萃": "紀萃文", "萃文": "紀萃文", 
            "函豫": "李函豫", "Hanny": "遊函豫", "子綺": "尤子綺", "Yuli": "尤子綺", 
            "楷翌": "張楷翌", "Eric": "張楷翌", "懿庭": "侯懿庭", "Yvonne Hou": "侯懿庭", 
            "俐池": "謝俐池", "Grace Hsieh": "謝俐池", "姿菁": "黃姿菁", "郁雯": "籃郁雯", 
            "徐漫": "徐漫", "mandy": "徐漫", "漫漫": "徐漫", "筠馨": "鄭筠馨", 
            "舒涵": "高舒涵", "靜瑜": "邱靜瑜"
        }
        
        # 建立排序參考清單
        TEACHER_ORDER = list(dict.fromkeys(NAME_CONVERSION.values()))
        
        # 名稱轉換函數
        def get_formal_name(raw_name):
            name_str = str(raw_name).strip()
            for key, formal_name in NAME_CONVERSION.items():
                if key.lower() in name_str.lower():
                    return formal_name
            return name_str
        
        # 排序權重函數
        def teacher_sort_key(name):
            if name in TEACHER_ORDER:
                return TEACHER_ORDER.index(name)
            return len(TEACHER_ORDER)
        
        # --- 篩選條件區塊 ---
        st.markdown("### 1. 設定篩選條件")
        col_branch, col_date = st.columns(2)
        
        with col_branch:
            selected_branch = st.selectbox(
                "選擇館別", 
                ["全部", "中山館", "高美館", "義昌館", "巨蛋館"],
                key="branch_select"
            )
        
        with col_date:
            today = datetime.today()
            first_day_of_month = today.replace(day=1)
            date_range = st.date_input(
                "選擇日期區間",
                value=(first_day_of_month, today),
                help="請選取開始與結束日期",
                key="date_range"
            )
        
        if len(date_range) != 2:
            st.warning("請在日曆上選擇完整的開始與結束日期。")
            st.stop()
        
        # --- 檔案上傳區塊 ---
        st.markdown("### 2. 上傳報表檔案")
        uploaded_file = st.file_uploader("選擇原始檔案 (Excel 或 CSV)", type=["xlsx", "csv"], key="lesson_uploader")
        
        if uploaded_file is not None:
            try:
                def get_clean_df(file):
                    if file.name.endswith(('.xlsx', '.xls')):
                        temp_df = pd.read_excel(file, header=None, nrows=20)
                        file.seek(0)
                        target_row = 0
                        for i, row in temp_df.iterrows():
                            row_str = " ".join([str(x) for x in row.values])
                            if '課程日期' in row_str or '授課老師' in row_str:
                                target_row = i
                                break
                        return pd.read_excel(file, skiprows=target_row)
                    else:
                        encodings = ['utf-8-sig', 'big5', 'cp950', 'gbk']
                        for enc in encodings:
                            try:
                                file.seek(0)
                                df = pd.read_csv(file, encoding=enc)
                                if '課程日期' not in "".join(df.columns.astype(str)):
                                    file.seek(0)
                                    df = pd.read_csv(file, encoding=enc, skiprows=1)
                                return df
                            except:
                                continue
                        return None
                
                df = get_clean_df(uploaded_file)
                
                if df is None or df.empty:
                    st.error("無法辨識檔案格式或找不到『課程日期』。")
                    st.stop()
                
                df.columns = df.columns.astype(str).str.strip()
                
                def find_col(possible_names):
                    for name in possible_names:
                        for col in df.columns:
                            if name in col and "Unnamed" not in col:
                                return col
                    return None
                
                date_col = find_col(['課程日期', '日期'])
                teacher_col = find_col(['授課老師', '老師'])
                course_col = find_col(['課程名稱', '課程'])
                count_col = find_col(['預約總人數', '預約人數', '人數'])
                duration_col = find_col(['課程時數', '分鐘'])
                branch_col = find_col(['館別', '分館'])
                
                if not date_col or not teacher_col:
                    st.error(f"缺少必要欄位。偵測到的欄位有：{list(df.columns)}")
                    st.stop()
                
                # 資料清洗與篩選
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.dropna(subset=[date_col])
                
                if branch_col and selected_branch != "全部":
                    df = df[df[branch_col].astype(str).str.contains(selected_branch)]
                
                start_date, end_date = date_range
                df = df[(df[date_col].dt.date >= start_date) & (df[date_col].dt.date <= end_date)]
                
                df[count_col] = pd.to_numeric(df[count_col], errors='coerce').fillna(0)
                df_filtered = df[df[count_col] > 0].copy()
                
                # 轉換正式姓名
                df_filtered['正式姓名'] = df_filtered[teacher_col].apply(get_formal_name)
                
                # 統計邏輯
                stats_items = [
                    '團1人', '團2人', '團3人', '團4人', '團5人', '團6人',
                    '1對2(1.5hr)', '1對2', '1對1(1.5hr)', '1對1', '觀課'
                ]
                
                all_formal_teachers = df_filtered['正式姓名'].unique().tolist()
                df_stats = pd.DataFrame(0, index=all_formal_teachers, columns=stats_items)
                
                for _, row in df_filtered.iterrows():
                    teacher = row['正式姓名']
                    course_name = str(row[course_col]).strip()
                    count = int(row[count_col])
                    duration = row[duration_col] if duration_col else 60
                    
                    if '觀課' in course_name:
                        df_stats.at[teacher, '觀課'] += 1
                    elif '一對一' in course_name:
                        if duration >= 90: df_stats.at[teacher, '1對1(1.5hr)'] += 1
                        else: df_stats.at[teacher, '1對1'] += 1
                    elif '一對二' in course_name:
                        if duration >= 90: df_stats.at[teacher, '1對2(1.5hr)'] += 1
                        else: df_stats.at[teacher, '1對2'] += 1
                    else:
                        if 1 <= count <= 6:
                            col_name = f'團{count}人'
                            df_stats.at[teacher, col_name] += 1
                
                # 計算小計
                df_stats['小計'] = df_stats.sum(axis=1)
                
                # 排序老師
                df_stats['sort_key'] = df_stats.index.map(teacher_sort_key)
                df_stats = df_stats.sort_values('sort_key').drop(columns=['sort_key'])
                
                # 計算合計
                total_row = df_stats.sum().to_frame().T
                total_row.index = ['合計']
                df_final_with_total = pd.concat([df_stats, total_row])
                
                # 轉置
                df_transposed = df_final_with_total.T
                df_transposed.index.name = "課程項目 \ 姓名"
                
                # 介面呈現
                st.success("檔案處理成功。")
                st.info(f"統計館別：{selected_branch} | 統計區間：{start_date} 至 {end_date}")
                
                tab_stat, tab_detail = st.tabs(["橫向統計表", "原始明細對照"])
                with tab_stat:
                    st.dataframe(df_transposed, use_container_width=False)
                with tab_detail:
                    st.dataframe(df_filtered[[date_col, course_col, teacher_col, '正式姓名', count_col]], use_container_width=True, hide_index=True)
                
                # 下載 Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    info_df = pd.DataFrame([
                        ['統計館別', selected_branch],
                        ['統計區間', f"{start_date} 至 {end_date}"]
                    ])
                    
                    info_df.to_excel(writer, sheet_name='統計總表', index=False, header=False, startrow=0)
                    df_transposed.to_excel(writer, sheet_name='統計總表', startrow=3)
                    
                    df_transposed_v2 = df_transposed.copy()
                    if '團1人' in df_transposed_v2.index and '團2人' in df_transposed_v2.index:
                        df_transposed_v2.loc['團1-2人'] = df_transposed_v2.loc['團1人'] + df_transposed_v2.loc['團2人']
                        df_transposed_v2 = df_transposed_v2.drop(['團1人', '團2人'])
                        new_index = ['團1-2人'] + [i for i in df_transposed_v2.index if i != '團1-2人']
                        df_transposed_v2 = df_transposed_v2.reindex(new_index)
                    
                    info_df.to_excel(writer, sheet_name='統計總表2', index=False, header=False, startrow=0)
                    df_transposed_v2.to_excel(writer, sheet_name='統計總表2', startrow=3)
                    
                    df_filtered.to_excel(writer, sheet_name='預約報表明細', index=False)
                
                st.download_button(
                    label="下載橫向 Excel 報表",
                    data=buffer.getvalue(),
                    file_name=f"預約統計_{selected_branch}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            except Exception as e:
                st.error(f"處理失敗: {e}")
                st.exception(e)
    
    # ===== 業績報表轉換 =====
    elif st.session_state.feature == "sales_report":
        st.title("業績報表自動化轉換工具")
        st.write("請上傳原始交易報表，系統將自動提取並整理為指定格式。")
        
        def get_unit_price(contract_type):
            contract_type = str(contract_type)
            if '一對一' in contract_type:
                return 2300
            elif '一對二' in contract_type:
                return 1300
            elif '一對三' in contract_type:
                return 1050
            elif '一對四' in contract_type:
                return 900
            else:
                return 0
        
        uploaded_file_sales = st.file_uploader("選擇原始 Excel 檔案", type=["xlsx"], key="sales_uploader")
        
        if uploaded_file_sales:
            df_raw = pd.read_excel(uploaded_file_sales, header=1)
            
            # 建立基礎資料
            df_base = pd.DataFrame()
            df_base["業績人員"] = df_raw["銷售人員"]
            df_base["會員姓名"] = df_raw["會員姓名"]
            df_base["開課日期"] = df_raw["交易日期"]
            df_base["合約類型"] = df_raw["票券/商品種類"]
            df_base["堂數"] = pd.to_numeric(df_raw["數量"], errors='coerce').fillna(0)
            
            total_price = pd.to_numeric(df_raw["總計(元)"], errors='coerce').fillna(0)
            df_base["合約總價"] = total_price
            df_base["金額(未稅)"] = (total_price / 1.05).round(0)
            
            df_base["購買合約原價"] = df_base["合約類型"].apply(get_unit_price) * df_base["堂數"]
            
            df_base["銷售折數"] = np.where(
                df_base["購買合約原價"] != 0,
                (df_base["金額(未稅)"] / df_base["購買合約原價"]).round(2),
                0
            )
            
            df_base["活動"] = df_raw["Tag"]
            
            cond = [
                (df_base["銷售折數"] > 0.8),
                (df_base["銷售折數"] == 0.8),
                (df_base["銷售折數"] < 0.8) & (df_base["銷售折數"] > 0)
            ]
            
            bonus_rate = np.select(cond, [0.02, 0.015, 0.01], default=0)
            
            df_base["業績計算"] = np.select(cond, ["2%", "1.5%", "1%"], default="0%")
            df_base["業績獎金"] = (df_base["金額(未稅)"] * bonus_rate).round(0)
            
            df_base["備註"] = df_raw["備註"].astype(str).replace('nan', '')
            
            # 分類
            df_new = df_base[df_base["備註"].str.contains("新購|首購")].copy()
            df_renew = df_base[df_base["備註"].str.contains("續購")].copy()
            
            # 排序
            df_new = df_new.sort_values(by="業績人員").reset_index(drop=True)
            df_renew = df_renew.sort_values(by="業績人員").reset_index(drop=True)
            
            # 預覽
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("新購預覽")
                st.dataframe(df_new, use_container_width=True)
            with col2:
                st.subheader("續購預覽")
                st.dataframe(df_renew, use_container_width=True)
            
            # 下載
            def to_excel(df_new, df_renew):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_new.to_excel(writer, index=False, sheet_name='新購')
                    df_renew.to_excel(writer, index=False, sheet_name='續購')
                return output.getvalue()
            
            if not df_new.empty or not df_renew.empty:
                excel_data = to_excel(df_new, df_renew)
                
                st.download_button(
                    label="下載轉換後的 Excel 報表",
                    data=excel_data,
                    file_name="業績產出報表.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("找不到符合條件的資料")
        else:
            st.write("請上傳檔案以開始處理。")
    
    # ===== 業務獎金計算 =====
    elif st.session_state.feature == "editor_bonus":
        st.title("業務獎金計算系統")
        
        # 計算函式
        def calculate_bonus(deal_counts, extra_classes, loyalty_counts, upgrade_counts, is_full_time, brand_count, personal_revenue_tier=None):
            """
            personal_revenue_tier 選項: None, "12萬元", "24萬元", "30萬元"
            """
            
            # 1. 個人業績獎金
            revenue_bonus_map = {
                None: 0,
                "不列入計算": 0,
                "12萬元": 2000,
                "24萬元": 4000,
                "30萬元": 6000
            }
            r_total = revenue_bonus_map.get(personal_revenue_tier, 0)
            
            # 2. 體驗成交獎金
            d_total = (deal_counts.get("當天", 0) * 80 + 
                       deal_counts.get("48小時", 0) * 60 + 
                       deal_counts.get("7天內", 0) * 50 +
                       deal_counts.get("超過7天", 0) * 0)
            
            # 3. 補位獎金
            c_total = extra_classes * 30
            
            # 4. 回流獎勵獎金 (STP-T)
            l_total = (loyalty_counts.get("10堂", 0) * 100 + 
                       loyalty_counts.get("20堂", 0) * 200 + 
                       loyalty_counts.get("30堂", 0) * 300 + 
                       loyalty_counts.get("40堂", 0) * 500)
            
            # 5. 結構升級獎金
            upgrade_prices = {"1對2變1對3": 100, "團課變期班": 150, "包班成立": 300}
            u_total = sum(upgrade_prices.get(name, 0) * count for name, count in upgrade_counts.items())
            
            # 6. 品牌知名度獎金
            base_val = 5 if is_full_time else 2
            b_note = ""
            if brand_count == 0:
                b_total = -200
                b_note = "推廣人數為 0"
            elif brand_count < base_val:
                b_total = -100
                b_note = f"未達門檻 ({base_val}位)"
            elif brand_count == base_val:
                b_total = 0
                b_note = "符合基本門檻"
            else:
                extra_units = (brand_count - base_val) // 5
                b_total = extra_units * 200
                b_note = f"加發 {extra_units} 組獎金"
            
            # 7. 月轉換高手筆數累計
            total_deals = (sum(deal_counts.values()) + 
                           sum(upgrade_counts.values()) + 
                           sum(loyalty_counts.values()) + 
                           extra_classes)
            
            if total_deals >= 50:
                monthly_bonus = 5000
            elif total_deals >= 30:
                monthly_bonus = 2000
            else:
                monthly_bonus = 0
                
            final_total = d_total + c_total + l_total + u_total + monthly_bonus + b_total + r_total
            
            return final_total, total_deals, monthly_bonus, l_total, d_total, u_total, b_total, b_note, r_total
        
        # 產生 Excel 報表
        def generate_matrix_excel(meta_data, total_v, result, deal_dict, classes, loyalty_dict, upgrade_counts, d_bonus, l_bonus, u_bonus, m_bonus, b_bonus, b_note, emp_type, b_count, r_bonus, r_tier):
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                workbook = writer.book
                worksheet = workbook.create_sheet('獎金結算', 0)
                
                bold_font = Font(bold=True, name='微軟正黑體')
                center_align = Alignment(horizontal="center", vertical="center")
                header_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
                thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                
                basic_info = [
                    ["館別", meta_data["館別"], "", "小編姓名", meta_data["小編姓名"]],
                    ["報表日期", meta_data["報表日期"], "", "員工身份", emp_type],
                    ["個人業績級別", r_tier if r_tier else "不列入計算", "", "", ""],
                    []
                ]
                for r_idx, row in enumerate(basic_info, 1):
                    for c_idx, value in enumerate(row, 1):
                        cell = worksheet.cell(row=r_idx, column=c_idx, value=value)
                        if value:
                            cell.alignment = center_align
                            if c_idx in [1, 4]:
                                cell.font = bold_font
                                cell.fill = header_fill
                            cell.border = thin_border
                
                matrix_header = ["項目", "數據/次數", "獎金金額", "備註"]
                for c_idx, text in enumerate(matrix_header, 1):
                    cell = worksheet.cell(row=6, column=c_idx, value=text)
                    cell.font = bold_font
                    cell.fill = header_fill
                    cell.alignment = center_align
                    cell.border = thin_border
                
                matrix_data = [
                    ["個人業績獎金", r_tier, r_bonus, ""],
                    ["體驗成交", sum(deal_dict.values()), d_bonus, ""],
                    ["補位獎金", classes, classes * 30, ""],
                    ["回流獎金", sum(loyalty_dict.values()), l_bonus, ""],
                    ["結構升級獎金", sum(upgrade_counts.values()), u_bonus, ""],
                    ["品牌知名度獎金", b_count, b_bonus, b_note],
                    ["月高手獎勵", total_v, m_bonus, f"總轉換筆數: {total_v}"],
                    ["總計", "", result, ""]
                ]
                
                for r_idx, row_data in enumerate(matrix_data, 7):
                    for c_idx, value in enumerate(row_data, 1):
                        cell = worksheet.cell(row=r_idx, column=c_idx, value=value)
                        cell.alignment = center_align
                        cell.border = thin_border
                        if r_idx == 7 + len(matrix_data) - 1:
                            cell.font = bold_font
                
                for i in range(1, 5):
                    worksheet.column_dimensions[get_column_letter(i)].width = 20
            
            return output.getvalue()
        
        # 側邊欄設定
        with st.sidebar:
            st.header("基本資訊設定")
            gym = st.selectbox("館別", ["巨蛋館", "其他分館"])
            name = st.text_input("小編姓名", "請輸入姓名")
            date = st.date_input("報表日期")
            is_ft = st.toggle("正職身份", value=True)
        
        # 1. 體驗與品牌推廣區塊
        st.header("1. 體驗與品牌推廣")
        
        # 個人業績選擇
        revenue_tier = st.selectbox(
            "個人業績獎金級別", 
            ["不列入計算", "12萬元", "24萬元", "30萬元"]
        )
        
        st.divider()
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            d_today = st.number_input("當天成交(筆)", min_value=0, value=0)
            d_48h = st.number_input("48小時(筆)", min_value=0, value=0)
            d_7d = st.number_input("7天內(筆)", min_value=0, value=0)
            d_over7 = st.number_input("超過7天(筆)", min_value=0, value=0)
            deal_dict = {"當天": d_today, "48小時": d_48h, "7天內": d_7d, "超過7天": d_over7}
        
        with col_b:
            brand_input = st.number_input("品牌推廣人數", min_value=0, value=5)
            extra_cls = st.number_input("補開課程次數", min_value=0, value=0)
        
        st.header("2. 回流與升級項目")
        col_c, col_d = st.columns(2)
        
        with col_c:
            st.write("回流人數 (STP-T)")
            l_10 = st.number_input("10堂人數", min_value=0, value=0)
            l_20 = st.number_input("20堂人數", min_value=0, value=0)
            l_30 = st.number_input("30堂人數", min_value=0, value=0)
            l_40 = st.number_input("40堂人數", min_value=0, value=0)
            loyalty_dict = {"10堂": l_10, "20堂": l_20, "30堂": l_30, "40堂": l_40}
        
        with col_d:
            st.write("結構升級次數")
            u_12_13 = st.number_input("1對2變1對3(次)", min_value=0, value=0)
            u_group = st.number_input("團課變期班(次)", min_value=0, value=0)
            u_class = st.number_input("包班成立(次)", min_value=0, value=0)
            upgrade_dict = {"1對2變1對3": u_12_13, "團課變期班": u_group, "包班成立": u_class}
        
        # 計算結果
        res = calculate_bonus(deal_dict, extra_cls, loyalty_dict, upgrade_dict, is_ft, brand_input, revenue_tier)
        
        st.divider()
        main_col1, main_col2 = st.columns(2)
        with main_col1:
            st.metric("當月預計總獎金", f"{res[0]} 元")
        with main_col2:
            if revenue_tier != "不列入計算":
                st.info(f"包含個人業績獎金 ({revenue_tier}): {res[8]} 元")
        
        # 匯出按鈕
        if st.button("產生並下載結算報表"):
            meta = {"館別": gym, "小編姓名": name, "報表日期": str(date)}
            excel_file = generate_matrix_excel(
                meta, res[1], res[0], deal_dict, extra_cls, loyalty_dict, upgrade_dict,
                res[4], res[3], res[5], res[2], res[6], res[7], 
                "正職" if is_ft else "兼職", brand_input, res[8], revenue_tier
            )
            st.download_button(
                label="點我儲存 Excel 檔案",
                data=excel_file,
                file_name=f"{name}_獎金結算_{date}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
