# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'digikalaextractor.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
import re
import requests
from bs4 import BeautifulSoup

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(851, 611)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(20, 230, 171, 31))
        self.username.setText("")
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(20, 270, 171, 31))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(60, 320, 88, 27))
        self.run.setObjectName("run")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(210, 10, 621, 461))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.output_general = QtWidgets.QTableWidget(self.tab)
        self.output_general.setGeometry(QtCore.QRect(10, 10, 601, 361))
        self.output_general.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.output_general.setLineWidth(1)
        self.output_general.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.output_general.setShowGrid(True)
        self.output_general.setObjectName("output_general")
        self.output_general.setColumnCount(4)
        self.output_general.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.output_general.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.output_general.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.output_general.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.output_general.setHorizontalHeaderItem(3, item)
        self.output_general.horizontalHeader().setCascadingSectionResizes(False)
        self.output_general.horizontalHeader().setDefaultSectionSize(80)
        self.output_general.horizontalHeader().setMinimumSectionSize(38)
        self.output_general.horizontalHeader().setSortIndicatorShown(False)
        self.output_general.horizontalHeader().setStretchLastSection(True)
        self.output_general.verticalHeader().setCascadingSectionResizes(False)
        self.output_general.verticalHeader().setSortIndicatorShown(False)
        self.output_general.verticalHeader().setStretchLastSection(False)
        self.output_result = QtWidgets.QListWidget(self.tab)
        self.output_result.setGeometry(QtCore.QRect(10, 380, 601, 51))
        self.output_result.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.output_result.setObjectName("output_result")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.log = QtWidgets.QTextBrowser(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(210, 480, 621, 81))
        self.log.setObjectName("log")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.pixmap = QPixmap('./logo.png')
        self.logo.setScaledContents(True)
        self.logo.setPixmap(self.pixmap)
        self.logo.setGeometry(QtCore.QRect(20, 30, 171, 171))
        self.logo.setText("")
        self.logo.setObjectName("logo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 851, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.run.clicked.connect(self.get_data)
        self.password.returnPressed.connect(self.get_data)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_data(self):
        self.log.append('شروع')
        app.processEvents()
        def dkprice_to_numbers(dkprice):
            '''gets something like ۱۱۷،۰۰۰ تومان and returns 117000'''
            convert_dict = {u'۱': '1', u'۲': '2', u'۳': '3', u'۴': '4', u'۵': '5',
                            u'۶': '6', u'۷': '7', u'۸': '8', u'۹': '9', u'۰': '0', }
            price = u'۰' + dkprice
            for k in convert_dict.keys():
                price = re.sub(k, convert_dict[k], price)

            price = re.sub('[^0-9]', '', price)
            return int(price)


        def extract_data(one_page, all_orders):            
            soup = BeautifulSoup(one_page.text, 'html.parser')
            # there might be more than one table
            for this_table in soup.find_all('div', class_='c-table-order__body'):
                for this_item in this_table.find_all('div', class_='c-table-order__row'):
                    name = this_item.find('span').get_text()
                    dknum = this_item.find(
                        'div', class_='c-table-order__cell--value').get_text()
                    num = dkprice_to_numbers(dknum)
                    dkprice = this_item.find(
                        'div', class_='c-table-order__cell--price-final').get_text()
                    price = dkprice_to_numbers(dkprice)
                    date = soup.find('h4').span.get_text()
                    date = re.sub(u'ثبت شده در تاریخ ', '', date)
                    all_orders.append((date, name, num, price))


        url = 'https://www.digikala.com/users/login/'
        payload = {'login[email_phone]': self.username.text(),
                   'login[password]': self.password.text(), 'remember': 1}
        session = requests.session()
        r = session.post(url, data=payload)
        if r.status_code != 200:
            self.log.append('مشکل در اتصال. کد خطا: %s' % r.status_code)
            return False

        successful_login_text = 'سفارش‌های من'
        if re.search(successful_login_text, r.text):
            self.log.append('لاگین موفق')
        else:
            self.log.append('کلمه عبور یا نام کاربری اشتباه است')
            return False

        app.processEvents()
        page_number = 1
        orders = session.get(
            'https://www.digikala.com/profile/orders/?page=%i' % page_number)
        soup = BeautifulSoup(orders.text, 'html.parser')

        all_orders = []  # (list of (date, name, number, item_price))

        while not soup.find('div', class_='c-profile-empty'):
            app.processEvents()
            for this_order in soup.find_all('a', class_='btn-order-more'):
                this_order_link = this_order.get('href')
                print('going to fetch: http://digikala.com'+this_order_link)
                one_page = session.get('http://digikala.com'+this_order_link)
                extract_data(one_page, all_orders)
            self.log.append('بررسی صفحه %i' % page_number)
            page_number += 1
            orders = session.get(
                'https://www.digikala.com/profile/orders/?page=%i' % page_number)
            soup = BeautifulSoup(orders.text, 'html.parser')
            

        self.log.append('پایان')


        total_price = 0
        total_purchase = 0
        full_purchase_list = ''
        n = 0
        self.output_general.setRowCount(len(all_orders))
        
        for date, name, num, price in all_orders:
            this_purchase_str = "تاریخ %s:‌ %s عدد %s, به قیمت هر واحد %s\n" % (
                date, num, name, price)
            full_purchase_list = this_purchase_str + full_purchase_list
            total_price += price
            total_purchase += 1

            self.output_general.setItem(n,0,QTableWidgetItem(str(date)))
            self.output_general.setItem(n,1,QTableWidgetItem(str(num)))
            self.output_general.setItem(n,2,QTableWidgetItem(str(price)))
            self.output_general.setItem(n,3,QTableWidgetItem(str(name)))
            n=n+1
        self.output_result.clear()
        price_item = ['کل خرید شما از دیجی کالا:    {} تومان'.format(total_price)]
        purchase_item = ['تعداد خرید:    {}'.format(total_purchase)]

        self.output_result.addItems(price_item)
        self.output_result.addItems(purchase_item)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "سابقه من در دیجی کالا"))
        self.username.setPlaceholderText(_translate("MainWindow", "Email"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.run.setText(_translate("MainWindow", "اجرا"))
        self.output_general.setSortingEnabled(False)
        item = self.output_general.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "تاریخ"))
        item = self.output_general.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "تعداد"))
        item = self.output_general.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "قیمت"))
        item = self.output_general.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "نام"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "اطلاعات عمومی"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "نمودار خرید"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #app.setLayoutDirection(QtCore.Qt.RightToLeft)
    MainWindow = QtWidgets.QMainWindow()
    app_icon = QIcon('./icon.svg')
    MainWindow.setWindowIcon(app_icon)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

