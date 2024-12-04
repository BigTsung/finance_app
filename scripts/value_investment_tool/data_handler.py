import yfinance as yf
import pandas as pd
from ui_components import create_label, create_separator
from utils import format_number
import traceback

def fetch_stock_info(stock_entry, left_frame_content_1, left_frame_content_2, left_frame_content_3, center_frame_content, right_frame_content):
    """獲取並顯示股票基本資訊和財務數據"""
    stock_symbol = stock_entry.get()
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.info  # 獲取股票基本資訊
    
    # 查看財務報表中的所有字段
    financials = stock.financials
    quarterly_financials = stock.quarterly_financials
    
    balance_sheet = stock.balance_sheet
    quarterly_balance_sheet = stock.quarterly_balance_sheet
    
    cash_flow = stock.cashflow
    quarterly_cashflow = stock.quarterly_cashflow


    pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    print(quarterly_balance_sheet)
    # print(quarterly_financials)
    # 在完成後恢復顯示選項
    pd.reset_option('display.max_rows')
    # pd.reset_option('display.max_columns')
    # try:
    #     # 獲取財務資料
    #     financials = stock.financials
    #     balance_sheet = stock.balance_sheet
    #     cash_flow = stock.cashflow

    #     print(stock.quarterly_financials)

    #     # 將資料存成 Excel 檔案
    #     with pd.ExcelWriter('stock_data.xlsx') as writer:
    #         financials.to_excel(writer, sheet_name='Financials')
    #         balance_sheet.to_excel(writer, sheet_name='Balance Sheet')
    #         cash_flow.to_excel(writer, sheet_name='Cash Flow')

    #     print("資料已成功存成 Excel 檔案")

    # except Exception as e:
    #     print(f"Error retrieving financial data: {e}")

    #     print(balance_sheet)

    # 清空區塊內容
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
        net_income = quarterly_financials.loc["Net Income"].iloc[0] if "Net Income" in quarterly_financials.index else "N/A"
        formatted_net_income = format_number(net_income)
    except Exception:
        formatted_net_income = "N/A"

    financial_fields.append(("netIncome", "Net Income", f"淨利: {formatted_net_income}"))

    # # 獲取保留盈餘並計算長期淨利
    # try:
    #     # 獲取保留盈餘 (Retained Earnings) 數據
    #     retained_earnings = balance_sheet.loc["Retained Earnings"].iloc[0]
    #     formatted_retained_earnings = format_number(retained_earnings)

    #     # 計算長期淨利，這裡假設長期淨利等於保留盈餘
    #     long_term_net_income = retained_earnings
    #     formatted_long_term_net_income = format_number(long_term_net_income)
    # except Exception as e:
    #     print("無法取得 Retained Earnings:", str(e))
    #     formatted_retained_earnings = "N/A"
    #     formatted_long_term_net_income = "N/A"

    # # 在 financial_fields 中添加保留盈餘和長期淨利數據
    # financial_fields.append(("retainedEarnings", "Retained Earnings", f"保留盈餘: {formatted_retained_earnings}"))
    # financial_fields.append(("longTermNetIncome", "Long Term Net Income", f"長期淨利: {formatted_long_term_net_income}"))

    # 獲取財務報表中的長期債務數據
    try:
        # 獲取最新的 Long Term Debt 數據
        latest_long_term_debt = balance_sheet.loc["Long Term Debt"].iloc[0]
        formatted_long_term_debt = format_number(latest_long_term_debt)
    except Exception as e:
        print("無法取得 Long Term Debt:", str(e))
        formatted_long_term_debt = "N/A"

    # 在 financial_fields 中添加長期負債數據
    financial_fields.append(("longTermDebt", "Long Term Debt", f"長期負債: {formatted_long_term_debt}"))

    # 確保在 display_financial_data() 被呼叫之前 financial_fields 已經包含最新的數據
    display_financial_data(stock, center_frame_content, financial_fields)

    # 顯示十全劍條件
    display_condition_1(stock_info, right_frame_content)
    display_condition_2(quarterly_financials, right_frame_content)
    display_condition_3(quarterly_financials, right_frame_content)
    display_condition_4(quarterly_financials, right_frame_content)
    display_condition_5(quarterly_balance_sheet, right_frame_content)
    display_condition_6(quarterly_balance_sheet, quarterly_financials, right_frame_content)
    display_condition_7(quarterly_balance_sheet, right_frame_content)

    display_condition_8(quarterly_financials, right_frame_content)
    display_condition_9(quarterly_cashflow, right_frame_content)
    display_condition_10(quarterly_cashflow, right_frame_content)

def display_condition_1(stock_info, right_frame_content):
    create_label(right_frame_content, "條件 1: P/E < 25 || PEG < 1.0", 0)
    condition_1_met = (stock_info.get('trailingPE', float('inf')) < 25) or (stock_info.get('trailingPegRatio', float('inf')) < 1.0)
    create_label(right_frame_content, "✅" if condition_1_met else "❌", 0, column=1)

# def display_condition_2(stock_info, right_frame_content):
#     create_label(right_frame_content, "條件 2: 營收增長", 1)
#     condition_2_met = stock_info.get('revenueGrowth', 0) > 0
#     create_label(right_frame_content, "✅" if condition_2_met else "❌", 1, column=1)

def display_condition_2(quarterly_financials, right_frame_content):
    create_label(right_frame_content, "條件 2: 營收增長(最新季-上一季)", 1)
    try:
        total_revenue = quarterly_financials.loc['Total Revenue']
        if len(total_revenue) >= 2:
            latest_revenue = total_revenue.iloc[0]
            previous_revenue = total_revenue.iloc[1]
            growth_rate = ((latest_revenue - previous_revenue) / previous_revenue) * 100 if previous_revenue != 0 else 0
            print("CONDITION 2")
            print(latest_revenue)
            print(previous_revenue)
            print(growth_rate)
            condition_2_met = growth_rate > 0
        else:
            condition_2_met = False
    except Exception:
        condition_2_met = False
    create_label(right_frame_content, "✅" if condition_2_met else "❌", 1, column=1)

# def display_condition_3(financials, right_frame_content):
#     create_label(right_frame_content, "條件 3: 營業利益成長", 2)
#     try:
#         formatted_growth = calculate_growth_rate(financials.loc['Operating Income'])
#         condition_3_met = formatted_growth != "N/A" and float(formatted_growth.replace('%', '')) > 0
#         create_label(right_frame_content, "✅" if condition_3_met else "❌", 2, column=1)
#     except Exception:
#         create_label(right_frame_content, "❌", 2, column=1)

def display_condition_3(quarterly_financials, right_frame_content):
    create_label(right_frame_content, "條件 3: 營業利益成長", 2)
    try:
        # 獲取最新一季和前一季的營業收入數據
        latest_value = quarterly_financials.loc['Operating Income'].iloc[0]
        previous_value = quarterly_financials.loc['Operating Income'].iloc[1]

        # 計算差值和成長比率
        if pd.notna(latest_value) and pd.notna(previous_value) and previous_value != 0:
            difference = latest_value - previous_value
            growth_rate = (difference / previous_value) * 100

            print("CONDITION 3")
            print(latest_value)
            print(previous_value)
            print(growth_rate)
            condition_3_met = growth_rate > 0
        else:
            condition_3_met = False

        create_label(right_frame_content, "✅" if condition_3_met else "❌", 2, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 2, column=1)

# def display_condition_4(financials, right_frame_content):
#     create_label(right_frame_content, "條件 4: 淨收入成長", 3)
#     try:
#         formatted_net_income_growth = calculate_growth_rate(financials.loc['Net Income'])
#         condition_4_met = formatted_net_income_growth != "N/A" and float(formatted_net_income_growth.replace('%', '')) > 0
#         create_label(right_frame_content, "✅" if condition_4_met else "❌", 3, column=1)
#     except Exception:
#         create_label(right_frame_content, "❌", 3, column=1)


def display_condition_4(quarterly_financials, right_frame_content):
    create_label(right_frame_content, "條件 4: 淨收入成長", 3)
    try:
        latest_net_income = quarterly_financials.loc['Net Income'].iloc[0]
        previous_net_income = quarterly_financials.loc['Net Income'].iloc[1]
        if pd.notna(latest_net_income) and pd.notna(previous_net_income):
            difference = latest_net_income - previous_net_income
            growth_rate = (difference / previous_net_income) * 100
            condition_4_met = growth_rate > 0

            print("CONDITION 4")
            print(latest_net_income)
            print(previous_net_income)
            print(growth_rate)
        else:
            condition_4_met = False
        create_label(right_frame_content, "✅" if condition_4_met else "❌", 3, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 3, column=1)


def display_condition_5(quarterly_balance_sheet, right_frame_content):
    create_label(right_frame_content, "條件 5: 流動資產 > 流動負債", 4)
    try:
        current_assets = quarterly_balance_sheet.loc["Current Assets"].iloc[0] if "Current Assets" in quarterly_balance_sheet.index else 0
        current_liabilities = quarterly_balance_sheet.loc["Current Liabilities"].iloc[0] if "Current Liabilities" in quarterly_balance_sheet.index else 0
        condition_5_met = current_assets > current_liabilities

        print("CONDITION 5")
        print(current_assets)
        print(current_liabilities)
        create_label(right_frame_content, "✅" if condition_5_met else "❌", 4, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 4, column=1)

# def display_condition_6(balance_sheet, right_frame_content, retained_earnings):
#     create_label(right_frame_content, "條件 6: 長期負債 / 長期淨利 < 4", 5)
#     try:
#         long_term_debt = balance_sheet.loc["Long Term Debt"].iloc[0] if "Long Term Debt" in balance_sheet.index else None
#         long_term_net_income = retained_earnings if retained_earnings != "N/A" else None
#         if long_term_debt is not None and long_term_net_income is not None and long_term_net_income != 0:
#             condition_6_met = (long_term_debt / long_term_net_income) < 4
#         else:
#             condition_6_met = False
#         create_label(right_frame_content, "✅" if condition_6_met else "❌", 5, column=1)
#     except Exception:
#         create_label(right_frame_content, "❌", 5, column=1)

def display_condition_6(quarterly_balance_sheet, quarterly_financials, right_frame_content):
    create_label(right_frame_content, "條件 6: 長期負債 / 淨利 < 4", 5)
    try:
        long_term_debt = quarterly_balance_sheet.loc["Long Term Debt"].iloc[0] if "Long Term Debt" in quarterly_balance_sheet.index else None
        net_income = quarterly_financials.loc['Net Income'].iloc[0]
        if long_term_debt is not None and net_income is not None and net_income != 0:
            # print(f"Ratio: {long_term_debt / net_income}")

            condition_6_met = (long_term_debt / net_income) < 4
            print("CONDITION 6")
            print(long_term_debt)
            print(net_income)
            print((long_term_debt / net_income))
        else:
            condition_6_met = False
            print("Either long_term_debt or net_income is None or net_income is zero.")
        create_label(right_frame_content, "✅" if condition_6_met else "❌", 5, column=1)
    except Exception as e:
        print("An error occurred:")
        print(str(e))
        traceback.print_exc()  # 這行可以顯示具體的錯誤回溯信息
        create_label(right_frame_content, "❌", 5, column=1)


# def display_condition_7(balance_sheet, right_frame_content):
#     create_label(right_frame_content, "條件 7: 股東權益正成長", 6)
#     try:
#         stockholders_equity = balance_sheet.loc["Stockholders Equity"].iloc[0] if "Stockholders Equity" in balance_sheet.index else "N/A"
#         previous_stockholders_equity = balance_sheet.loc["Stockholders Equity"].iloc[1] if "Stockholders Equity" in balance_sheet.index and len(balance_sheet.loc["Stockholders Equity"]) > 1 else "N/A"

#         if stockholders_equity != "N/A" and previous_stockholders_equity != "N/A" and previous_stockholders_equity != 0:
#             equity_growth_rate = ((stockholders_equity - previous_stockholders_equity) / previous_stockholders_equity) * 100
#             condition_7_met = equity_growth_rate > 0
#         else:
#             condition_7_met = False

#         create_label(right_frame_content, "✅" if condition_7_met else "❌", 6, column=1)
#     except Exception:
#         create_label(right_frame_content, "❌", 6, column=1)

def display_condition_7(quarterly_balance_sheet, right_frame_content):
    create_label(right_frame_content, "條件 7: 股東權益正成長", 6)
    try:
        # 獲取 "Stockholders Equity" 的數據
        if "Stockholders Equity" in quarterly_balance_sheet.index:
            stockholders_equity = quarterly_balance_sheet.loc["Stockholders Equity"]

            # 確保有至少兩個季度的數據進行比較
            if len(stockholders_equity) >= 2:
                current_value = stockholders_equity.iloc[0]  # 最新一季的數據
                previous_value = stockholders_equity.iloc[1]  # 前一季的數據

                if pd.notna(current_value) and pd.notna(previous_value) and previous_value != 0:
                    difference = current_value - previous_value
                    growth_rate = (difference / previous_value) * 100
                    condition_7_met = growth_rate > 0  # 比率為正值表示股東權益成長
                    print("CONDITION 7")
                    print(current_value)
                    print(previous_value)
                    print(growth_rate)
                    create_label(right_frame_content, "✅" if condition_7_met else "❌", 6, column=1)
                else:
                    create_label(right_frame_content, "❌", 6, column=1)
            else:
                create_label(right_frame_content, "❌", 6, column=1)
        else:
            create_label(right_frame_content, "❌", 6, column=1)
    except Exception as e:
        print(f"Error in display_condition_7: {e}")
        create_label(right_frame_content, "❌", 6, column=1)

# def display_condition_8(basic_average_shares, right_frame_content):
#     create_label(right_frame_content, "條件 8: 流通在外股數下降", 7)
#     try:
#         if len(basic_average_shares) >= 2:
#             current_value = basic_average_shares.iloc[0]
#             previous_value = basic_average_shares.iloc[1]

#             if pd.notna(current_value) and pd.notna(previous_value):
#                 difference = current_value - previous_value
#                 condition_8_met = difference < 0
#                 create_label(right_frame_content, "✅" if condition_8_met else "❌", 7, column=1)
#             else:
#                 create_label(right_frame_content, "❌", 7, column=1)
#         else:
#             create_label(right_frame_content, "❌", 7, column=1)
#     except Exception:
#         create_label(right_frame_content, "❌", 7, column=1)

def display_condition_8(quarterly_financials, right_frame_content):
    create_label(right_frame_content, "條件 8: 流通在外股數下降", 7)
    try:
        # 獲取 "Basic Average Shares" 的數據
        if "Basic Average Shares" in quarterly_financials.index:
            basic_average_shares = quarterly_financials.loc["Basic Average Shares"]

            # 確保有至少兩個季度的數據進行比較
            if len(basic_average_shares) >= 2:
                current_value = basic_average_shares.iloc[0]  # 最新一季的數據
                previous_value = basic_average_shares.iloc[1]  # 前一季的數據

                if pd.notna(current_value) and pd.notna(previous_value):
                    difference = current_value - previous_value
                    # growth_rate = (difference / previous_value) * 100
                    condition_8_met = difference < 0  # 比率為負值表示流通股數下降

                    print("CONDITION 8")
                    print(current_value)
                    print(previous_value)
                    create_label(right_frame_content, "✅" if condition_8_met else "❌", 7, column=1)
                else:
                    create_label(right_frame_content, "❌", 7, column=1)
            else:
                create_label(right_frame_content, "❌", 7, column=1)
        else:
            create_label(right_frame_content, "❌", 7, column=1)
    except Exception as e:
        print(f"Error in display_condition_8: {e}")
        create_label(right_frame_content, "❌", 7, column=1)

def display_condition_9(quarterly_cashflow, right_frame_content):
    create_label(right_frame_content, "條件 9: 營業金流 > 投資金流 && 營業金流 > 融資金流", 8)
    try:
        operating_cash_flow = quarterly_cashflow.loc["Operating Cash Flow"].iloc[0]
        financing_cash_flow = quarterly_cashflow.loc["Financing Cash Flow"].iloc[0]
        investing_cash_flow = quarterly_cashflow.loc["Investing Cash Flow"].iloc[0]

        print("CONDITION 9")
        print(operating_cash_flow)
        print(financing_cash_flow)
        print(investing_cash_flow)
        
        condition_9_met = operating_cash_flow is not None and operating_cash_flow > investing_cash_flow and operating_cash_flow > financing_cash_flow
        create_label(right_frame_content, "✅" if condition_9_met else "❌", 8, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 8, column=1)

# def display_condition_10(financials, right_frame_content):
#     create_label(right_frame_content, "條件 10: 自由現金流正成長", 9)
#     try:
#         free_cash_flow = financials.loc['Free Cash Flow'] if 'Free Cash Flow' in financials.index else None
#         condition_10_met = calculate_growth_rate(free_cash_flow) != "N/A" and float(calculate_growth_rate(free_cash_flow).replace('%', '')) > 0
#         create_label(right_frame_content, "✅" if condition_10_met else "❌", 9, column=1)
#     except Exception:
#         create_label(right_frame_content, "❌", 9, column=1)

def display_condition_10(quarterly_cashflow, right_frame_content):
    create_label(right_frame_content, "條件 10: 自由現金流正成長", 9)
    try:
        # 獲取 "Free Cash Flow" 的數據
        if "Free Cash Flow" in quarterly_cashflow.index:
            free_cash_flow = quarterly_cashflow.loc["Free Cash Flow"]

            # 確保有至少兩個季度的數據進行比較
            if len(free_cash_flow) >= 2:
                current_value = free_cash_flow.iloc[0]  # 最新一季的數據
                previous_value = free_cash_flow.iloc[1]  # 前一季的數據

                if pd.notna(current_value) and pd.notna(previous_value):
                    difference = current_value - previous_value
                    # growth_rate = (difference / previous_value) * 100

                    print("CONDITION 10")
                    print(current_value)
                    print(previous_value)
                    condition_10_met = difference > 0  # 比率為正值表示自由現金流成長
                    create_label(right_frame_content, "✅" if condition_10_met else "❌", 9, column=1)
                else:
                    create_label(right_frame_content, "❌", 9, column=1)
            else:
                create_label(right_frame_content, "❌", 9, column=1)
        else:
            create_label(right_frame_content, "❌", 9, column=1)
    except Exception as e:
        print(f"Error in display_condition_10: {e}")
        create_label(right_frame_content, "❌", 9, column=1)

def clear_frame_content(frame):
    """清空框架內容"""
    for widget in frame.winfo_children():
        widget.destroy()

def display_basic_info(stock_info, content_frame, basic_info_fields):
    """顯示基本資訊"""
    for idx, (field, eng_label, label) in enumerate(basic_info_fields, start=1):
        value = stock_info.get(field, "N/A")  # 如果字段不存在，顯示 "N/A"
        formatted_value = format_number(value)  # 格式化數字
        create_label(content_frame, f"{eng_label} ({label}):", 2 * idx - 1)
        create_label(content_frame, formatted_value, 2 * idx - 1, column=1)
        create_separator(content_frame, 2 * idx)

def display_financial_data(stock, content_frame, financial_fields):
    """顯示財務數據"""
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
