import pandas as pd
import numpy as np

import yfinance as yf
import tkinter as tk
from tkinter import ttk

def format_number(value):
    """格式化數字為可讀形式"""
    try:
        value = float(value)
        if value >= 1e12:
            return f"{value / 1e12:.3f}T"
        elif value >= 1e9:
            return f"{value / 1e9:.3f}B"
        elif value >= 1e6:
            return f"{value / 1e6:.3f}M"
        return f"{value:.2f}"
    except:
        return value

def fetch_stock_info():
    """獲取並顯示股票基本資訊和財務數據"""
    stock_symbol = stock_entry.get()
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.info  # 獲取股票基本資訊

    # 清空區塊 1 和區塊 2 的內容
    for widget in left_frame.winfo_children():
        widget.destroy()
    for widget in center_frame.winfo_children():
        widget.destroy()

    # 區塊 1：基本資訊
    basic_info_fields = [
        "marketCap",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
        "fiftyDayAverage",
        "trailingEps",
        "forwardEps",
        "trailingPE",
        "forwardPE",
        "trailingPegRatio",
    ]
    tk.Label(left_frame, text="基本資訊", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
    for idx, field in enumerate(basic_info_fields, start=1):
        value = stock_info.get(field, "N/A")  # 如果字段不存在，顯示 "N/A"
        formatted_value = format_number(value)  # 格式化數字
        tk.Label(left_frame, text=f"{field}:", anchor="w").grid(row=idx, column=0, sticky="w", padx=5)
        tk.Label(left_frame, text=formatted_value, anchor="e").grid(row=idx, column=1, sticky="w", padx=5)

    # 區塊 2：財務數據
    financial_fields = [
        "marketCap",
        "enterpriseValue",
        "profitMargins",
        "grossMargins",
        "operatingMargins",
        "debtToEquity",
        "returnOnAssets",
        "returnOnEquity",
        "revenueGrowth",
        "earningsGrowth",
        "totalDebt",
        "sharesOutstanding",
        "operatingCashflow",
        "freeCashflow",
    ]
    tk.Label(center_frame, text="財務數據", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
    for idx, field in enumerate(financial_fields, start=1):
        value = stock_info.get(field, "N/A")  # 如果字段不存在，顯示 "N/A"
        formatted_value = format_number(value)  # 格式化數字
        tk.Label(center_frame, text=f"{field}:", anchor="w").grid(row=idx, column=0, sticky="w", padx=5)
        tk.Label(center_frame, text=formatted_value, anchor="e").grid(row=idx, column=1, sticky="w", padx=5)

# 主視窗
window = tk.Tk()
window.title("股票分析工具")
window.geometry("1200x800")

# 輸入框區域
input_frame = tk.Frame(window)
input_frame.pack(anchor="w", padx=10, pady=10)

tk.Label(input_frame, text="請輸入股票代號:").pack(side="left", padx=5)
stock_entry = ttk.Entry(input_frame, width=20)
stock_entry.pack(side="left", padx=5)
search_button = ttk.Button(input_frame, text="查詢", command=fetch_stock_info)
search_button.pack(side="left", padx=5)

# 下方區域框架
main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# 區塊 1：基本資訊
left_frame = tk.LabelFrame(main_frame, text="基本資訊", width=300)
left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# 區塊 2：財務數據
center_frame = tk.LabelFrame(main_frame, text="財務數據", width=300)
center_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# 區塊 3：十全劍
right_frame = tk.LabelFrame(main_frame, text="十全劍", width=300)
right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
tk.Label(right_frame, text="這裡可以填充十全劍的自定義內容", anchor="w", justify="left").pack(fill="both", padx=5, pady=5)

# 主循環
window.mainloop()


# # 格式化數值
# def format_number(value):
#     try:
#         if value is None:
#             return "N/A"
#         if isinstance(value, (list, np.ndarray)):  # 如果是數組或列表類型，直接返回原始值的字符串表示
#             return ", ".join(map(str, value))
#         if pd.isna(value):  # 處理單一 NaN
#             return "N/A"
#         value = float(value)  # 確保值是數字
#         if value >= 1e12 or value <= -1e12:
#             return f"{value / 1e12:.3f}T"
#         elif value >= 1e9 or value <= -1e9:
#             return f"{value / 1e9:.3f}B"
#         elif value >= 1e6 or value <= -1e6:
#             return f"{value / 1e6:.3f}M"
#         return f"{value:.2f}"
#     except (ValueError, TypeError):  # 如果值不是數字或 NaN，直接返回字符串表示
#         return str(value)

# # 獲取股票季度財務數據
# def get_financials(stock_symbol):
#     stock = yf.Ticker(stock_symbol)
#     quarterly_financials = stock.quarterly_financials

#     if not quarterly_financials.empty:
#         required_fields = ["Net Income", "Operating Income", "Total Revenue"]
#         filtered_data = quarterly_financials.loc[quarterly_financials.index.isin(required_fields)]
#         filtered_data_top5 = filtered_data.iloc[:, :5]

#         # 計算差值及百分比變化
#         differences = pd.DataFrame(index=filtered_data_top5.index, columns=filtered_data_top5.columns)
#         percentage_changes = pd.DataFrame(index=filtered_data_top5.index, columns=filtered_data_top5.columns)

#         for col_idx in range(len(filtered_data_top5.columns) - 1):  # 不處理最後一列
#             current_col = filtered_data_top5.iloc[:, col_idx]
#             next_col = filtered_data_top5.iloc[:, col_idx + 1]
#             differences.iloc[:, col_idx] = current_col - next_col
#             percentage_changes.iloc[:, col_idx] = ((current_col - next_col) / current_col) * 100

#         # 格式化數據
#         formatted_data = filtered_data_top5.copy()
#         for row_idx in range(len(formatted_data)):
#             for col_idx in range(len(formatted_data.columns)):
#                 current_value = filtered_data_top5.iloc[row_idx, col_idx]
#                 if col_idx < len(formatted_data.columns) - 1:  # 不處理最後一列
#                     diff_value = differences.iloc[row_idx, col_idx]
#                     diff_rate = percentage_changes.iloc[row_idx, col_idx]
#                     if not pd.isna(diff_value) and not pd.isna(diff_rate):
#                         formatted_data.iloc[row_idx, col_idx] = f"{format_number(current_value)} ({format_number(diff_value)}, {diff_rate:+.2f}%)"
#                     else:
#                         formatted_data.iloc[row_idx, col_idx] = f"{format_number(current_value)}"
#                 else:
#                     formatted_data.iloc[row_idx, col_idx] = format_number(current_value)
#         return formatted_data
#     else:
#         return None

# # 獲取股票基本資訊
# def get_stock_info(stock_symbol):
#     stock = yf.Ticker(stock_symbol)
#     return stock.info

# # 建立介面
# def display_interface():
#     def fetch_data():
#         stock_symbol = stock_entry.get()

#         # 獲取財務數據
#         financial_data = get_financials(stock_symbol)
#         for widget in financial_canvas.winfo_children():
#             widget.destroy()  # 清空財務結果顯示區域
#         if financial_data is not None:
#             columns = list(financial_data.columns)
#             rows = list(financial_data.index)

#             # 顯示財務數據表格
#             for col_idx, col_name in enumerate([""] + columns):
#                 label = tk.Label(financial_canvas, text=col_name, borderwidth=1, relief="solid")
#                 label.grid(row=0, column=col_idx, sticky="nsew")

#             for row_idx, row_name in enumerate(rows):
#                 label = tk.Label(financial_canvas, text=row_name, borderwidth=1, relief="solid")
#                 label.grid(row=row_idx + 1, column=0, sticky="nsew")

#                 for col_idx, col_name in enumerate(columns):
#                     value = financial_data.iloc[row_idx, col_idx]
#                     label = tk.Label(financial_canvas, text=value, borderwidth=1, relief="solid")
#                     label.grid(row=row_idx + 1, column=col_idx + 1, sticky="nsew")
#         else:
#             tk.Label(financial_canvas, text="無法獲取財務數據", fg="red").pack()

#         # 獲取股票基本資訊
#         stock_info = get_stock_info(stock_symbol)
#         for widget in info_canvas.winfo_children():
#             widget.destroy()  # 清空基本資訊顯示區域
#         if stock_info:
#             for key, value in stock_info.items():
#                 formatted_value = format_number(value)
#                 tk.Label(info_canvas, text=f"{key}: {formatted_value}", anchor="w", justify="left", wraplength=400).pack(fill="x")
#         else:
#             tk.Label(info_canvas, text="無法獲取基本資訊", fg="red").pack()

#     # 主視窗
#     window = tk.Tk()
#     window.title("股票數據分析")
#     window.geometry("1200x800")

#     # 股票代號輸入框
#     input_frame = tk.Frame(window)
#     input_frame.pack(pady=10)

#     tk.Label(input_frame, text="請輸入股票代號:").pack(side="left")
#     stock_entry = tk.Entry(input_frame, width=20)
#     stock_entry.pack(side="left", padx=5)
#     tk.Button(input_frame, text="查詢", command=fetch_data).pack(side="left")

#     # 左右佈局框架
#     main_frame = tk.Frame(window)
#     main_frame.pack(fill="both", expand=True, padx=10, pady=10)

#     # 股票基本資訊顯示區域 (左側)
#     info_frame = tk.Frame(main_frame, width=600)
#     info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

#     info_scrollbar = tk.Scrollbar(info_frame)
#     info_scrollbar.pack(side="right", fill="y")

#     info_canvas = tk.Canvas(info_frame, yscrollcommand=info_scrollbar.set)
#     info_canvas.pack(side="left", fill="both", expand=True)

#     info_scrollbar.config(command=info_canvas.yview)

#     info_inner_frame = tk.Frame(info_canvas)
#     info_canvas.create_window((0, 0), window=info_inner_frame, anchor="nw")
#     info_inner_frame.bind("<Configure>", lambda e: info_canvas.config(scrollregion=info_canvas.bbox("all")))

#     # 財務數據顯示區域 (右側)
#     financial_frame = tk.Frame(main_frame, width=600)
#     financial_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

#     financial_scrollbar = tk.Scrollbar(financial_frame)
#     financial_scrollbar.pack(side="right", fill="y")

#     financial_canvas = tk.Canvas(financial_frame, yscrollcommand=financial_scrollbar.set)
#     financial_canvas.pack(side="left", fill="both", expand=True)

#     financial_scrollbar.config(command=financial_canvas.yview)

#     financial_inner_frame = tk.Frame(financial_canvas)
#     financial_canvas.create_window((0, 0), window=financial_inner_frame, anchor="nw")
#     financial_inner_frame.bind("<Configure>", lambda e: financial_canvas.config(scrollregion=financial_canvas.bbox("all")))

#     # 啟動主循環
#     window.mainloop()

# # 執行介面
# if __name__ == "__main__":
#     display_interface()