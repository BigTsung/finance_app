import sys
import twstock
import pandas as pd
import urllib.request

from twstock import BestFourPoint
from twstock import Stock
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QDateEdit, QFrame
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtGui import QPainter, QFont
from datetime import datetime
from PyQt5.QtCore import Qt, QDateTime, QDate


class StockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.stock_code = ''  # 初始化 stock_code 為空字串

    def initUI(self):

        # layout init
        layoutMain = QVBoxLayout(self)
        layoutSingleStockInfo = QHBoxLayout(self)
        layoutStockInfo = QVBoxLayout(self)
        layoutStockChart = QVBoxLayout(self)
        layoutLooking = QVBoxLayout(self)

        # input layout setting
        inputLayout = self.inputUISetting()
        layoutStockInfo.addLayout(inputLayout)
        
        # stock info layout
        self.stockInfoLayout = self.stockInfoSetting()
        self.setLayoutVisible(self.stockInfoLayout, False)
        layoutStockInfo.addLayout(self.stockInfoLayout)

        layoutSingleStockInfo.addLayout(layoutStockInfo)
        
        # chart layout
        self.stockChartLayout = self.stockChartSetting()
        self.setLayoutVisible(self.stockChartLayout, False)
        layoutStockChart.addLayout(self.stockChartLayout)
        
        layoutSingleStockInfo.addLayout(layoutStockChart)

         # network light layout 
        self.networkCheckingLayout = self.networkChecking()
        # self.setLayoutVisible(self.networkCheckingLayout, False)
        layoutSingleStockInfo.addLayout(self.networkCheckingLayout)

        layoutMain.addLayout(layoutSingleStockInfo)    

        # 新增的功能佈局
        # self.lookingLayout = self.lookingSetting()
        # layoutMain.addLayout(self.lookingLayout)

        # main layout init
        self.setLayout(layoutMain)
        self.setWindowTitle('股票資訊查詢')
        self.setGeometry(300, 300, 600, 100)

    # UI Setting
    def networkChecking(self):
        self.networkStatusLabel = QLabel(self)
        self.networkStatusLabel.setFixedSize(20, 20)  # 設置燈號的大小
        self.networkStatusLabel.setStyleSheet(
            "QLabel { background-color: red; border-radius: 10px; }"  # 初始設為紅色圓形
        )
         # self.networkStatusLabel.setAlignment(Qt.AlignRight | Qt.AlignTop)

        layoutV = QVBoxLayout()

        layoutV.addWidget(self.networkStatusLabel, 0, Qt.AlignRight | Qt.AlignTop)
        return layoutV

    def stockChartSetting(self):
        print("stockChartSetting")
        self.chartView = QChartView()
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chartView.setMinimumHeight(400)
        self.chartView.setMinimumWidth(600)
        self.chartView.setVisible(True)

        layoutV = QVBoxLayout()
        
        title_label = self.addTitleLable(layoutV, '股價走勢圖', 16, True)
        self.addLine(layoutV)
        layoutV.addWidget(self.chartView, 0, Qt.AlignRight | Qt.AlignTop)

        # 設置標籤的寬度
        title_label.setFixedWidth(200)  # 可以調整寬度使其與「輸入代號」對齊

        return layoutV

    def stockInfoSetting(self):
        print("StockInfoSetting")
        self.realTimeInfoLabel = QLabel('', self)
        # self.yesterdayInfoLabel = QLabel('', self)
        self.infoLabel = QLabel('', self)

        # 創建顯示股票資訊的 QLabel
        self.priceLabel = QLabel('成交價: -', self)
        self.yesterdayCloseLabel = QLabel('昨收: -', self)
        self.changePriceLabel = QLabel('漲跌價: -', self)
        self.changePercentLabel = QLabel('漲跌幅: -', self)
        self.amplitudeLabel = QLabel('振幅: -', self)
        self.openPriceLabel = QLabel('開盤: -', self)
        self.highPriceLabel = QLabel('最高: -', self)
        self.lowPriceLabel = QLabel('最低: -')
        self.continuousLabel = QLabel('持續上升天數: -', self)
        self.average5daysPriceLabel = QLabel('5日均價: -', self)
        self.average5daysCapacityLabel = QLabel('5日均量: -', self)

        self.volumeLabel = QLabel('成交張數: -', self)
        self.amountLabel = QLabel('成交金額: -', self)
        self.transactionCountLabel = QLabel('成交筆數: -', self)
        self.averageVolumeLabel = QLabel('成交均張: -', self)
        self.averagePriceLabel = QLabel('成交均價: -', self)

        self.kValueLabel = QLabel('K值: -', self)
        self.dValueLabel = QLabel('D值: -', self)
        self.epsLabel = QLabel('EPS: -', self)


        self.bestBuyLabel1 = QLabel('量大收紅', self)
        self.bestBuyLabel2 = QLabel('量縮價不跌', self)
        self.bestBuyLabel3 = QLabel('三日均價由下往上', self)
        self.bestBuyLabel4 = QLabel('三日均價大於六日均價', self)

        self.bestSellLabel1 = QLabel('量大收黑', self)
        self.bestSellLabel2 = QLabel('量縮價跌', self)
        self.bestSellLabel3 = QLabel('三日均價由上往下', self)
        self.bestSellLabel4 = QLabel('三日均價小於六日均價', self)

        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        layoutStockLeft = QVBoxLayout()
        layoutStockRight = QVBoxLayout()
        layoutStockBest = QVBoxLayout()

        self.addTitleLable(layoutV,'股票資訊',16,True)
        self.addLine(layoutV)

        # add real time stock info
        layoutV.addWidget(self.realTimeInfoLabel)
        

        # add stock info
        layoutStockLeft.addWidget(self.priceLabel)
        layoutStockLeft.addWidget(self.yesterdayCloseLabel)
        layoutStockLeft.addWidget(self.changePriceLabel)
        layoutStockLeft.addWidget(self.changePercentLabel)
        layoutStockLeft.addWidget(self.amplitudeLabel)
        layoutStockLeft.addWidget(self.openPriceLabel)
        layoutStockLeft.addWidget(self.highPriceLabel)
        layoutStockLeft.addWidget(self.lowPriceLabel)
        layoutStockLeft.addWidget(self.continuousLabel)
        layoutStockLeft.addWidget(self.average5daysPriceLabel)
        layoutStockLeft.addWidget(self.average5daysCapacityLabel)
        
        layoutH.addLayout(layoutStockLeft)

        # add stock info
        layoutStockRight.addWidget(self.volumeLabel)
        layoutStockRight.addWidget(self.amountLabel)
        layoutStockRight.addWidget(self.transactionCountLabel)
        layoutStockRight.addWidget(self.averageVolumeLabel)
        layoutStockRight.addWidget(self.averagePriceLabel)
        layoutStockRight.addWidget(self.kValueLabel)
        layoutStockRight.addWidget(self.dValueLabel)
        layoutStockRight.addWidget(self.epsLabel)
        layoutH.addLayout(layoutStockRight)

        # add stock info
        layoutStockBest.addWidget(self.bestBuyLabel1)
        layoutStockBest.addWidget(self.bestBuyLabel2)
        layoutStockBest.addWidget(self.bestBuyLabel3)
        layoutStockBest.addWidget(self.bestBuyLabel4)
        layoutStockBest.addWidget(self.bestSellLabel1)
        layoutStockBest.addWidget(self.bestSellLabel2)
        layoutStockBest.addWidget(self.bestSellLabel3)
        layoutStockBest.addWidget(self.bestSellLabel4)
        layoutH.addLayout(layoutStockBest)


        layoutV.addLayout(layoutH)

        return layoutV

    def inputUISetting(self):
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        
        title_label = self.addTitleLable(layoutV, '輸入代號', 16, True)
        self.addLine(layoutV)

        self.stockInput = QLineEdit()
        fetchButton = QPushButton('獲取股票資訊')
        fetchButton.clicked.connect(self.updateChart)

        layoutH.addWidget(self.stockInput)
        layoutH.addWidget(fetchButton)

        layoutV.addLayout(layoutH)

        # 設置標籤和輸入框的寬度
        title_label.setFixedWidth(200)  # 可以調整寬度使其與「股價走勢圖」對齊
        self.stockInput.setFixedWidth(200)  # 可以調整寬度使其與「股價走勢圖」對齊

        return layoutV

    # 新增功能的佈局設置
    # def lookingSetting(self):
    #     layoutV = QVBoxLayout()

    #     self.addTitleLable(layoutV, 'new function', 16, True)
    #     self.addLine(layoutV)

    #     # 可以在這裡添加新的控件，例如按鈕、標籤等
    #     newFunctionButton = QPushButton('new function')
    #     layoutV.addWidget(newFunctionButton)

    #     return layoutV


    def setLayoutVisible(self, layout, visible):
        for i in range(layout.count()):
            layoutItem = layout.itemAt(i)

            # 檢查這是一個佈局還是一個小部件
            if layoutItem.widget() is not None:
                widget = layoutItem.widget()
                widget.setVisible(visible)
            elif layoutItem.layout() is not None:
                self.setLayoutVisible(layoutItem.layout(), visible)  # 遞迴調用

    def addLine(self, layout):
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line, 0, Qt.AlignTop)

    def addTitleLable(self, layout, name, fontSize=12, Bold=False):
        titleLabel = QLabel(name, self)
        font = QFont()
        font.setPointSize(fontSize)  # 設置字體大小
        font.setBold(Bold)  # 設置加粗
        titleLabel.setFont(font)
        layout.addWidget(titleLabel, 0, Qt.AlignLeft | Qt.AlignTop)
        return titleLabel  # 返回標籤對象

    def updateNetworkStatus(self, isConnected):
        if isConnected:
            self.networkStatusLabel.setStyleSheet(
                "QLabel { background-color: green; border-radius: 10px; }"
            )
        else:
            self.networkStatusLabel.setStyleSheet(
                "QLabel { background-color: red; border-radius: 10px; }"
            )

    def updateAnalysics(self):
        # self.stock.con
        analytics_result = Stock(self.stock)
        print(analytics_result)

    def updateBestLabels(self):
        bfp = BestFourPoint(self.stock)
        
        self.updateLabel(self.bestBuyLabel1, bfp.best_buy_1(), special=True)
        self.updateLabel(self.bestBuyLabel2, bfp.best_buy_2())
        self.updateLabel(self.bestBuyLabel3, bfp.best_buy_3())
        self.updateLabel(self.bestBuyLabel4, bfp.best_buy_4())

        self.updateLabel(self.bestSellLabel1, bfp.best_sell_1(), special=False)
        self.updateLabel(self.bestSellLabel2, bfp.best_sell_2())
        self.updateLabel(self.bestSellLabel3, bfp.best_sell_3())
        self.updateLabel(self.bestSellLabel4, bfp.best_sell_4())

    def updateLabel(self, label, value, special=False):
        if value:
            if special:
                label.setStyleSheet("QLabel { background-color : red; color : white; }")
            else:
                label.setStyleSheet("QLabel { background-color : orange; color : white; }")
        else:
            label.setStyleSheet("QLabel { background-color : gray; color : white; }")


    def updateChart(self):
        new_stock_code = self.stockInput.text()
        if new_stock_code == self.stock_code:
            print("just check")
            return  # 如果新輸入的股票代號與原本的相同，什麼都不做
        self.stock_code = new_stock_code  # 更新 stock_code 為新的輸入值
        
        if not self.stock_code:
            self.infoLabel.setText('請輸入股票代碼')
            # self.chartView.setVisible(False)  # 沒有數據時不顯示
            return

        self.stock = twstock.Stock(self.stock_code)
        # test
        # print(self.stock.price)
        # print(self.stock.continuous(self.stock.price))
        # print(self.stock.moving_average(self.stock.price, 5))

        # start_date = self.startDateEdit.date().toPyDate() #使用者輸入
        start_date = datetime.now().date()  # 這行將日期設置為程式執行時的日期
        self.historical_data = self.stock.fetch_from(start_date.year, start_date.month)
        self.showStockChart(self.historical_data, self.stock_code)
        # self.chartView.setVisible(True)
        
        self.fetchRealTimeStockInfo()
        self.showStockInfo()

        # # 創建 DataFrame
        # df = pd.DataFrame(historical_data)
        # df.columns = ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction']

        # # 計算 KD 值
        # kd_values = self.calculate_KD(df, n=9)
        # print(kd_values.tail(1))

        self.setLayoutVisible(self.stockInfoLayout, True)
        self.setLayoutVisible(self.stockChartLayout, True)

        self.updateBestLabels()
        # self.updateAnalysics()

    def get_eps_from_brokerage(self, stock_code):
        api_url = f'https://api.brokerage.com/v1/stock/{stock_code}/financials'
        headers = {
            'Authorization': 'Bearer YOUR_API_KEY'
        }
        response = requests.get(api_url, headers=headers)
        data = response.json()

        if 'EPS' in data:
            return data['EPS']
        return None

    # def get_eps(self, stock_code):
    #     stock = yf.Ticker(stock_code)
    #     financials = stock.financials
    #     balance_sheet = stock.balance_sheet

    #     try:
    #         # 获取净利润
    #         net_income = financials.loc['Net Income'].values[0]
    #         # 获取流通股数
    #         shares_outstanding = balance_sheet.loc['Common Stock'].values[0]

    #         # 计算 EPS
    #         eps = net_income / shares_outstanding
    #         return eps
    #     except KeyError as e:
    #         print(f"Key error: {e}")
    #         return None
    #     except Exception as e:
    #         print(f"Error fetching data for {stock_code}: {e}")
            # return None

    # def get_eps_from_mops(self, stock_code, year, season):
    #     url = f'https://mops.twse.com.tw/mops/web/t05st22_q1?co_id={stock_code}&year={year}&season={season}'
    #     response = requests.get(url)
    #     response.encoding = 'utf-8'

    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     tables = soup.find_all('table')

    #     for table in tables:
    #         if '基本每股盈餘（元）' in table.text:
    #             rows = table.find_all('tr')
    #             for row in rows:
    #                 cells = row.find_all('td')
    #                 if len(cells) > 1 and '基本每股盈餘（元）' in cells[0].text:
    #                     eps = cells[1].text.strip()
    #                     return eps

    #     return None

    # def get_eps_from_mops(self, stock_code):
    #     url = f'https://mops.twse.com.tw/mops/web/t05st22_q1?co_id={stock_code}&year=2023&season=01'
    #     response = requests.get(url)
    #     response.encoding = 'utf-8'

    #     print("URL:", url)

    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     tables = soup.find_all('table')
        
    #     for table in tables:
    #         if '每股盈餘(EPS)單位：元' in table.text:
    #             rows = table.find_all('tr')
    #             for row in rows:
    #                 cells = row.find_all('td')
    #                 if len(cells) > 1 and '基本每股盈餘（元）' in cells[0].text:
    #                     eps = cells[1].text.strip()
    #                     return eps

    #     return None

    # get EPS by Yahoo Finance
    # def get_eps(self, stock_code):
    #     stock = yf.Ticker(stock_code)
    #     print("stock code:", stock_code)
    #     try:
    #         financials = stock.financials
    #         balance_sheet = stock.balance_sheet

    #         if 'Net Income' not in financials.index or 'Common Stock' not in balance_sheet.index:
    #             raise ValueError("Required financial data not available")

    #         net_income = financials.loc['Net Income'][0]
    #         shares_outstanding = balance_sheet.loc['Common Stock'][0]
    #         eps = net_income / shares_outstanding
    #         return eps
    #     except Exception as e:
    #         print(f"Error fetching EPS for {stock_code}: {e}")
    #         return None

    # 計算 KD 值的函數
    def calculate_KD(self, data, n=9):
        low_min = data['low'].rolling(window=n, min_periods=1).min()
        high_max = data['high'].rolling(window=n, min_periods=1).max()

        rsv = ((data['close'] - low_min) / (high_max - low_min)) * 100
        data['K'] = rsv.ewm(com=2).mean()
        data['D'] = data['K'].ewm(com=2).mean()

        return data[['date', 'K', 'D']]


    def showStockChart(self, historical_data, stock_code):
        series = QLineSeries()
        for data in historical_data:
            date = QDateTime(datetime(data.date.year, data.date.month, data.date.day))
            series.append(date.toMSecsSinceEpoch(), data.close)

        chart = QChart()
        chart.addSeries(series)

        axisX = QDateTimeAxis()
        axisX.setFormat("MM-dd")
        axisX.setTitleText("日期")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("股價 (TWD)")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chart.setTitle(f'{stock_code} 股價走勢')

        self.chartView.setChart(chart)

    def fetchRealTimeStockInfo(self):
        stock_code = self.stockInput.text()
        self.stock = twstock.Stock(stock_code)  # 儲存股票實例以便後續使用
        real_time_data = twstock.realtime.get(stock_code)
        
        if real_time_data['success']:
            info = real_time_data['info']
            real_price = real_time_data['realtime']['latest_trade_price']

            if real_price and real_price != '-':
                price_text = f'即時價格: {real_price}'
            else:
                # 當 real_price 是 "-"，對齊顯示最佳五檔的買賣價格
                best_bid_price = real_time_data['realtime']['best_bid_price']
                best_ask_price = real_time_data['realtime']['best_ask_price']
                indent = ' ' * (len('即時價格: 買價: ') - len('賣價: '))
                price_text = f'即時價格: 買價: {best_bid_price}\n{indent}賣價: {best_ask_price}'

            self.realTimeInfoLabel.setText(f'股票名稱: {info["name"]}\n股票代號: {info["code"]}\n{price_text}')
        else:
            self.realTimeInfoLabel.setText('無法獲取即時資訊')

       

    def showStockInfo(self):

        self.priceLabel.setText(f'成交價: {self.stock.price[-1]}')
        self.yesterdayCloseLabel.setText(f'昨收: {self.stock.close[-1]}')
        self.changePriceLabel.setText(f'漲跌價: {self.stock.change[-1]}')

        # 獲取最近兩天的收盤價
        latest_prices = self.stock.price[-2:]

        # 計算漲跌價和漲跌幅
        if len(latest_prices) == 2:
            change = latest_prices[1] - latest_prices[0]
            change_percentage = (change / latest_prices[0]) * 100
        self.changePercentLabel.setText(f"漲跌幅: {change_percentage:.2f}%")
        high_price = self.stock.high[-1]
        low_price = self.stock.low[-1]
        amplitude = (high_price - low_price) / low_price * 100

        self.amplitudeLabel.setText(f'振幅: {amplitude:.2f}%')

        self.openPriceLabel.setText(f'開盤: {self.stock.open[-1]}')
        self.highPriceLabel.setText(f'最高: {self.stock.high[-1]}')
        self.lowPriceLabel.setText(f'最低: {self.stock.low[-1]}')
        self.continuousLabel.setText(f'持續上升天數: {self.stock.continuous(self.stock.price)}')
        self.average5daysPriceLabel.setText(f'5日均價: {self.stock.moving_average(self.stock.price,5)[-1]}')
        self.average5daysCapacityLabel.setText(f'5日均量: {self.stock.moving_average(self.stock.capacity,5)[-1]}')
        
        self.volumeLabel.setText(f'成交張數: {round(self.stock.capacity[-1]/1000)}')

        turnover_in_billion = self.stock.turnover[-1] / 1e8
        formatted_turnover = f'{turnover_in_billion:.2f}億'
        self.amountLabel.setText(f'成交金額: {formatted_turnover}')
        

        self.transactionCountLabel.setText(f'成交筆數: {self.stock.transaction[-1]}')
        self.averageVolumeLabel.setText(f'成交均張: {(self.stock.capacity[-1]/1000/self.stock.transaction[-1]):.1f}張/筆')
        self.averagePriceLabel.setText(f'成交均價: {(self.stock.turnover[-1]/self.stock.capacity[-1]):.1f}元')
        
        # 創建 DataFrame
        df = pd.DataFrame(self.historical_data)
        df.columns = ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction']

        # 計算 KD 值
        kd_values = self.calculate_KD(df, n=9)
        # print(kd_values)
        latest_kd = kd_values.tail(1)

        # 獲取 K 和 D 值
        latest_K = latest_kd['K'].iloc[0]
        latest_D = latest_kd['D'].iloc[0]

        self.kValueLabel.setText(f'K值: {latest_K:.1f}')
        self.dValueLabel.setText(f'D值: {latest_D:.1f}')

        
        # eps = self.get_eps(self.stock_code)
        # eps = self.get_eps_from_mops(self.stock_code, 2024, 1)
        # eps = self.get_eps_from_brokerage(self.stock_code)
        # eps = self.get_eps(self.stock_code)
        
        eps=""
        print("EPS:", eps)
        # self.epsLabel.setText(f'D值: {eps:.1f}')

        # 顯示昨日收盤資訊
        # if self.stock:
        #     self.yesterdayInfoLabel.setText(f'昨日開盤價: {self.stock.open[-1]}\n昨日最高價: {self.stock.high[-1]}\n昨日最低價: {self.stock.low[-1]}\n昨日收盤價: {self.stock.price[-1]}')

def checkInternetConnection():
    try:
        # 嘗試訪問 Google
        urllib.request.urlopen('http://www.google.com', timeout=2)
        return True
    except urllib.error.URLError:
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StockApp()
    ex.show()
    isConnected = checkInternetConnection()
    ex.updateNetworkStatus(isConnected)
    sys.exit(app.exec_())
