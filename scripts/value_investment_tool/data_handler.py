import yfinance as yf
import pandas as pd
from ui_components import create_label, create_separator
from utils import format_number
import traceback
from scipy.stats import linregress
import numpy as np

# 全域參數
# condition 1
PE_THRESHOLD = 25
PEG_THRESHOLD = 1.0


def fetch_stock_info(stock_entry, left_frame_content_1, ten_punch_content):
# def fetch_stock_info(stock_entry, left_frame_content_1, left_frame_content_2, ten_punch_content, quarterly_cashflow_content, quarterly_balance_sheet_content):
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

    print(stock_info)

    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # print(financials)
    # print(quarterly_financials)
    # print(cash_flow)
    # # print(quarterly_financials)
    # # 在完成後恢復顯示選項
    # pd.reset_option('display.max_rows')
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
    # clear_frame_content(left_frame_content_2)
    clear_frame_content(ten_punch_content)
    # clear_frame_content(quarterly_cashflow_content)
    # clear_frame_content(quarterly_balance_sheet_content)

    # 顯示基本資訊
        # 獲取 stock.info 中的所有鍵
    # stock_info_keys = stock.info.keys()
    # print(stock_info_keys)
    # 將 stock.info 中的所有鍵動態地加入到 company_info_fields 中
    # company_info_fields = [(key, key.replace('_', ' ').title(), key.replace('_', ' ').title()) for key in stock_info_keys]

    company_info_fields = [
        # ("address1", "Address 1", "地址"),
        # ("city", "City", "城市"),
        # ("state", "State", "州"),
        # ("zip", "ZIP Code", "郵遞區號"),
        # ("shortName", "Short Name", "簡稱"),
        ("longName", "Long Name", "全名"),
        ("symbol", "Symbol", "股票代號"),
        ("country", "Country", "國家"),
        ("marketCap", "Market Cap", "市值"),
        ("currency", "Currency", "貨幣"),
        ("enterpriseValue", "Enterprise Value", "企業價值"),
        ("sharesOutstanding", "Shares Outstanding", "在外流通股數"),
        # ("phone", "Phone", "電話"),
        # ("website", "Website", "網站"),
        # ("industry", "Industry", "產業"),
        # ("industryKey", "Industry Key", "產業代碼"),
        # ("industryDisp", "Industry Display", "產業顯示名稱"),
        ("sector", "Sector", "產業類別"),
        # ("sectorKey", "Sector Key", "產業類別代碼"),
        # ("sectorDisp", "Sector Display", "產業類別顯示名稱"),
        # ("longBusinessSummary", "Long Business Summary", "公司業務簡介"),
        ("fullTimeEmployees", "Full Time Employees", "全職員工數"),
        # ("companyOfficers", "Company Officers", "公司高層"),
        ("auditRisk", "Audit Risk", "審計風險"),
        ("boardRisk", "Board Risk", "董事會風險"),
        ("compensationRisk", "Compensation Risk", "薪酬風險"),
        ("shareHolderRightsRisk", "Shareholder Rights Risk", "股東權利風險"),
        ("overallRisk", "Overall Risk", "總體風險"),
        # ("governanceEpochDate", "Governance Epoch Date", "治理時代日期"),
        # ("compensationAsOfEpochDate", "Compensation As Of Epoch Date", "薪酬日期"),
        # ("irWebsite", "Investor Relations Website", "投資者關係網站"),
        # ("maxAge", "Max Age", "最大年齡"),
        ("priceHint", "Price Hint", "價格提示"),
        ("previousClose", "Previous Close", "前一日收盤價"),
        ("open", "Open", "開盤價"),
        ("dayLow", "Day Low", "當日最低價"),
        ("dayHigh", "Day High", "當日最高價"),
        ("regularMarketPreviousClose", "Regular Market Previous Close", "常規市場前收盤價"),
        ("regularMarketOpen", "Regular Market Open", "常規市場開盤價"),
        ("regularMarketDayLow", "Regular Market Day Low", "常規市場最低價"),
        ("regularMarketDayHigh", "Regular Market Day High", "常規市場最高價"),
        ("exDividendDate", "Ex-Dividend Date", "除息日期"),
        ("beta", "Beta", "貝塔值"),
        ("trailingPE", "Trailing P/E", "本益比"),
        ("forwardPE", "Forward P/E", "預期本益比"),
        ("volume", "Volume", "成交量"),
        ("regularMarketVolume", "Regular Market Volume", "常規市場成交量"),
        ("averageVolume", "Average Volume", "平均成交量"),
        ("averageVolume10days", "Average Volume (10 Days)", "十日平均成交量"),
        ("averageDailyVolume10Day", "Average Daily Volume (10 Days)", "十日每日平均成交量"),
        ("bid", "Bid", "買入報價"),
        ("ask", "Ask", "賣出報價"),
        ("bidSize", "Bid Size", "買入數量"),
        ("askSize", "Ask Size", "賣出數量"),
        ("fiftyTwoWeekLow", "52-Week Low", "52周最低價"),
        ("fiftyTwoWeekHigh", "52-Week High", "52周最高價"),
        ("priceToSalesTrailing12Months", "Price to Sales (Trailing 12 Months)", "市銷率"),
        ("fiftyDayAverage", "50-Day Average", "50日均價"),
        ("twoHundredDayAverage", "200-Day Average", "200日均價"),
        ("profitMargins", "Profit Margins", "利潤率"),
        ("floatShares", "Float Shares", "自由流通股數"),
        ("sharesShort", "Shares Short", "賣空股數"),
        ("sharesShortPriorMonth", "Shares Short Prior Month", "前一月賣空股數"),
        ("sharesShortPreviousMonthDate", "Shares Short Previous Month Date", "前一月賣空日期"),
        ("dateShortInterest", "Date Short Interest", "賣空利息日期"),
        ("sharesPercentSharesOut", "Shares Percent Shares Out", "賣空股數佔流通股比例"),
        ("heldPercentInsiders", "Held Percent Insiders", "內部人士持股比例"),
        ("heldPercentInstitutions", "Held Percent Institutions", "機構持股比例"),
        ("shortRatio", "Short Ratio", "賣空比例"),
        ("shortPercentOfFloat", "Short Percent Of Float", "賣空佔自由流通股比例"),
        ("impliedSharesOutstanding", "Implied Shares Outstanding", "隱含在外流通股數"),
        ("bookValue", "Book Value", "每股淨值"),
        ("priceToBook", "Price to Book", "市淨率"),
        ("lastFiscalYearEnd", "Last Fiscal Year End", "上財年結束"),
        ("nextFiscalYearEnd", "Next Fiscal Year End", "下財年結束"),
        ("mostRecentQuarter", "Most Recent Quarter", "最近一季度"),
        ("earningsQuarterlyGrowth", "Earnings Quarterly Growth", "季度收益增長"),
        ("netIncomeToCommon", "Net Income to Common", "淨收入"),
        ("trailingEps", "Trailing EPS", "每股盈餘"),
        ("forwardEps", "Forward EPS", "預期每股盈餘"),
        ("lastSplitFactor", "Last Split Factor", "最近拆股比例"),
        ("lastSplitDate", "Last Split Date", "最近拆股日期"),
        ("enterpriseToRevenue", "Enterprise to Revenue", "企業收入比"),
        ("enterpriseToEbitda", "Enterprise to EBITDA", "企業EBITDA比"),
        ("52WeekChange", "52 Week Change", "52周變化"),
        ("SandP52WeekChange", "S&P 52 Week Change", "標普52周變化"),
        ("exchange", "Exchange", "交易所"),
        ("quoteType", "Quote Type", "報價類型"),
        ("underlyingSymbol", "Underlying Symbol", "基礎股票代號"),
        ("firstTradeDateEpochUtc", "First Trade Date (Epoch UTC)", "首次交易日期"),
        ("timeZoneFullName", "Time Zone Full Name", "時區名稱"),
        ("timeZoneShortName", "Time Zone Short Name", "時區簡稱"),
        ("uuid", "UUID", "UUID"),
        ("messageBoardId", "Message Board ID", "留言板ID"),
        ("gmtOffSetMilliseconds", "GMT Offset Milliseconds", "GMT偏移毫秒"),
        ("currentPrice", "Current Price", "當前價格"),
        ("targetHighPrice", "Target High Price", "目標最高價"),
        ("targetLowPrice", "Target Low Price", "目標最低價"),
        ("targetMeanPrice", "Target Mean Price", "目標平均價"),
        ("targetMedianPrice", "Target Median Price", "目標中間價"),
        ("recommendationMean", "Recommendation Mean", "推薦平均"),
        ("recommendationKey", "Recommendation Key", "推薦鍵"),
        ("numberOfAnalystOpinions", "Number of Analyst Opinions", "分析師意見數量"),
        ("totalCash", "Total Cash", "總現金"),
        ("totalCashPerShare", "Total Cash Per Share", "每股總現金"),
        ("ebitda", "EBITDA", "息稅折舊攤銷前利潤"),
        ("totalDebt", "Total Debt", "總負債"),
        ("quickRatio", "Quick Ratio", "速動比率"),
        ("currentRatio", "Current Ratio", "流動比率"),
        ("totalRevenue", "Total Revenue", "總營收"),
        ("debtToEquity", "Debt to Equity", "負債股本比率"),
        ("revenuePerShare", "Revenue Per Share", "每股營收"),
        ("returnOnAssets", "Return on Assets", "資產報酬率"),
        ("returnOnEquity", "Return on Equity", "股東權益報酬率"),
        ("freeCashflow", "Free Cashflow", "自由現金流量"),
        ("operatingCashflow", "Operating Cashflow", "營業現金流量"),
        ("earningsGrowth", "Earnings Growth", "收益增長率"),
        ("revenueGrowth", "Revenue Growth", "營收增長率"),
        ("grossMargins", "Gross Margins", "毛利率"),
        ("ebitdaMargins", "EBITDA Margins", "EBITDA 利潤率"),
        ("operatingMargins", "Operating Margins", "營業利潤率"),
        ("financialCurrency", "Financial Currency", "財務貨幣"),
        ("trailingPegRatio", "Trailing PEG Ratio", "本益成長比率")
    ]
    display_basic_info(stock_info, left_frame_content_1, company_info_fields)

    # basic_info_fields = [
    #     ("marketCap", "Market Cap", "市值"),
    #     ("fiftyTwoWeekLow", "52-Week Low", "52週最低價"),
    #     ("fiftyTwoWeekHigh", "52-Week High", "52週最高價"),
    #     ("fiftyDayAverage", "50-Day Average", "50日均價"),
    #     ("trailingEps", "Trailing EPS", "每股盈餘"),
    #     ("forwardEps", "Forward EPS", "預期每股盈餘"),
    #     ("trailingPE", "Trailing P/E", "本益比"),
    #     ("forwardPE", "Forward P/E", "預期本益比"),
    #     ("trailingPegRatio", "Trailing PEG Ratio", "本益成長比率"),
    #     ("earningsGrowth", "Earnings Growth", "收益增長率"),
    #     ("revenueGrowth", "Revenue Growth", "營收增長率"),
    #     ("fiveYearAvgDividendYield", "5-Year Avg Dividend Yield", "五年平均股息率"),
    #     ("profitMargins", "Profit Margins", "利潤率"),
    #     ("sharesOutstanding", "Shares Outstanding", "在外流通股數"),
    #     ("lastSplitDate", "Last Split Date", "最近拆股日期"),
    #     ("grossMargins", "Gross Margins", "毛利率"),
    #     ("beta", "Beta", "貝塔值"),
    # ]
    # display_basic_info(stock_info, left_frame_content_2, basic_info_fields)

    balance_sheet_field = [
        ("Treasury Shares Number", "Treasury Shares Number", "庫藏股數"),
        ("Ordinary Shares Number", "Ordinary Shares Number", "普通股數"),
        ("Share Issued", "Share Issued", "已發行股份"),
        ("Total Debt", "Total Debt", "總負債"),
        ("Tangible Book Value", "Tangible Book Value", "有形帳面價值"),
        ("Invested Capital", "Invested Capital", "投入資本"),
        ("Working Capital", "Working Capital", "營運資金"),
        ("Net Tangible Assets", "Net Tangible Assets", "有形資產淨值"),
        ("Capital Lease Obligations", "Capital Lease Obligations", "資本租賃責任"),
        ("Common Stock Equity", "Common Stock Equity", "普通股股本"),
        ("Total Capitalization", "Total Capitalization", "總資本"),
        ("Total Equity Gross Minority Interest", "Total Equity Gross Minority Interest", "股東權益（含少數股權）"),
        ("Stockholders Equity", "Stockholders Equity", "股東權益"),
        ("Gains Losses Not Affecting Retained Earnings", "Gains Losses Not Affecting Retained Earnings", "未影響留存收益的損益"),
        ("Other Equity Adjustments", "Other Equity Adjustments", "其他權益調整"),
        ("Treasury Stock", "Treasury Stock", "庫藏股"),
        ("Retained Earnings", "Retained Earnings", "保留盈餘"),
        ("Additional Paid In Capital", "Additional Paid In Capital", "額外實收資本"),
        ("Capital Stock", "Capital Stock", "股本"),
        ("Common Stock", "Common Stock", "普通股"),
        ("Total Liabilities Net Minority Interest", "Total Liabilities Net Minority Interest", "總負債（扣除少數股權）"),
        ("Total Non Current Liabilities Net Minority Interest", "Total Non Current Liabilities Net Minority Interest", "總非流動負債（扣除少數股權）"),
        ("Other Non Current Liabilities", "Other Non Current Liabilities", "其他非流動負債"),
        ("Non Current Deferred Liabilities", "Non Current Deferred Liabilities", "非流動遞延負債"),
        ("Non Current Deferred Taxes Liabilities", "Non Current Deferred Taxes Liabilities", "非流動遞延稅項負債"),
        ("Long Term Debt And Capital Lease Obligation", "Long Term Debt And Capital Lease Obligation", "長期債務與資本租賃責任"),
        ("Long Term Capital Lease Obligation", "Long Term Capital Lease Obligation", "長期資本租賃責任"),
        ("Long Term Debt", "Long Term Debt", "長期負債"),
        ("Current Liabilities", "Current Liabilities", "流動負債"),
        ("Other Current Liabilities", "Other Current Liabilities", "其他流動負債"),
        ("Current Deferred Liabilities", "Current Deferred Liabilities", "流動遞延負債"),
        ("Current Deferred Revenue", "Current Deferred Revenue", "流動遞延收入"),
        ("Current Debt And Capital Lease Obligation", "Current Debt And Capital Lease Obligation", "流動債務與資本租賃責任"),
        ("Current Debt", "Current Debt", "流動債務"),
        ("Other Current Borrowings", "Other Current Borrowings", "其他流動借款"),
        ("Pensionand Other Post Retirement Benefit Plans Current", "Pensionand Other Post Retirement Benefit Plans Current", "當期養老金及其他退休福利計劃"),
        ("Payables And Accrued Expenses", "Payables And Accrued Expenses", "應付帳款及應計費用"),
        ("Current Accrued Expenses", "Current Accrued Expenses", "當期應計費用"),
        ("Payables", "Payables", "應付帳款"),
        ("Dueto Related Parties Current", "Dueto Related Parties Current", "當期應付關聯方"),
        ("Total Tax Payable", "Total Tax Payable", "應付稅款總額"),
        ("Accounts Payable", "Accounts Payable", "應付帳款"),
        ("Total Assets", "Total Assets", "總資產"),
        ("Total Non Current Assets", "Total Non Current Assets", "總非流動資產"),
        ("Other Non Current Assets", "Other Non Current Assets", "其他非流動資產"),
        ("Non Current Deferred Assets", "Non Current Deferred Assets", "非流動遞延資產"),
        ("Non Current Deferred Taxes Assets", "Non Current Deferred Taxes Assets", "非流動遞延稅項資產"),
        ("Investments And Advances", "Investments And Advances", "投資及預付款"),
        ("Long Term Equity Investment", "Long Term Equity Investment", "長期股權投資"),
        ("Goodwill And Other Intangible Assets", "Goodwill And Other Intangible Assets", "商譽及其他無形資產"),
        ("Other Intangible Assets", "Other Intangible Assets", "其他無形資產"),
        ("Goodwill", "Goodwill", "商譽"),
        ("Net PPE", "Net PPE", "淨固定資產"),
        ("Accumulated Depreciation", "Accumulated Depreciation", "累計折舊"),
        ("Gross PPE", "Gross PPE", "總固定資產"),
        ("Leases", "Leases", "租賃"),
        ("Construction In Progress", "Construction In Progress", "在建工程"),
        ("Other Properties", "Other Properties", "其他物業"),
        ("Machinery Furniture Equipment", "Machinery Furniture Equipment", "機器設備"),
        ("Buildings And Improvements", "Buildings And Improvements", "建築及改良"),
        ("Land And Improvements", "Land And Improvements", "土地及改良"),
        ("Properties", "Properties", "物業"),
        ("Current Assets", "Current Assets", "流動資產"),
        ("Other Current Assets", "Other Current Assets", "其他流動資產"),
        ("Prepaid Assets", "Prepaid Assets", "預付資產"),
        ("Inventory", "Inventory", "庫存"),
        ("Finished Goods", "Finished Goods", "成品"),
        ("Work In Process", "Work In Process", "在製品"),
        ("Raw Materials", "Raw Materials", "原材料"),
        ("Receivables", "Receivables", "應收款項"),
        ("Duefrom Related Parties Current", "Duefrom Related Parties Current", "當期應收關聯方"),
        ("Accounts Receivable", "Accounts Receivable", "應收帳款"),
        ("Cash Cash Equivalents And Short Term Investments", "Cash Cash Equivalents And Short Term Investments", "現金、現金等價物及短期投資"),
        ("Other Short Term Investments", "Other Short Term Investments", "其他短期投資"),
        ("Cash And Cash Equivalents", "Cash And Cash Equivalents", "現金及現金等價物")
    ]

    # display_basic_info(stock_info, quarterly_balance_sheet_content, balance_sheet_field)

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
    # display_financial_data(stock, quarterly_cashflow_content, financial_fields)

    # 顯示十全劍條件
    display_condition_1(stock_info, ten_punch_content)
    display_condition_2(financials, quarterly_financials, ten_punch_content)
    display_condition_3(financials, quarterly_financials, ten_punch_content)
    display_condition_4(financials, quarterly_financials, ten_punch_content)
    display_condition_5(quarterly_balance_sheet, ten_punch_content)
    display_condition_6(quarterly_balance_sheet, quarterly_financials, ten_punch_content)
    display_condition_7(balance_sheet, quarterly_balance_sheet, ten_punch_content)

    display_condition_8(quarterly_financials, ten_punch_content)
    display_condition_9(cash_flow, ten_punch_content)
    display_condition_10(quarterly_cashflow, ten_punch_content)

def display_condition_1(stock_info, right_frame_content, PE_THRESHOLD=25, PEG_THRESHOLD=1.0):
    create_label(right_frame_content, f"條件 1: P/E < {PE_THRESHOLD} || PEG < {PEG_THRESHOLD}", 0)

    try:
        # 取得 trailingPE 和 trailingPegRatio
        trailing_pe = stock_info.get('trailingPE')
        peg_ratio = stock_info.get('trailingPegRatio')

        print("CONDITION 1:", trailing_pe, peg_ratio)

        # 檢查是否有數值，如果沒有數值則顯示警告
        if trailing_pe is None and peg_ratio is None:
            create_label(right_frame_content, "⚠️ P/E 和 PEG 無法取得", 0, column=1)
            return
        elif trailing_pe is None:
            create_label(right_frame_content, "⚠️ P/E 無法取得", 0, column=1)
            return
        elif peg_ratio is None:
            create_label(right_frame_content, "⚠️ PEG 無法取得", 0, column=1)
            return

        # 條件判斷：P/E < 閾值 或 PEG < 閾值
        condition_1_met = (trailing_pe < PE_THRESHOLD) or (peg_ratio < PEG_THRESHOLD)

        # 顯示結果
        create_label(right_frame_content, 
                     f"{'✅' if condition_1_met else '❌'} P/E: {trailing_pe} PEG: {peg_ratio}", 
                     0, column=1)

    except Exception as e:
        print(f"Error in display_condition_1: {e}")
        create_label(right_frame_content, "⚠️ Error 發生", 0, column=1)


def display_condition_2(annual_financials, quarterly_financials, right_frame_content):
    create_label(right_frame_content, "條件 2: 營收正成長(包括 TTM)", 1)

    try:
        # 初始化空列表，用於存放年份和營收
        revenues = []
        years = []

        # 優先考慮 TTM
        if 'Total Revenue' in quarterly_financials.index and len(quarterly_financials.loc['Total Revenue']) >= 4:
            # 計算 TTM 營收
            ttm_revenue = quarterly_financials.loc['Total Revenue'].iloc[:4].sum()
            print(f"TTM 營收計算成功: {ttm_revenue}")
            revenues.append(ttm_revenue)
            years.append("TTM")

        # 加入所有年度數據
        if 'Total Revenue' in annual_financials.index:
            annual_revenues = annual_financials.loc['Total Revenue'].tolist()
            annual_years = annual_financials.columns.tolist()
            revenues.extend(annual_revenues)
            years.extend(annual_years)

        # 如果無可用數據，返回警告
        if not revenues:
            print("無法找到可用的 Total Revenue 數據")
            create_label(right_frame_content, "⚠️ 無可用數據", 1, column=1)
            return

        # 清理數據：移除 nan 或 inf
        revenues = np.array(revenues, dtype=float)
        years = np.array(years)
        valid_indices = np.isfinite(revenues)  # 找出合法數據
        revenues = revenues[valid_indices]
        years = years[valid_indices]

        # 確保數據長度足夠
        if len(revenues) < 2:
            print("有效數據不足，無法計算趨勢")
            create_label(right_frame_content, "⚠️ 數據不足", 1, column=1)
            return

        # 將數據從過去到現在排列
        revenues = revenues[::-1]
        years = years[::-1]

        # 打印取得的年份和數據
        print("取得的年份:", years)
        print("取得的營收資料:", revenues)

        # 使用二次回歸檢測整體趨勢
        x = np.arange(len(revenues), dtype=float)
        coefficients = np.polyfit(x, revenues, 2)  # 二次多項式擬合
        trend = np.poly1d(coefficients)           # 生成擬合函數

        # 計算整體趨勢（使用一階導數的平均值）
        first_derivative = np.polyder(trend, 1)
        avg_slope = np.mean(first_derivative(x))

        # 打印二次回歸結果
        print(f"二次回歸係數: {coefficients}")
        print(f"平均一階導數: {avg_slope:.6f}")

        # 判斷整體趨勢是否攀升
        condition_2_met = avg_slope > 0

        # 顯示結果
        if condition_2_met:
            create_label(right_frame_content, f"✅ ({years[0]}~{years[-1]})", 1, column=1)
            print(f"✅ 整體營收趨勢攀升 ({years[0]}~{years[-1]})")
        else:
            create_label(right_frame_content, "❌", 1, column=1)
            print(f"❌ 整體營收趨勢未攀升 ({years[0]}~{years[-1]})")

    except Exception as e:
        print(f"Error in display_condition_2: {e}")
        create_label(right_frame_content, "❌", 1, column=1)

def display_condition_3(financials, quarterly_financials, right_frame_content, growth_threshold=0.3):
    create_label(right_frame_content, "條件 3: 營運收入成長 (Annual + TTM)", 2)

    try:
        # 初始化空列表，用於存放年份和營運收入
        operating_incomes = []
        years = []

        # 取得最新 3 年的年度數據
        if 'Operating Income' in financials.index:
            annual_operating_incomes = financials.loc['Operating Income'].dropna()
            if len(annual_operating_incomes) >= 3:
                latest_annual_data = annual_operating_incomes.iloc[:3]  # 取最新 3 年數據
                operating_incomes.extend(latest_annual_data.tolist()[::-1])  # 倒序
                years.extend(latest_annual_data.index.tolist()[::-1])  # 年份倒序

        # 計算 TTM 營運收入
        if 'Operating Income' in quarterly_financials.index and len(quarterly_financials.loc['Operating Income']) >= 4:
            operating_income_ttm = quarterly_financials.loc['Operating Income'].iloc[:4].sum()
            print(f"TTM 營運收入: {operating_income_ttm}")
            operating_incomes.append(operating_income_ttm)
            years.append("TTM")

        # 確保數據完整（必須有 3 年年度數據 + TTM）
        if len(operating_incomes) != 4:
            print("有效數據不足，無法進行分析")
            create_label(right_frame_content, "⚠️ 數據不足", 2, column=1)
            return

        # 打印數據以供檢查
        print("取得的年份:", years)
        print("取得的營運收入資料:", operating_incomes)

        # Step 1: 使用線性回歸檢查整體斜率
        x = np.arange(len(operating_incomes))
        slope, intercept, _, _, _ = linregress(x, operating_incomes)
        print(f"斜率: {slope:.6f}")

        condition_3_met = False  # 預設未成長
        ttm_growth_message = ""

        if slope > 0:
            # 如果斜率向上，判定成長
            condition_3_met = True
            print("✅ 整體斜率向上，營運收入呈現成長")
        else:
            # Step 2: 如果斜率不向上，檢查 TTM 是否高於最新年度數據的 30%
            ttm_value = operating_incomes[3]  # TTM 值
            latest_annual_value = operating_incomes[2]  # 最新年度數據
            print("anson", ttm_value, latest_annual_value, growth_threshold)
            if ttm_value > latest_annual_value * (1 + growth_threshold):
                condition_3_met = True
                ttm_growth_message = f"TTM 明顯成長 (> {growth_threshold * 100:.0f}%)"
                print(f"✅ TTM 高於最新年度 30%: {ttm_value} > {latest_annual_value * 1.3}")
            else:
                print("❌ TTM 未達到明顯成長標準")

        # # 視覺化結果
        # plt.figure(figsize=(8, 5))
        # plt.plot(x, operating_incomes, 'o-', label='Operating Income')  # 原始數據連線
        
        # # 顯示每個數據點的數值
        # for i, value in enumerate(operating_incomes):
        #     plt.text(x[i], value, f"{value:,.0f}", ha='center', va='bottom', fontsize=8)

        # plt.xticks(x, years, rotation=45)  # x 軸標籤
        # plt.title("Operating Income Trend (3 Years + TTM)")
        # plt.xlabel("Time Series")
        # plt.ylabel("Operating Income (Unit)")
        # plt.legend()
        # plt.grid(True)

        # # 保存圖片
        # output_file = "./operating_income_trend_ttm.png"
        # plt.tight_layout()
        # plt.savefig(output_file)
        # print(f"Plot saved as {output_file}")

        # 顯示結果
        if condition_3_met:
            result_text = f"✅ {f'({ttm_growth_message})' if ttm_growth_message else ''}"
            create_label(right_frame_content, result_text, 2, column=1)
        else:
            create_label(right_frame_content, "❌", 2, column=1)

    except Exception as e:
        print(f"Error in display_condition_3: {e}")
        create_label(right_frame_content, "⚠️ Error", 2, column=1)

def display_condition_4(financials, quarterly_financials, right_frame_content, growth_threshold=0.3):
    create_label(right_frame_content, "條件 4: 淨利正成長 (2 Years + TTM)", 3)

    try:
        # 初始化空列表，用於存放年份和淨利
        net_incomes = []
        years = []

        # 取得最新 3 年的年度數據
        if 'Net Income' in financials.index:
            annual_net_incomes = financials.loc['Net Income'].dropna()
            if len(annual_net_incomes) >= 3:
                latest_annual_data = annual_net_incomes.iloc[:3]  # 取最新 3 年數據
                net_incomes.extend(latest_annual_data.tolist()[::-1])  # 倒序
                years.extend(latest_annual_data.index.tolist()[::-1])  # 年份倒序

        # 計算 TTM 淨利並加入最後
        if 'Net Income' in quarterly_financials.index and len(quarterly_financials.loc['Net Income']) >= 4:
            net_income_ttm = quarterly_financials.loc['Net Income'].iloc[:4].sum()
            print(f"TTM 淨利: {net_income_ttm}")
            net_incomes.append(net_income_ttm)
            years.append("TTM")

        # 確保數據完整（必須有 3 個數據: 2 年年度數據 + TTM）
        if len(net_incomes) != 4:
            print("有效數據不足，無法進行分析")
            create_label(right_frame_content, "⚠️ 數據不足", 4, column=1)
            return

        # 打印數據以供檢查
        print("取得的年份:", years)
        print("取得的淨利資料:", net_incomes)

        # Step 1: 使用線性回歸檢查整體斜率
        x = np.arange(len(net_incomes))
        slope, intercept, _, _, _ = linregress(x, net_incomes)
        print(f"斜率: {slope:.6f}")

        condition_4_met = False  # 預設未成長
        ttm_growth_message = ""

        if slope > 0:
            # 如果斜率向上，判定成長
            condition_4_met = True
            print("✅ 整體斜率向上，淨利呈現成長")
        else:
            # Step 2: 如果斜率不向上，檢查 TTM 是否高於最新年度數據的 30%
            ttm_value = net_incomes[3]  # TTM 值
            latest_annual_value = net_incomes[2]  # 最新年度數據
            print("anson", ttm_value, latest_annual_value, growth_threshold)
            if ttm_value > latest_annual_value * (1 + growth_threshold):
                condition_4_met = True
                ttm_growth_message = f"TTM 明顯成長 (> {growth_threshold * 100:.0f}%)"
                print(f"✅ TTM 高於最新年度 30%: {ttm_value} > {latest_annual_value * 1.3}")
            else:
                print("❌ TTM 未達到明顯成長標準")

        # # 視覺化結果
        # plt.figure(figsize=(8, 5))
        # plt.plot(x, net_incomes, 'o-', label='Net Income')  # 原始數據連線

        # # 顯示每個數據點的數值
        # for i, value in enumerate(net_incomes):
        #     plt.text(x[i], value, f"{value:,.0f}", ha='center', va='bottom', fontsize=8)

        # plt.xticks(x, years, rotation=45)  # x 軸標籤
        # plt.title("Net Income Trend (2 Years + TTM)")
        # plt.xlabel("Time Series")
        # plt.ylabel("Net Income (Unit)")
        # plt.legend()
        # plt.grid(True)

        # # 保存圖片
        # output_file = "./net_income_trend_ttm.png"
        # plt.tight_layout()
        # plt.savefig(output_file)
        # print(f"Plot saved as {output_file}")

        # 顯示結果
        if condition_4_met:
            result_text = f"✅ {f'({ttm_growth_message})' if ttm_growth_message else ''}"
            create_label(right_frame_content, result_text, 3, column=1)
        else:
            create_label(right_frame_content, "❌ ", 3, column=1)

    except Exception as e:
        print(f"Error in display_condition_4: {e}")
        create_label(right_frame_content, "⚠️ Error", 3, column=1)

def display_condition_5(quarterly_balance_sheet, right_frame_content):
    create_label(right_frame_content, "條件 5: 流動資產 TTM > 流動負債 TTM", 4)
    try:
        # 檢查是否可以取得流動資產和流動負債的數據
        if "Current Assets" not in quarterly_balance_sheet.index or "Current Liabilities" not in quarterly_balance_sheet.index:
            create_label(right_frame_content, "⚠️ 數據不足", 4, column=1)
            return

        # 獲取最近四個季度的流動資產和流動負債數據
        current_assets_series = quarterly_balance_sheet.loc["Current Assets"].iloc[:4]
        current_liabilities_series = quarterly_balance_sheet.loc["Current Liabilities"].iloc[:4]

        print("CONDITION_5", current_assets_series, current_liabilities_series)

        # 將 NaN 值填充為 0
        current_assets_series = current_assets_series
        current_liabilities_series = current_liabilities_series

        # 計算最近四個季度的流動資產和流動負債的 TTM 總和
        current_assets_ttm = current_assets_series.sum()
        current_liabilities_ttm = current_liabilities_series.sum()

        # 確保數據不是 NaN 且流動資產 TTM 大於流動負債 TTM
        if pd.notna(current_assets_ttm) and pd.notna(current_liabilities_ttm):
            condition_5_met = current_assets_ttm > current_liabilities_ttm
        else:
            create_label(right_frame_content, "⚠️ 數據不足", 4, column=1)
            return

        # 顯示結果
        create_label(right_frame_content, "✅" if condition_5_met else "❌", 4, column=1)

        # 輸出數據供檢查
        print("CONDITION 5")
        print("Current Assets TTM:", current_assets_ttm)
        print("Current Liabilities TTM:", current_liabilities_ttm)
    except Exception as e:
        print(f"Error in display_condition_5: {e}")
        create_label(right_frame_content, "⚠️ 數據不足", 4, column=1)

def display_condition_6(quarterly_balance_sheet, quarterly_financials, right_frame_content):
    create_label(right_frame_content, "條件 6: 長期負債/淨利 < 4", 5)
    try:
        long_term_debt = quarterly_balance_sheet.loc["Long Term Debt"].iloc[0] if "Long Term Debt" in quarterly_balance_sheet.index else None
        
        # 確保索引是否存在
        if 'Net Income' in quarterly_financials.index:
            net_income_series = quarterly_financials.loc['Net Income'].iloc[:4]
            # 計算最近四個季度的 TTM 淨利潤
            net_income = net_income_series.sum()
        else:
            net_income = None
        
        if long_term_debt is not None and net_income is not None and net_income != 0:
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
        traceback.print_exc()  # 顯示具體的錯誤回溯信息
        create_label(right_frame_content, "❌", 5, column=1)

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

def display_condition_7(annual_balance_sheet, quarterly_balance_sheet, right_frame_content):
    create_label(right_frame_content, "條件 7: 股東權益正成長(Step-by-Step Growth (2 Years + TTM))", 6)

    try:
        # 初始化空列表，用於存放年份和數值
        equity_values = []
        x_values = []

        # 取得最新 2 年的年度數據
        if "Stockholders Equity" in annual_balance_sheet.index:
            stockholders_equity_annual = annual_balance_sheet.loc["Stockholders Equity"].dropna()

            # 確保至少有 2 年的年度數據
            if len(stockholders_equity_annual) >= 2:
                latest_annual_data = stockholders_equity_annual.iloc[:2]  # 取最新 2 年
                equity_values.extend(latest_annual_data.tolist()[::-1])  # 倒序，舊到新
                x_values.extend(latest_annual_data.index.tolist()[::-1])  # 對應年份

        # 計算 TTM
        if "Stockholders Equity" in quarterly_balance_sheet.index:
            stockholders_equity_quarterly = quarterly_balance_sheet.loc["Stockholders Equity"].dropna()

            # 確保至少有 4 季數據
            if len(stockholders_equity_quarterly) >= 4:
                ttm_value = stockholders_equity_quarterly.iloc[:4].sum()  # 最近 4 季加總
                equity_values.append(ttm_value)
                x_values.append("TTM")  # 標記為 TTM

        # 確保數據完整
        if len(equity_values) != 3:
            print("Not enough valid data for analysis.")
            create_label(right_frame_content, "⚠️ Insufficient Data", 6, column=1)
            return

        # 檢查數據是否逐步成長
        condition_7_met = all(equity_values[i] <= equity_values[i + 1] for i in range(len(equity_values) - 1))

        # # 打印檢查結果
        # print("Years/Labels:", x_values)
        # print("Equity Values:", equity_values)
        # print(f"Condition Met (Step-by-Step Growth): {condition_7_met}")

        # # 視覺化結果
        # numerical_x = np.arange(len(equity_values))
        # plt.figure(figsize=(8, 5))
        # plt.plot(numerical_x, equity_values, 'o-', label='Stockholders\' Equity')  # 原始數據連線
        
        # # 顯示數據點的數值標籤
        # for i, value in enumerate(equity_values):
        #     plt.text(numerical_x[i], value, f"{value:,.0f}", ha='center', va='bottom', fontsize=8)

        # plt.xticks(numerical_x, x_values, rotation=45)  # x 軸標籤
        # plt.title("Stockholders' Equity Trend (Latest 2 Years + TTM)")
        # plt.xlabel("Time Series")
        # plt.ylabel("Stockholders' Equity (Unit)")
        # plt.legend()
        # plt.grid(True)

        # # 保存圖片
        # output_file = "./equity_trend_2years_ttm.png"
        # plt.tight_layout()
        # plt.savefig(output_file)
        # print(f"Plot saved as {output_file}")

        # 顯示結果
        if condition_7_met:
            create_label(right_frame_content, "✅", 6, column=1)
            print("✅ Stockholders' Equity shows step-by-step growth.")
        else:
            create_label(right_frame_content, "❌", 6, column=1)
            print("❌ Stockholders' Equity does not show step-by-step growth.")

    except Exception as e:
        print(f"Error in display_condition_7: {e}")
        create_label(right_frame_content, "⚠️", 6, column=1)


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
        print("Operating Cash Flow", operating_cash_flow)
        print("Financing Cash Flow", financing_cash_flow)
        print("Investing Cash Flow", investing_cash_flow)
        condition_9_met = operating_cash_flow > investing_cash_flow and operating_cash_flow > financing_cash_flow
        create_label(right_frame_content, "✅" if condition_9_met else "❌", 8, column=1)
    except Exception:
        create_label(right_frame_content, "❌", 8, column=1)

def display_condition_10(quarterly_cashflow, right_frame_content):
    create_label(right_frame_content, "條件 10: 自由現金流正成長(連續三季)", 9)
    try:
        # 獲取 "Free Cash Flow" 的數據
        if "Free Cash Flow" in quarterly_cashflow.index:
            quarterly_free_cash_flow = quarterly_cashflow.loc["Free Cash Flow"]

            # 確保有至少三個季度的數據進行比較
            if len(quarterly_free_cash_flow) >= 3:
                latest_value = quarterly_free_cash_flow.iloc[0]
                previous_value_1 = quarterly_free_cash_flow.iloc[1]
                previous_value_2 = quarterly_free_cash_flow.iloc[2]

                # 檢查是否有連續三季的正成長
                if pd.notna(latest_value) and pd.notna(previous_value_1) and pd.notna(previous_value_2):
                    condition_10_met = (latest_value > previous_value_1) and (previous_value_1 > previous_value_2)

                    print("CONDITION 10")
                    print("Latest:", latest_value)
                    print("Previous 1:", previous_value_1)
                    print("Previous 2:", previous_value_2)
                    
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
