import yfinance as yf
import pandas as pd
from ui_components import create_label, create_separator
from utils import format_number

def fetch_stock_info(stock_entry, left_frame_content_1, left_frame_content_2, left_frame_content_3, center_frame_content, right_frame_content):
    """獲取並顯示股票基本資訊和財務數據"""
    stock_symbol = stock_entry.get()
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.info  # 獲取股票基本資訊
    
   # 使用迴圈遍歷字典中的所有鍵值對
    # for key, value in stock_info.items():
    #     print(f"{key}: {value}")
    # 清空區塊 1 和區塊 2 的內容
    clear_frame_content(left_frame_content_1)
    clear_frame_content(left_frame_content_2)
    clear_frame_content(left_frame_content_3)
    clear_frame_content(center_frame_content)
    clear_frame_content(right_frame_content)

    # 顯示基本資訊
    company_info_fields = [
        ("longName", "Long Name", "公司名稱"),
        ("industry", "Industry", "產業"),
        ("symbol", "Symbol", "股票代號"),
        ("sector", "Sector", "產業類別"),
        ("longBusinessSummary", "Long Business Summary", "公司業務簡介")
    ]

    display_basic_info(stock_info, left_frame_content_1, company_info_fields)
    
    basic_info_fields = [
        ("marketCap", "Market Cap", "市值"),
        ("fiftyTwoWeekLow", "52-Week Low", "52週最低價"),
        ("fiftyTwoWeekHigh", "52-Week High", "52週最高價"),
        ("fiftyDayAverage", "50-Day Average", "50日均價"),
        ("trailingEps", "Trailing EPS", "每股盈餘"),
        ("forwardEps", "Forward EPS", "預期每股盈餘"),
        ("trailingPE", "Trailing P/E", "本益比"),
        ("forwardPE", "Forward P/E", "預期本益比"),
        ("trailingPegRatio", "Trailing PEG Ratio", "本益成長比率"),
        ("earningsGrowth", "Earnings Growth", "收益增長率"),
        ("revenueGrowth", "Revenue Growth", "營收增長率"),
        ("fiveYearAvgDividendYield", "5-Year Avg Dividend Yield", "五年平均股息率"),
        ("profitMargins", "Profit Margins", "利潤率"),
        ("sharesOutstanding", "Shares Outstanding", "在外流通股數"),
        ("lastSplitDate", "Last Split Date", "最近拆股日期"),
        ("grossMargins", "Gross Margins", "毛利率"),
        ("beta", "Beta", "貝塔值"),
    ]
    display_basic_info(stock_info, left_frame_content_2, basic_info_fields)

    # 顯示財務數據
    financial_fields = [
        ("marketCap", "Market Cap", "市值"),
        ("enterpriseValue", "Enterprise Value", "企業價值"),
        ("profitMargins", "Profit Margins", "利潤率"),
        ("grossMargins", "Gross Margins", "毛利率"),
        ("operatingMargins", "Operating Margins", "營業利潤率"),
        ("debtToEquity", "Debt to Equity", "負債股本比率"),
        ("returnOnAssets", "Return on Assets", "資產報酬率"),
        ("returnOnEquity", "Return on Equity", "股東權益報酬率"),
        ("revenueGrowth", "Revenue Growth", "營收增長率"),
        ("earningsGrowth", "Earnings Growth", "收益增長率"),
        ("totalDebt", "Total Debt", "總負債"),
        ("sharesOutstanding", "Shares Outstanding", "在外流通股數"),
        ("operatingCashflow", "Operating Cashflow", "營業現金流量"),
        ("freeCashflow", "Free Cashflow", "自由現金流量"),
    ]

    # 獲取並顯示 Net Income
    try:
        income_statement = stock.financials
        net_income = income_statement.loc["Net Income"].iloc[0] if "Net Income" in income_statement.index else "N/A"
        formatted_net_income = format_number(net_income)
    except Exception:
        formatted_net_income = "N/A"

    financial_fields.append(("netIncome", "Net Income", f"淨利潤: {formatted_net_income}"))

    # 獲取保留盈餘並計算長期淨利
    try:
        balance_sheet = stock.balance_sheet
        # 獲取保留盈餘 (Retained Earnings) 數據
        retained_earnings = balance_sheet.loc["Retained Earnings"].iloc[0]
        formatted_retained_earnings = format_number(retained_earnings)

        # 計算長期淨利，這裡假設長期淨利等於保留盈餘
        long_term_net_income = retained_earnings
        formatted_long_term_net_income = format_number(long_term_net_income)

        # print(f"最新的 Retained Earnings: {formatted_retained_earnings}")
        # print(f"估算的 Long Term Net Income: {formatted_long_term_net_income}")
    except Exception as e:
        print("無法取得 Retained Earnings:", str(e))
        formatted_retained_earnings = "N/A"
        formatted_long_term_net_income = "N/A"

    # 在 financial_fields 中添加保留盈餘和長期淨利數據
    financial_fields.append(("retainedEarnings", "Retained Earnings", f"保留盈餘: {formatted_retained_earnings}"))
    financial_fields.append(("longTermNetIncome", "Long Term Net Income", f"長期淨利: {formatted_long_term_net_income}"))


    # 獲取財務報表中的長期債務數據
    try:
        balance_sheet = stock.balance_sheet

        # 獲取最新的 Long Term Debt 數據
        latest_long_term_debt = balance_sheet.loc["Long Term Debt"].iloc[0]
        formatted_long_term_debt = format_number(latest_long_term_debt)

        # print(f"最新的 Long Term Debt: {formatted_long_term_debt}")
    except Exception as e:
        print("無法取得 Long Term Debt:", str(e))
        formatted_long_term_debt = "N/A"

    # 在 financial_fields 中添加長期負債數據
    financial_fields.append(("longTermDebt", "Long Term Debt", f"長期負債: {formatted_long_term_debt}"))

    # 確保在 display_financial_data() 被呼叫之前 financial_fields 已經包含最新的數據
    display_financial_data(stock, center_frame_content, financial_fields)

    # 顯示 sharesOutstanding 成長狀況
    try:
        shares_outstanding = stock_info.get("sharesOutstanding", "N/A")
        previous_shares_outstanding = 5000000000  # 假設一個數值作為過去的股數（實際應該從歷史資料取得）

        if shares_outstanding != "N/A" and previous_shares_outstanding != "N/A":
            if previous_shares_outstanding != 0:
                growth_rate = ((shares_outstanding - previous_shares_outstanding) / previous_shares_outstanding) * 100
                growth_status = "成長" if growth_rate > 0 else "下降"
                formatted_growth_rate = f"{abs(growth_rate):.2f}%"
                result = f"{growth_status} ({formatted_growth_rate})"
            else:
                result = "N/A"
        else:
            result = "N/A"

        create_label(center_frame_content, "Shares Outstanding Growth (股數成長狀況):", 2 * (len(financial_fields) + 5) - 1)
        create_label(center_frame_content, result, 2 * (len(financial_fields) + 5) - 1, column=1)
        create_separator(center_frame_content, 2 * (len(financial_fields) + 5))
    except Exception as e:
        create_label(center_frame_content, "Shares Outstanding Growth (股數成長狀況):", 2 * (len(financial_fields) + 5) - 1)
        create_label(center_frame_content, "N/A", 2 * (len(financial_fields) + 5) - 1, column=1)
        create_separator(center_frame_content, 2 * (len(financial_fields) + 5))

    # 顯示 Growing Equity 成長狀況
    try:
        balance_sheet = stock.balance_sheet
        stockholders_equity = balance_sheet.loc["Stockholders Equity"].iloc[0] if "Stockholders Equity" in balance_sheet.index else "N/A"
        previous_stockholders_equity = balance_sheet.loc["Stockholders Equity"].iloc[1] if "Stockholders Equity" in balance_sheet.index and len(balance_sheet.loc["Stockholders Equity"]) > 1 else "N/A"

        if stockholders_equity != "N/A" and previous_stockholders_equity != "N/A":
            if previous_stockholders_equity != 0:
                equity_growth_rate = ((stockholders_equity - previous_stockholders_equity) / previous_stockholders_equity) * 100
                equity_status = "成長" if equity_growth_rate > 0 else f"下降 ({equity_growth_rate:.2f}%)"
            else:
                equity_status = "N/A"
        else:
            equity_status = "N/A"

        create_label(center_frame_content, "Growing Equity (股東權益成長):", 2 * (len(financial_fields) + 6) - 1)
        create_label(center_frame_content, equity_status, 2 * (len(financial_fields) + 6) - 1, column=1)
        create_separator(center_frame_content, 2 * (len(financial_fields) + 6))
    except Exception as e:
        create_label(center_frame_content, "Growing Equity (股東權益成長):", 2 * (len(financial_fields) + 6) - 1)
        create_label(center_frame_content, "N/A", 2 * (len(financial_fields) + 6) - 1, column=1)
        create_separator(center_frame_content, 2 * (len(financial_fields) + 6))

    # 顯示 Investing Cash Flow
    try:
        cash_flow = stock.cashflow
        investing_cash_flow = cash_flow.loc['Investing Cash Flow'].iloc[0] if 'Investing Cash Flow' in cash_flow.index else "N/A"
        formatted_investing_cash_flow = format_number(investing_cash_flow)
    except Exception:
        formatted_investing_cash_flow = "N/A"

    create_label(center_frame_content, "Investing Cash Flow (投資活動現金流量):", 2 * (len(financial_fields) + 7) - 1)
    create_label(center_frame_content, formatted_investing_cash_flow, 2 * (len(financial_fields) + 7) - 1, column=1)
    create_separator(center_frame_content, 2 * (len(financial_fields) + 7))

    # 顯示 Financing Cash Flow
    try:
        cash_flow = stock.cashflow
        # 直接嘗試取出 Financing Cash Flow
        financing_cash_flow = cash_flow.loc['Financing Cash Flow'].iloc[0] if 'Financing Cash Flow' in cash_flow.index else "N/A"
        
        # 如果成功獲取且不是 'N/A'，則格式化數字
        if financing_cash_flow != "N/A":
            formatted_financing_cash_flow = format_number(financing_cash_flow)
        else:
            formatted_financing_cash_flow = "N/A"
    except Exception as e:
        # 如果在取值過程中遇到任何問題，將顯示 'N/A'
        formatted_financing_cash_flow = "N/A"

    # 顯示 'Financing Cash Flow' 的結果
    create_label(center_frame_content, "Financing Cash Flow (籌資活動現金流量):", 2 * (len(financial_fields) + 8) - 1)
    create_label(center_frame_content, formatted_financing_cash_flow, 2 * (len(financial_fields) + 8) - 1, column=1)
    create_separator(center_frame_content, 2 * (len(financial_fields) + 8))

    # 顯示十全劍的條件
    # 條件 1: P/E < 25 || PEG < 1.0
    create_label(right_frame_content, "條件 1: P/E < 25 || PEG < 1.0", 0)
    condition_1_met = (stock_info.get('trailingPE', float('inf')) < 25) or (stock_info.get('trailingPegRatio', float('inf')) < 1.0)
    create_label(right_frame_content, "✅" if condition_1_met else "❌", 0, column=1)

    # 條件 2: revenueGrowth > 0
    create_label(right_frame_content, "條件 2: 營收增長率 > 0", 1)
    condition_2_met = stock_info.get('revenueGrowth', 0) > 0
    create_label(right_frame_content, "✅" if condition_2_met else "❌", 1, column=1)

    # 條件 3: formatted_growth > 0
    create_label(right_frame_content, "條件 3: 營業利潤成長率 > 0", 2)
    condition_3_met = calculate_growth_rate(stock.financials.loc['Operating Income']) != "N/A" and float(calculate_growth_rate(stock.financials.loc['Operating Income']).replace('%', '')) > 0
    create_label(right_frame_content, "✅" if condition_3_met else "❌", 2, column=1)

    # 條件 4: formatted_net_income_growth > 0
    create_label(right_frame_content, "條件 4: 淨利潤成長率 > 0", 3)
    condition_4_met = calculate_growth_rate(stock.financials.loc['Net Income']) != "N/A" and float(calculate_growth_rate(stock.financials.loc['Net Income']).replace('%', '')) > 0
    create_label(right_frame_content, "✅" if condition_4_met else "❌", 3, column=1)

    # 條件 5: 流動資產 > 流動負債
    create_label(right_frame_content, "條件 5: 流動資產 > 流動負債", 4)
    try:
        current_assets = stock.balance_sheet.loc["Current Assets"].iloc[0] if "Current Assets" in stock.balance_sheet.index else 0
        current_liabilities = stock.balance_sheet.loc["Current Liabilities"].iloc[0] if "Current Liabilities" in stock.balance_sheet.index else 0
        condition_5_met = current_assets > current_liabilities
        create_label(right_frame_content, "✅" if condition_5_met else "❌", 4, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 4, column=1)

    # 條件 6: 長期負債/長期淨利 < 4
    create_label(right_frame_content, "條件 6: 長期負債 / 長期淨利 < 4", 5)
    try:
        long_term_debt = balance_sheet.loc["Long Term Debt"].iloc[0] if "Long Term Debt" in balance_sheet.index else None
        long_term_net_income = retained_earnings if retained_earnings != "N/A" else None
        if long_term_debt is not None and long_term_net_income is not None and long_term_net_income != 0:
            condition_6_met = (long_term_debt / long_term_net_income) < 4
        else:
            condition_6_met = False
        create_label(right_frame_content, "✅" if condition_6_met else "❌", 5, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 5, column=1)

    # 條件 7: 股東權益正成長 equity_growth_rate > 0
    create_label(right_frame_content, "條件 7: 股東權益正成長", 6)
    try:
        condition_7_met = equity_growth_rate != "N/A" and float(equity_growth_rate.replace('%', '')) > 0
        create_label(right_frame_content, "✅" if condition_7_met else "❌", 6, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 6, column=1)

    # 條件 8: 流通在外股數下降
    create_label(right_frame_content, "條件 8: 流通在外股數下降", 7)
    try:
        condition_8_met = growth_rate < 0
        create_label(right_frame_content, "✅" if condition_8_met else "❌", 7, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 7, column=1)

    # 條件 9: 營業金流 > 投資金流 && 營業金流 > 融資金流
    create_label(right_frame_content, "條件 9: 營業金流 > 投資金流 && 營業金流 > 融資金流", 8)
    try:
        operating_cash_flow = stock.cashflow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in stock.cashflow.index else None
        condition_9_met = operating_cash_flow is not None and operating_cash_flow > investing_cash_flow and operating_cash_flow > financing_cash_flow
        create_label(right_frame_content, "✅" if condition_9_met else "❌", 8, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 8, column=1)

    # 條件 10: Growing Free Cash Flow
    create_label(right_frame_content, "條件 10: 自由現金流正成長", 9)
    try:
        free_cash_flow = stock.cashflow.loc['Free Cash Flow'] if 'Free Cash Flow' in stock.cashflow.index else None
        condition_10_met = calculate_growth_rate(free_cash_flow) != "N/A" and float(calculate_growth_rate(free_cash_flow).replace('%', '')) > 0
        create_label(right_frame_content, "✅" if condition_10_met else "❌", 9, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 9, column=1)

    # 將 balance_sheet 存成 Excel 檔案
    try:
        balance_sheet = stock.balance_sheet
        balance_sheet.to_excel("./balance_sheet.xlsx")
    except Exception as e:
        print(f"Error saving balance sheet to Excel: {e}")

def clear_frame_content(frame):
    """清空框架內容"""
    for widget in frame.winfo_children():
        widget.destroy()

def display_basic_info(stock_info, content_frame, basic_info_fields):
    """顯示基本資訊"""
    # create_label(content_frame, "基本資訊", 0, columnspan=2, pady=5)

    # 打印出參數名稱
    for key in stock_info.keys():
        print(key)
    for idx, (field, eng_label, label) in enumerate(basic_info_fields, start=1):
        value = stock_info.get(field, "N/A")  # 如果字段不存在，顯示 "N/A"
        formatted_value = format_number(value)  # 格式化數字
        create_label(content_frame, f"{eng_label} ({label}):", 2 * idx - 1)
        create_label(content_frame, formatted_value, 2 * idx - 1, column=1)
        create_separator(content_frame, 2 * idx)

def display_financial_data(stock, content_frame, financial_fields):
    """顯示財務數據"""
    # create_label(content_frame, "財務數據", 0, columnspan=2, pady=5)
    for idx, (field, eng_label, label) in enumerate(financial_fields, start=1):
        value = stock.info.get(field, "N/A") if field not in ["netIncome", "longTermDebt", "retainedEarnings", "longTermNetIncome"] else label.split(': ')[1]  # 如果字段不存在，顯示 "N/A"
        formatted_value = format_number(value) if field not in ["netIncome", "longTermDebt", "retainedEarnings", "longTermNetIncome"] else value  # 格式化數字
        create_label(content_frame, f"{eng_label} ({label.split(':')[0]}):", 2 * idx - 1)
        create_label(content_frame, formatted_value, 2 * idx - 1, column=1)
        create_separator(content_frame, 2 * idx)

    # 顯示營業利潤成長率和淨利潤成長率
    display_growth_rates(stock, content_frame, len(financial_fields))
    display_current_assets_liabilities(stock, content_frame, len(financial_fields))

def display_growth_rates(stock, content_frame, financial_fields_len):
    """顯示營業利潤成長率和淨利潤成長率"""
    try:
        income_statement = stock.financials
        # 營業利潤成長率
        operating_income = income_statement.loc["Operating Income"]
        formatted_growth = calculate_growth_rate(operating_income)
    except Exception:
        formatted_growth = "N/A"

    # 顯示營業利潤成長率
    create_label(content_frame, "Growing Operating Income (營業利潤成長):", 2 * (financial_fields_len + 1) - 1)
    create_label(content_frame, formatted_growth, 2 * (financial_fields_len + 1) - 1, column=1)
    create_separator(content_frame, 2 * (financial_fields_len + 1))

    # 獲取並計算淨利潤成長率
    try:
        net_income = income_statement.loc["Net Income"]
        formatted_net_income_growth = calculate_growth_rate(net_income)
    except Exception:
        formatted_net_income_growth = "N/A"

    # 顯示淨利潤成長率
    create_label(content_frame, "Growing Net Income (淨利潤成長):", 2 * (financial_fields_len + 2) - 1)
    create_label(content_frame, formatted_net_income_growth, 2 * (financial_fields_len + 2) - 1, column=1)
    create_separator(content_frame, 2 * (financial_fields_len + 2))

def calculate_growth_rate(data_series):
    """計算成長率"""
    if len(data_series) >= 2:
        latest_value = data_series.iloc[0]
        previous_value = data_series.iloc[1]
        if previous_value != 0:
            return f"{((latest_value - previous_value) / previous_value * 100):.2f}%"
    return "N/A"

def display_current_assets_liabilities(stock, content_frame, financial_fields_len):
    """顯示流動資產和流動負債"""
    try:
        balance_sheet = stock.balance_sheet
        # 流動資產
        current_assets = balance_sheet.loc["Current Assets"].iloc[0] if "Current Assets" in balance_sheet.index else 0
        formatted_current_assets = format_number(current_assets)
    except Exception:
        formatted_current_assets = "N/A"

    # 顯示流動資產
    create_label(content_frame, "Current Assets (流動資產):", 2 * (financial_fields_len + 3) - 1)
    create_label(content_frame, formatted_current_assets, 2 * (financial_fields_len + 3) - 1, column=1)
    create_separator(content_frame, 2 * (financial_fields_len + 3))

    # 獲取流動負債組成項目並計算流動負債總值
    try:
        current_liabilities = balance_sheet.loc["Current Liabilities"].iloc[0] if "Current Liabilities" in balance_sheet.index else 0
        formatted_current_liabilities = format_number(current_liabilities)
    except Exception:
        formatted_current_liabilities = "N/A"

    # 顯示流動負債
    create_label(content_frame, "Current Liabilities (流動負債):", 2 * (financial_fields_len + 4) - 1)
    create_label(content_frame, formatted_current_liabilities, 2 * (financial_fields_len + 4) - 1, column=1)
    create_separator(content_frame, 2 * (financial_fields_len + 4))
