import streamlit as st
import pandas as pd
import io
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import numpy as np

# ========================
# 頁面設定
# ========================
st.set_page_config(page_title="春不老薪資計算系統", layout="wide")

# ========================
# Session State 初始化
# ========================
if "role" not in st.session_state:
    st.session_state.role = None
if "feature" not in st.session_state:
    st.session_state.feature = None
if "show_finance_login" not in st.session_state:
    st.session_state.show_finance_login = False

# ========================
# 步驟 1: 身份選擇
# ========================
if st.session_state.role is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>春不老薪資計算系統</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #999;'>請選擇您的角色登入系統</p>", unsafe_allow_html=True)
        
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
        col_btn3, col_btn4 = st.columns(2)
        with col_btn3:
            if st.button("美編登入", key="designer_btn", use_container_width=True):
                st.session_state.role = "designer"
                st.rerun()

        with col_btn4:
            if st.button("財務登入", key="finance_btn", use_container_width=True):
                st.session_state.show_finance_login = True

        # 財務密碼驗證區塊
        if st.session_state.get("show_finance_login", False):
            st.markdown("<br>", unsafe_allow_html=True)
            password = st.text_input(
                "請輸入財務密碼",
                type="password",
                key="finance_password_input"
            )
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("確認", key="finance_confirm_btn", use_container_width=True):
                    if password == "20260512":
                        st.session_state.role = "finance"
                        st.session_state.show_finance_login = False
                        st.rerun()
                    else:
                        st.error("密碼錯誤，請重試")
            with col_cancel:
                if st.button("取消", key="finance_cancel_btn", use_container_width=True):
                    st.session_state.show_finance_login = False
                    st.rerun()

# ========================
# 步驟 2: 功能選擇
# ========================
elif st.session_state.feature is None:
    col_back, col_title = st.columns([1, 10])
    with col_back:
        if st.button("返回"):
            st.session_state.role = None
            st.session_state.feature = None
            st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.role == "manager":
            st.markdown("<h1 style='text-align: center;'>店長功能選擇</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #999;'>請選擇您要使用的功能</p>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 使用三欄位佈局
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                if st.button("教練堂數統計", key="lesson_report", use_container_width=True):
                    st.session_state.feature = "lesson_report"
                    st.rerun()
            
            with col_f2:
                if st.button("團個績計算工具", key="sales_report", use_container_width=True):
                    st.session_state.feature = "sales_report"
                    st.rerun()
            
            with col_f3:
                if st.button("出勤明細統計", key="attendance_report", use_container_width=True):
                    st.session_state.feature = "attendance_report"
                    st.rerun()
        
        else:  # editor
            st.markdown("<h1 style='text-align: center;'>小編功能選擇</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #999;'>請選擇您要使用的功能</p>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("業務獎金計算", key="editor_bonus", use_container_width=True):
                st.session_state.feature = "editor_bonus"
                st.rerun()

# ========================
# 步驟 3: 顯示功能
# ========================
else:
    col_back, col_title, col_empty = st.columns([1, 10, 1])
    with col_back:
        if st.button("返回"):
            st.session_state.feature = None
            st.rerun()
    
    # ===== 預約報表統計 =====
    if st.session_state.feature == "lesson_report":
        st.title("教練堂數統計")
        st.markdown("請上傳原始團體課預約報表，系統將自動提取並整理為指定格式。")
        
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
                
                df_stats['小計'] = df_stats.sum(axis=1)
                
                # 排序
                df_stats['sort_key'] = df_stats.index.map(teacher_sort_key)
                df_stats = df_stats.sort_values('sort_key').drop(columns=['sort_key'])
                
                # 合計列
                total_row = df_stats.sum().to_frame().T
                total_row.index = ['合計']
                df_final = pd.concat([df_stats, total_row])
                
                # 轉置
                df_transposed = df_final.T
                
                st.markdown("### 3. 統計結果預覽")
                st.dataframe(df_transposed, use_container_width=True)
                
                # 匯出 Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_transposed.to_excel(writer, sheet_name='堂數統計')
                
                st.download_button(
                    label="下載統計報表 (Excel)",
                    data=output.getvalue(),
                    file_name=f"堂數統計_{selected_branch}_{start_date}_{end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            except Exception as e:
                st.error(f"處理過程中發生錯誤: {e}")

    # ===== 業績報表自動化轉換工具 =====
    elif st.session_state.feature == "sales_report":
        st.title("業績報表自動化轉換工具")
        st.markdown("請上傳原始交易報表，系統將自動提取並整理為指定格式。")
        
        uploaded_file = st.file_uploader("選擇原始 Excel 檔案", type=["xlsx"], key="sales_uploader")
        
        if uploaded_file is not None:
            try:
                df_raw = pd.read_excel(uploaded_file, header=1)
                
                # 建立基礎資料
                df_base = pd.DataFrame()
                df_base["合約建立日期"] = df_raw["交易日期"]
                df_base["業績人員"] = df_raw["銷售人員"]
                df_base["會員姓名"] = df_raw["會員姓名"]
                df_base["開課日期"] = np.nan
                df_base["合約類型"] = df_raw["票券/商品種類"]
                df_base["堂數"] = pd.to_numeric(df_raw["數量"], errors='coerce').fillna(0)
                
                total_price = pd.to_numeric(df_raw["總計(元)"], errors='coerce').fillna(0)
                df_base["合約總價"] = total_price
                df_base["金額(未稅)"] = (total_price / 1.05).round(0)
                
                def get_unit_price(contract_type):
                    contract_type = str(contract_type)
                    if '一對一' in contract_type: return 2300
                    elif '一對二' in contract_type: return 1300
                    elif '一對三' in contract_type: return 1050
                    elif '一對四' in contract_type: return 900
                    else: return 0
                
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
                
                target_columns = [
                    "合約建立日期", "業績人員", "會員姓名", "開課日期", "合約類型", 
                    "堂數", "合約總價", "金額(未稅)", "銷售折數", "活動", 
                    "業績計算", "業績獎金", "購買合約原價", "備註"
                ]
                df_base = df_base[target_columns]
                
                df_new = df_base[df_base["備註"].str.contains("新購|首購")].copy()
                df_renew = df_base[df_base["備註"].str.contains("續購")].copy()
                
                df_new = df_new.sort_values(by="業績人員").reset_index(drop=True)
                df_renew = df_renew.sort_values(by="業績人員").reset_index(drop=True)
                
                st.markdown("### 新購/首購 預覽")
                st.dataframe(df_new, use_container_width=True)
                
                st.markdown("### 續購 預覽")
                st.dataframe(df_renew, use_container_width=True)
                
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_new.to_excel(writer, sheet_name='新購首購', index=False)
                    df_renew.to_excel(writer, sheet_name='續購', index=False)
                
                st.download_button(
                    label="下載轉換後報表 (Excel)",
                    data=output.getvalue(),
                    file_name=f"業績報表轉換_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            except Exception as e:
                st.error(f"處理過程中發生錯誤: {e}")

    # ===== 出勤明細統計 (新功能) =====
    elif st.session_state.feature == "attendance_report":
        st.title("出勤明細統計")
        st.markdown("上傳原始 Excel 進出場記錄，系統將自動生成統計報表。")
        
        uploaded_file = st.file_uploader("選擇原始 Excel 進出場記錄檔案", type=["xlsx"], key="attendance_uploader")
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                
                # 資料清洗
                df['進場日期'] = pd.to_datetime(df['進場日期'], errors='coerce').dt.date
                df['出場日期'] = pd.to_datetime(df['出場日期'], errors='coerce').dt.date
                df['總時間(分)'] = pd.to_numeric(df['總時間(分)'], errors='coerce')
                
                # 統計
                summary = (
                    df.groupby('姓名')
                    .agg(
                        出勤天數=('進場日期', 'nunique'),
                        總時數_分=('總時間(分)', 'sum'),
                    )
                    .reset_index()
                    .sort_values('姓名')
                )
                
                def minutes_to_hhmm(minutes):
                    if pd.isna(minutes): return ""
                    h, m = divmod(int(minutes), 60)
                    return f"{h}:{m:02d}"
                
                summary['總工時(時:分)'] = summary['總時數_分'].apply(minutes_to_hhmm)
                
                st.markdown("### 出勤統計預覽")
                st.dataframe(summary[['姓名', '出勤天數', '總時數_分', '總工時(時:分)']], use_container_width=True)
                
                # 報表生成邏輯 (整合 abcde 專案邏輯)
                if st.button("產生完整報表並下載"):
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        # Sheet 1: 出勤明細
                        df_sorted = df.sort_values(['姓名', '進場日期', '進場時間']).reset_index(drop=True)
                        df_sorted['總工時(時:分)'] = df_sorted['總時間(分)'].apply(minutes_to_hhmm)
                        df_sorted.to_excel(writer, sheet_name='出勤明細', index=False)
                        
                        # Sheet 2: 月份出勤統計
                        summary.to_excel(writer, sheet_name='月份出勤統計', index=False)
                        
                        # Sheet 3: 月曆排班表
                        df2 = df.copy()
                        df2['日期'] = df2['進場日期'].astype(str).str[:10]
                        pivot = df2.pivot_table(
                            index='姓名', columns='日期', values='總時間(分)', aggfunc='sum'
                        ).fillna(0)
                        pivot.to_excel(writer, sheet_name='月曆排班表')
                        
                    st.download_button(
                        label="點我儲存 Excel 檔案",
                        data=output.getvalue(),
                        file_name=f"出勤明細統計_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"處理過程中發生錯誤: {e}")

    # ===== 業務獎金計算系統 =====
    elif st.session_state.feature == "editor_bonus":
        st.title("業務獎金計算系統")
        
        def calculate_bonus(deal_dict, classes, loyalty_dict, upgrade_counts, is_ft, brand_count, revenue_tier):
            # 1. 體驗成交獎金
            d_bonus = (deal_dict["當天"] * 80 + deal_dict["48小時"] * 60 + 
                      deal_dict["7天內"] * 50 + deal_dict["超過7天"] * 0)
            
            # 2. 補位獎金
            c_bonus = classes * 30
            
            # 3. 回流獎金
            l_bonus = (loyalty_dict["10堂"] * 100 + loyalty_dict["20堂"] * 200 + 
                      loyalty_dict["30堂"] * 300 + loyalty_dict["40堂"] * 500)
            
            # 4. 結構升級獎金
            u_bonus = (upgrade_counts["1對2變1對3"] * 100 + 
                      upgrade_counts["團課變期班"] * 150 + 
                      upgrade_counts["包班成立"] * 300)
            
            # 5. 品牌知名度獎金
            base_val = 5 if is_ft else 2
            if brand_count == 0:
                b_bonus = -200
                b_note = "推廣人數為 0"
            elif brand_count < base_val:
                b_bonus = -100
                b_note = f"未達門檻 ({base_val}位)"
            elif brand_count == base_val:
                b_bonus = 0
                b_note = "符合基本門檻"
            else:
                extra_units = (brand_count - base_val) // 5
                b_bonus = extra_units * 200
                b_note = f"加發 {extra_units} 組獎金"
            
            # 6. 月高手獎勵
            total_v = sum(deal_dict.values()) + classes + sum(loyalty_dict.values()) + sum(upgrade_counts.values())
            if total_v >= 50: m_bonus = 5000
            elif total_v >= 30: m_bonus = 2000
            else: m_bonus = 0
            
            # 7. 個人業績獎金
            rev_map = {"不列入計算": 0, "12萬元": 2000, "24萬元": 4000, "30萬元": 6000}
            r_bonus = rev_map.get(revenue_tier, 0)
            
            total = d_bonus + c_bonus + l_bonus + u_bonus + b_bonus + m_bonus + r_bonus
            return total, total_v, m_bonus, l_bonus, d_bonus, u_bonus, b_bonus, b_note, r_bonus

        def generate_matrix_excel(meta_data, total_v, result, deal_dict, classes, loyalty_dict, upgrade_counts, d_bonus, l_bonus, u_bonus, m_bonus, b_bonus, b_note, emp_type, b_count, r_bonus, r_tier):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                workbook = writer.book
                worksheet = workbook.create_sheet('獎金結算', 0)
                bold_font = Font(bold=True, name='微軟正黑體')
                center_align = Alignment(horizontal="center", vertical="center")
                thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                
                info = [
                    ["館別", meta_data["館別"]],
                    ["報表日期", meta_data["報表日期"]],
                    ["小編姓名", meta_data["小編姓名"]],
                    ["員工身份", emp_type]
                ]
                for i, (k, v) in enumerate(info, 1):
                    worksheet.cell(row=i, column=1, value=k).font = bold_font
                    worksheet.cell(row=i, column=2, value=v)
                
                header_row = 7
                headers = ["項目", "筆數", "獎金金額", "備註"]
                for i, h in enumerate(headers, 1):
                    worksheet.cell(row=header_row, column=i, value=h).font = bold_font
                
                data_rows = [
                    ["個人業績獎金", r_tier if r_tier else "不列入計算", r_bonus, ""],
                    ["體驗成交", sum(deal_dict.values()), d_bonus, ""],
                    ["補位獎金", classes, classes * 30, ""],
                    ["回流獎金", sum(loyalty_dict.values()), l_bonus, ""],
                    ["結構升級獎金", sum(upgrade_counts.values()), u_bonus, ""],
                    ["品牌知名度獎金", b_count, b_bonus, b_note],
                    ["月高手獎勵", total_v, m_bonus, f"總轉換筆數: {total_v}"],
                    ["總計", "", result, ""]
                ]
                for r_idx, row_data in enumerate(data_rows, header_row + 1):
                    for c_idx, value in enumerate(row_data, 1):
                        cell = worksheet.cell(row=r_idx, column=c_idx, value=value)
                        cell.alignment = center_align
                        cell.border = thin_border
                        if r_idx == header_row + len(data_rows): cell.font = bold_font
                
                worksheet.column_dimensions['A'].width = 15
                worksheet.column_dimensions['B'].width = 15
                worksheet.column_dimensions['C'].width = 15
                worksheet.column_dimensions['D'].width = 20
            return output.getvalue()
        
        st.markdown("### 基本資訊設定")
        col1, col2, col3, col4 = st.columns(4)
        with col1: gym = st.selectbox("館別", ["義昌館", "高美館", "中山館", "巨蛋館"], key="gym_select")
        with col2: name = st.text_input("小編姓名", "", placeholder="請輸入姓名", key="name_input")
        with col3:
            date_range = st.date_input("報表日期", value=None, key="date_input")
            date_str = str(date_range) if date_range else ""
        with col4: is_ft = st.selectbox("員工身份", ["正職", "兼職"], key="employment_select") == "正職"
        
        st.divider()
        st.markdown("### 1. 體驗與品牌推廣")
        revenue_tier = st.selectbox("個人業績獎金級別", ["不列入計算", "12萬元", "24萬元", "30萬元"], key="revenue_tier_select")
        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            d_today = st.number_input("當天成交(筆)", min_value=0, value=0, key="deal_today")
            d_48h = st.number_input("48小時(筆)", min_value=0, value=0, key="deal_48h")
            d_7d = st.number_input("7天內(筆)", min_value=0, value=0, key="deal_7d")
            d_over7 = st.number_input("超過7天(筆)", min_value=0, value=0, key="deal_over7")
            deal_dict = {"當天": d_today, "48小時": d_48h, "7天內": d_7d, "超過7天": d_over7}
        with col_b:
            brand_input = st.number_input("品牌推廣人數", min_value=0, value=0, key="brand_input")
            extra_cls = st.number_input("補開課程次數", min_value=0, value=0, key="extra_cls")
        
        st.markdown("### 2. 回流與升級項目")
        col_c, col_d = st.columns(2)
        with col_c:
            st.write("回流人數 (STP-T)")
            l_10 = st.number_input("10堂人數", min_value=0, value=0, key="loyalty_10")
            l_20 = st.number_input("20堂人數", min_value=0, value=0, key="loyalty_20")
            l_30 = st.number_input("30堂人數", min_value=0, value=0, key="loyalty_30")
            l_40 = st.number_input("40堂人數", min_value=0, value=0, key="loyalty_40")
            loyalty_dict = {"10堂": l_10, "20堂": l_20, "30堂": l_30, "40堂": l_40}
        with col_d:
            st.write("結構升級次數")
            u_12_13 = st.number_input("1對2變1對3(次)", min_value=0, value=0, key="upgrade_1213")
            u_group = st.number_input("團課變期班(次)", min_value=0, value=0, key="upgrade_group")
            u_class = st.number_input("包班成立(次)", min_value=0, value=0, key="upgrade_class")
            upgrade_dict = {"1對2變1對3": u_12_13, "團課變期班": u_group, "包班成立": u_class}
        
        res = calculate_bonus(deal_dict, extra_cls, loyalty_dict, upgrade_dict, is_ft, brand_input, revenue_tier)
        st.divider()
        main_col1, main_col2 = st.columns(2)
        with main_col1: st.metric("當月預計總獎金", f"{res[0]} 元")
        with main_col2:
            if revenue_tier != "不列入計算": st.info(f"包含個人業績獎金 ({revenue_tier}): {res[8]} 元")
        
        if st.button("產生並下載結算報表"):
            if not name or name.strip() == "": st.error("請輸入小編姓名")
            else:
                meta = {"館別": gym, "小編姓名": name, "報表日期": date_str}
                excel_file = generate_matrix_excel(
                    meta, res[1], res[0], deal_dict, extra_cls, loyalty_dict, upgrade_dict,
                    res[4], res[3], res[5], res[2], res[6], res[7], 
                    "正職" if is_ft else "兼職", brand_input, res[8], revenue_tier
                )
                st.download_button(
                    label="點我儲存 Excel 檔案",
                    data=excel_file,
                    file_name=f"{name}_獎金結算_{date_str}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
