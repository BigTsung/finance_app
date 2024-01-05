import sys
import twstock
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QDateEdit, QFrame
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtGui import QPainter, QFont
from datetime import datetime
from PyQt5.QtCore import Qt, QDateTime, QDate

class StockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.stockInput = QLineEdit(self)
        self.fetchButton = QPushButton('獲取股票資訊', self)
        self.fetchButton.clicked.connect(self.updateChart)

        self.startDateEdit = QDateEdit(self)
        self.startDateEdit.setDate(QDate.currentDate())
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.dateChanged.connect(self.updateChart)  # 連接 dateChanged 信號


        self.realTimeInfoLabel = QLabel('', self)
        self.yesterdayInfoLabel = QLabel('', self)
        self.infoLabel = QLabel('', self)
        self.chartView = QChartView(self)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chartView.setMinimumHeight(400)
        self.chartView.setMinimumWidth(600)
        self.chartView.setVisible(False)

        # 創建顯示股票資訊的 QLabel
        self.priceLabel = QLabel('成交價: -', self)
        self.yesterdayCloseLabel = QLabel('昨收: -', self)
        self.changePriceLabel = QLabel('漲跌價: -', self)
        self.changePercentLabel = QLabel('漲跌幅: -', self)
        self.amplitudeLabel = QLabel('振幅: -', self)
        self.openPriceLabel = QLabel('開盤: -', self)
        self.highPriceLabel = QLabel('最高: -', self)
        self.lowPriceLabel = QLabel('最低: -')

        self.volumeLabel = QLabel('成交張數: -', self)
        self.amountLabel = QLabel('成交金額: -', self)
        self.transactionCountLabel = QLabel('成交筆數: -', self)
        self.averageVolumeLabel = QLabel('成交均張: -', self)
        self.averagePriceLabel = QLabel('成交均價: -', self)


        layoutMain = QVBoxLayout()
        
        self.addTitleLable(layoutMain,'輸入',16,True)
        # self.addLine(layoutMain)
        layoutMain.addWidget(self.stockInput)
        
        # setting layout
        layoutSetting = QHBoxLayout()
        layoutSetting.addWidget(self.startDateEdit)
        layoutSetting.addWidget(self.fetchButton)
        layoutMain.addLayout(layoutSetting)

        # realtime layout
        self.addTitleLable(layoutMain,'即時資訊',16,True)
        
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layoutMain.addWidget(line)
        layoutTextInfo = QHBoxLayout()
        layoutTextInfo.addWidget(self.realTimeInfoLabel)
        layoutMain.addLayout(layoutTextInfo)

        layoutMain.addSpacing(10)

        # stock layout
        self.addTitleLable(layoutMain,'股票資訊',16,True)
        self.addLine(layoutMain)
        
        layoutStockMain = QHBoxLayout()

        layoutStockLeft = QVBoxLayout()
        layoutStockLeft.addWidget(self.priceLabel)
        layoutStockLeft.addWidget(self.yesterdayCloseLabel)
        layoutStockLeft.addWidget(self.changePriceLabel)
        layoutStockLeft.addWidget(self.changePercentLabel)
        layoutStockLeft.addWidget(self.amplitudeLabel)
        layoutStockLeft.addWidget(self.openPriceLabel)
        layoutStockLeft.addWidget(self.highPriceLabel)
        layoutStockLeft.addWidget(self.lowPriceLabel)
        layoutStockMain.addLayout(layoutStockLeft)

        layoutStockRight = QVBoxLayout()
        layoutStockRight.addWidget(self.volumeLabel)
        layoutStockRight.addWidget(self.amountLabel)
        layoutStockRight.addWidget(self.transactionCountLabel)
        layoutStockRight.addWidget(self.averageVolumeLabel)
        layoutStockRight.addWidget(self.averagePriceLabel)
        layoutStockMain.addLayout(layoutStockRight)
        layoutMain.addLayout(layoutStockMain)

        layoutMain.addSpacing(10)
        
        # chart layout
        self.addTitleLable(layoutMain,'股價走勢圖',16,True)
        self.addLine(layoutMain)
        layoutMain.addWidget(self.chartView)
        
        self.setLayout(layoutMain)
        
        self.setWindowTitle('股票資訊查詢')
        self.setGeometry(300, 300, 600, 100)

    def addLine(self, layout):
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

    def addTitleLable(self, layout, name, fontSize = 12, Bold = False):
        titleLabel = QLabel(name, self)
        font = QFont()
        font.setPointSize(fontSize)  # 設置字體大小
        font.setBold(Bold)     # 設置加粗
        titleLabel.setFont(font)
        layout.addWidget(titleLabel)

    def updateChart(self):
        stock_code = self.stockInput.text()
        if not stock_code:
            self.infoLabel.setText('請輸入股票代碼')
            self.chartView.setVisible(False)  # 沒有數據時不顯示
            return

        self.stock = twstock.Stock(stock_code)
        start_date = self.startDateEdit.date().toPyDate()
        historical_data = self.stock.fetch_from(start_date.year, start_date.month)
        self.showStockChart(historical_data, stock_code)
        self.chartView.setVisible(True)
        self.fetchRealTimeStockInfo()

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

        self.showYesterdayInfo()

    def showYesterdayInfo(self):
        print("stock: ", self.stock)

        # self.priceLabel = QLabel('成交價: -', self)
        # self.yesterdayCloseLabel = QLabel('昨收: -', self)
        # self.changePriceLabel = QLabel('漲跌價: -', self)
        # self.changePercentLabel = QLabel('漲跌幅: -', self)
        # self.amplitudeLabel = QLabel('振幅: -', self)
        # self.openPriceLabel = QLabel('開盤: -', self)
        # self.highPriceLabel = QLabel('最高: -', self)
        # self.lowPriceLabel = QLabel('最低: -')

        # self.volumeLabel = QLabel('成交張數: -', self)
        # self.amountLabel = QLabel('成交金額: -', self)
        # self.transactionCountLabel = QLabel('成交筆數: -', self)
        # self.averageVolumeLabel = QLabel('成交均張: -', self)
        # self.averagePriceLabel = QLabel('成交均價: -', self)



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

        self.volumeLabel.setText(f'成交張數: {round(self.stock.capacity[-1]/1000)}')
        self.amountLabel.setText(f'成交金額: {self.stock.turnover[-1]}')
        self.transactionCountLabel.setText(f'成交筆數: {self.stock.transaction[-1]}')

        # avg_trade_volume = self.stock.moving_average(self.stock.moving_volume, 5)

        self.averageVolumeLabel.setText(f'成交均張: {(self.stock.capacity[-1]/1000/self.stock.transaction[-1]):.1f}張/筆')

        # average_price = self.stock.price[-5:].mean()

        self.averagePriceLabel.setText(f'成交均價: {(self.stock.turnover[-1]/self.stock.capacity[-1]):.1f}元')
        

        # 顯示昨日收盤資訊
        # if self.stock:
        #     self.yesterdayInfoLabel.setText(f'昨日開盤價: {self.stock.open[-1]}\n昨日最高價: {self.stock.high[-1]}\n昨日最低價: {self.stock.low[-1]}\n昨日收盤價: {self.stock.price[-1]}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StockApp()
    ex.show()
    sys.exit(app.exec_())
