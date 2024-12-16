import tkinter as tk
from tkinter import ttk
from data_handler import fetch_stock_info
from ui_components import create_label, create_separator
import tkinter.font as tkFont

# 主視窗
window = tk.Tk()
window.title("股票分析工具")
window.geometry("1300x900")

# 輸入框區域
input_frame = tk.Frame(window)
input_frame.pack(anchor="w", padx=10, pady=10)

tk.Label(input_frame, text="請輸入股票代號:").pack(side="left", padx=5)
stock_entry = ttk.Entry(input_frame, width=20)
stock_entry.pack(side="left", padx=5)
stock_entry.focus()  # 設定游標一開始就聚焦在輸入框

# 修改查詢按鈕的命令回調函數
def fetch_and_print_stock_info(event=None):  # event=None 使此函數支援按鈕點擊及鍵盤事件
    stock_symbol = stock_entry.get()  # 獲取使用者輸入的股票代號
    print("===================================================")
    print("股票代號：", stock_symbol)
    print("===================================================")
    # 呼叫 fetch_stock_info 來顯示股票資訊
    fetch_stock_info(stock_entry, stock_info_frame, ten_punch_content)
    # 更新 left_frame_content_1 裡的字體大小
    update_font_size(stock_info_frame, size=8)

# 查詢按鈕設置
search_button = ttk.Button(input_frame, text="查詢", command=fetch_and_print_stock_info)
search_button.pack(side="left", padx=5)

# 綁定 Enter 鍵至查詢按鈕
stock_entry.bind("<Return>", fetch_and_print_stock_info)

# 下方區域框架，包含所有子區塊
main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# 左側區塊，劃分為三個並排的子區塊
horizontal_frame = tk.Frame(main_frame)
horizontal_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

# 基本資訊 1
left_frame_1 = tk.LabelFrame(horizontal_frame, text="基本資料")
left_frame_1.pack(side="left", fill="both", expand=True, padx=5, pady=5)
left_canvas_1 = tk.Canvas(left_frame_1)
left_scrollbar_1_y = ttk.Scrollbar(left_frame_1, orient="vertical", command=left_canvas_1.yview)
left_scrollbar_1_y.pack(side="right", fill="y")
left_scrollbar1_x = ttk.Scrollbar(left_frame_1, orient="horizontal", command=left_canvas_1.xview)
left_scrollbar1_x.pack(side="bottom", fill="x")
left_canvas_1.pack(side="left", fill="both", expand=True)
left_canvas_1.config(yscrollcommand=left_scrollbar_1_y.set, xscrollcommand=left_scrollbar1_x.set)

# 在 Canvas 裡創建一個 Frame 用來放置內容
stock_info_frame = tk.Frame(left_canvas_1)
left_canvas_1.create_window((0, 0), window=stock_info_frame, anchor="nw")

# 更新 Frame 大小
def on_left_frame_1_configure(event):
    left_canvas_1.config(scrollregion=left_canvas_1.bbox("all"))

stock_info_frame.bind("<Configure>", on_left_frame_1_configure)

# # 基本資訊 2
# left_frame_2 = tk.LabelFrame(horizontal_frame, text="財務資訊")
# left_frame_2.pack(side="left", fill="both", expand=True, padx=5, pady=5)
# left_canvas_2 = tk.Canvas(left_frame_2)
# left_scrollbar_2 = ttk.Scrollbar(left_frame_2, orient="vertical", command=left_canvas_2.yview)
# left_scrollbar_2.pack(side="right", fill="y")
# left_canvas_2.pack(side="left", fill="both", expand=True)
# left_canvas_2.config(yscrollcommand=left_scrollbar_2.set)

# # 在 Canvas 裡創建一個 Frame 用來放置內容
# left_frame_content_2 = tk.Frame(left_canvas_2)
# left_canvas_2.create_window((0, 0), window=left_frame_content_2, anchor="nw")

# # 更新 Frame 大小
# def on_left_frame_2_configure(event):
#     left_canvas_2.config(scrollregion=left_canvas_2.bbox("all"))

# left_frame_content_2.bind("<Configure>", on_left_frame_2_configure)

# 十全劍
left_frame_3 = tk.LabelFrame(horizontal_frame, text="十全劍")
left_frame_3.pack(side="left", fill="both", expand=True, padx=5, pady=5)
left_canvas_3 = tk.Canvas(left_frame_3)
left_scrollbar_3 = ttk.Scrollbar(left_frame_3, orient="vertical", command=left_canvas_3.yview)
left_scrollbar_3.pack(side="right", fill="y")
left_canvas_3.pack(side="left", fill="both", expand=True)
left_canvas_3.config(yscrollcommand=left_scrollbar_3.set)

# 在 Canvas 裡創建一個 Frame 用來放置內容
ten_punch_content = tk.Frame(left_canvas_3)
left_canvas_3.create_window((0, 0), window=ten_punch_content, anchor="nw")

# 更新 Frame 大小
def on_left_frame_3_configure(event):
    left_canvas_3.config(scrollregion=left_canvas_3.bbox("all"))

ten_punch_content.bind("<Configure>", on_left_frame_3_configure)

# # 中間區塊：財務數據
# center_frame = tk.LabelFrame(main_frame, text="現金流量表", width=300)
# center_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
# center_canvas = tk.Canvas(center_frame)
# center_scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=center_canvas.yview)
# center_scrollbar.pack(side="right", fill="y")
# center_canvas.pack(side="left", fill="both", expand=True)
# center_canvas.config(yscrollcommand=center_scrollbar.set)

# # 在 Canvas 裡創建一個 Frame 用來放置內容
# center_frame_content = tk.Frame(center_canvas)
# center_canvas.create_window((0, 0), window=center_frame_content, anchor="nw")

# # 更新 Frame 大小
# def on_center_frame_configure(event):
#     center_canvas.config(scrollregion=center_canvas.bbox("all"))

# center_frame_content.bind("<Configure>", on_center_frame_configure)

# # 資產負債表
# right_frame = tk.LabelFrame(main_frame, text="資產負債表", width=300)
# right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
# right_canvas = tk.Canvas(right_frame)
# right_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
# right_scrollbar.pack(side="right", fill="y")
# right_canvas.pack(side="left", fill="both", expand=True)
# right_canvas.config(yscrollcommand=right_scrollbar.set)

# # 在 Canvas 裡創建一個 Frame 用來放置內容
# balance_sheet_content = tk.Frame(right_canvas)
# right_canvas.create_window((0, 0), window=balance_sheet_content, anchor="nw")

# # 更新 Frame 大小
# def on_right_frame_configure(event):
#     right_canvas.config(scrollregion=right_canvas.bbox("all"))

# balance_sheet_content.bind("<Configure>", on_right_frame_configure)

# 更新指定 Frame 裡所有 Label 的字體大小
def update_font_size(frame, size=8):
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label):
            font = tkFont.Font(widget, widget.cget("font"))
            font.configure(size=size)
            widget.config(font=font)

# 主循環
window.mainloop()