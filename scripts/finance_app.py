import sys
import twstock
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QDateEdit
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtGui import QPainter
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

        layout = QVBoxLayout()
        layoutSet = QHBoxLayout()
        layoutTextInfo = QHBoxLayout()
        layout.addWidget(self.stockInput)
        layoutSet.addWidget(self.startDateEdit)
        layoutSet.addWidget(self.fetchButton)
        layout.addLayout(layoutSet)
        layout.addWidget(self.infoLabel)
        layoutTextInfo.addWidget(self.realTimeInfoLabel)
        layoutTextInfo.addWidget(self.yesterdayInfoLabel)
        layout.addLayout(layoutTextInfo)
        layout.addWidget(self.chartView)

        self.setLayout(layout)
        self.setWindowTitle('股票資訊查詢')
        self.setGeometry(300, 300, 600, 100)

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
        # 顯示昨日收盤資訊
        if self.stock:
            self.yesterdayInfoLabel.setText(f'昨日開盤價: {self.stock.open[-1]}\n昨日最高價: {self.stock.high[-1]}\n昨日最低價: {self.stock.low[-1]}\n昨日收盤價: {self.stock.price[-1]}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StockApp()
    ex.show()
    sys.exit(app.exec_())
