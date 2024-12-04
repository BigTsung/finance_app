import tkinter as tk
from tkinter import ttk
from data_handler import fetch_stock_info
from ui_components import create_label, create_separator

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
search_button = ttk.Button(input_frame, text="查詢", command=lambda: fetch_stock_info(stock_entry, left_frame_content_1, left_frame_content_2, left_frame_content_3, center_frame_content, right_frame_content))
search_button.pack(side="left", padx=5)

# 下方區域框架，包含所有子區塊
main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# 左側區塊，劃分成三等分
left_main_frame = tk.Frame(main_frame)
left_main_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# 基本資訊 1
left_frame_1 = tk.LabelFrame(left_main_frame, text="基本資料")
left_frame_1.pack(fill="both", expand=True)
left_canvas_1 = tk.Canvas(left_frame_1)
left_scrollbar_1_y = ttk.Scrollbar(left_frame_1, orient="vertical", command=left_canvas_1.yview)
left_scrollbar_1_y.pack(side="right", fill="y")
left_scrollbar1_x = ttk.Scrollbar(left_frame_1, orient="horizontal", command=left_canvas_1.xview)
left_scrollbar1_x.pack(side="bottom", fill="x")
left_canvas_1.pack(side="left", fill="both", expand=True)
left_canvas_1.config(yscrollcommand=left_scrollbar_1_y.set, xscrollcommand=left_scrollbar1_x.set)

# 在 Canvas 裡創建一個 Frame 用來放置內容
left_frame_content_1 = tk.Frame(left_canvas_1)
left_canvas_1.create_window((0, 0), window=left_frame_content_1, anchor="nw")

# 更新 Frame 大小
def on_left_frame_1_configure(event):
    left_canvas_1.config(scrollregion=left_canvas_1.bbox("all"))

left_frame_content_1.bind("<Configure>", on_left_frame_1_configure)

# 基本資訊 2
left_frame_2 = tk.LabelFrame(left_main_frame, text="財務資訊")
left_frame_2.pack(fill="both", expand=True)
left_canvas_2 = tk.Canvas(left_frame_2)
left_scrollbar_2 = ttk.Scrollbar(left_frame_2, orient="vertical", command=left_canvas_2.yview)
left_scrollbar_2.pack(side="right", fill="y")
left_canvas_2.pack(side="left", fill="both", expand=True)
left_canvas_2.config(yscrollcommand=left_scrollbar_2.set)

# 在 Canvas 裡創建一個 Frame 用來放置內容
left_frame_content_2 = tk.Frame(left_canvas_2)
left_canvas_2.create_window((0, 0), window=left_frame_content_2, anchor="nw")

# 更新 Frame 大小
def on_left_frame_2_configure(event):
    left_canvas_2.config(scrollregion=left_canvas_2.bbox("all"))

left_frame_content_2.bind("<Configure>", on_left_frame_2_configure)

# 基本資訊 3
left_frame_3 = tk.LabelFrame(left_main_frame, text="Coming Soon")
left_frame_3.pack(fill="both", expand=True)
left_canvas_3 = tk.Canvas(left_frame_3)
left_scrollbar_3 = ttk.Scrollbar(left_frame_3, orient="vertical", command=left_canvas_3.yview)
left_scrollbar_3.pack(side="right", fill="y")
left_canvas_3.pack(side="left", fill="both", expand=True)
left_canvas_3.config(yscrollcommand=left_scrollbar_3.set)

# 在 Canvas 裡創建一個 Frame 用來放置內容
left_frame_content_3 = tk.Frame(left_canvas_3)
left_canvas_3.create_window((0, 0), window=left_frame_content_3, anchor="nw")

# 更新 Frame 大小
def on_left_frame_3_configure(event):
    left_canvas_3.config(scrollregion=left_canvas_3.bbox("all"))

left_frame_content_3.bind("<Configure>", on_left_frame_3_configure)

# 中間區塊：財務數據
center_frame = tk.LabelFrame(main_frame, text="財務數據", width=300)
center_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
center_canvas = tk.Canvas(center_frame)
center_scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=center_canvas.yview)
center_scrollbar.pack(side="right", fill="y")
center_canvas.pack(side="left", fill="both", expand=True)
center_canvas.config(yscrollcommand=center_scrollbar.set)

# 在 Canvas 裡創建一個 Frame 用來放置內容
center_frame_content = tk.Frame(center_canvas)
center_canvas.create_window((0, 0), window=center_frame_content, anchor="nw")

# 更新 Frame 大小
def on_center_frame_configure(event):
    center_canvas.config(scrollregion=center_canvas.bbox("all"))

center_frame_content.bind("<Configure>", on_center_frame_configure)

# 右側區塊：十全劍
right_frame = tk.LabelFrame(main_frame, text="十全劍", width=300)
right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
right_canvas = tk.Canvas(right_frame)
right_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
right_scrollbar.pack(side="right", fill="y")
right_canvas.pack(side="left", fill="both", expand=True)
right_canvas.config(yscrollcommand=right_scrollbar.set)

# 在 Canvas 裡創建一個 Frame 用來放置內容
right_frame_content = tk.Frame(right_canvas)
right_canvas.create_window((0, 0), window=right_frame_content, anchor="nw")

# 更新 Frame 大小
def on_right_frame_configure(event):
    right_canvas.config(scrollregion=right_canvas.bbox("all"))

right_frame_content.bind("<Configure>", on_right_frame_configure)

# 主循環
window.mainloop()