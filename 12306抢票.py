import requests
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
# path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
# #启用无头模式
# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument('--headless')
# # chrome_options.add_argument('--disable-gpu')
#
# brower = webdriver.Chrome(executable_path=path)
# url = 'https://www.12306.cn/index/'
# brower.get(url)
# time.sleep(2)
#
# brower.save_screenshot('.\douban.png')
# time.sleep(3)
# #保存网页代码
# html = brower.page_source
# # with open(r'.\douban.html','w',encoding='utf8') as fp:
# #     fp.write(html)
# brower.quit()
class Qiangpiao():
    def __init__(self):
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'  # 登录界面
        self.initurl = 'https://kyfw.12306.cn/otn/view/index.html' #登陆成功显示的界面
        self.searchurl = 'https://kyfw.12306.cn/otn/leftTicket/init' #选车票的界面
        self.confirm_passenger = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc' #选择乘客界面
        self.brower = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')#初始化无头版谷歌浏览器
        self.from_station = input("出发地")
        self.to_station = input("目的地")
        self.date = input("出发日")
        self.target = input("目标车辆")
        self.name = input("乘客名字，如有多个请用英文逗号分开").split(',')

    def _login(self):
        self.brower.get(self.login_url)  #打开登录界面
        WebDriverWait(self.brower,1000).until(ec.url_to_be(self.initurl))  #显式等待跳转到登陆成功的界面
        print("登录成功")
    def _tickle(self):
        self.brower.get(self.searchurl) #跳转到选票的界面
        WebDriverWait(self.brower, 1000).until\
            (ec.text_to_be_present_in_element_value((By.ID,'fromStationText'),
                  self.from_station))     #显式等待输入出发站
        WebDriverWait(self.brower, 1000).until \
            (ec.text_to_be_present_in_element_value((By.ID, 'train_date'),
                  self.date))          #显式等待输入出发时间
        WebDriverWait(self.brower, 1000).until \
            (ec.text_to_be_present_in_element_value((By.ID, 'toStationText'),
                                                    self.to_station)) #显式等待输入到达站
        WebDriverWait(self.brower, 1000).until \
            (ec.element_to_be_clickable((By.ID,"query_ticket")))  #显式等待查询按钮能被点击
        searchBt = self.brower.find_element_by_id("query_ticket")  #按钮能被点击，找到查询按钮
        searchBt.click()  #点击查询操作
        WebDriverWait(self.brower, 1000).until \
            (ec.presence_of_element_located((By.XPATH,'//tbody[@id="queryLeftTable"]//tr')))  #显式等待所有列车信息被加载
        tr = self.brower.find_elements_by_xpath('//tbody[@id="queryLeftTable"]//tr[not(@datatran)]')#获取所有的车次的tr
        for t in tr:
            train = t.find_element_by_class_name("number").text #获取车次的名称，注意用t
            if train in self.target: #目标车次在列表中
                have = t.find_element_by_xpath(".//td[4]").text  #查询是否有目标票，注意用t
                if have == "有" or have.isdigit:
                    clickBt = t.find_element_by_class_name("btn72")  #找到查询按钮，注意用t
                    clickBt.click()    #点击
                    WebDriverWait(self.brower, 1000).until(ec.url_to_be(self.confirm_passenger))  #等待跳转到乘客选择界面
                    WebDriverWait(self.brower, 1000).until \
                        (ec.presence_of_element_located((By.XPATH,'.//ul[@id="normal_passenger_id"]/li'))) #等待乘客信息被加载出来
                    passengers_label = self.brower.find_elements_by_xpath('.//ul[@id="normal_passenger_id"]/li/label') #加载出来之后获取乘车人列表
                    for passenger_label in passengers_label: #遍历乘车人列表
                        pa = passenger_label.text  #获取乘车人姓名
                        if pa in self.name:   #如果乘车人姓名在输入的列表中
                            passenger_label.click()  #勾选该乘车人
                            WebDriverWait(self.brower, 1000).until \
                                (ec.presence_of_element_located((By.ID, "dialog_xsertcj")))  #若是学生票等待弹出确认窗口
                            cancel = self.brower.find_element_by_id("dialog_xsertcj_cancel")  #这里选择不购买学生票
                            cancel.click()  # 点击取消按钮   #注意：成人票没有该窗口
                    commit = self.brower.find_element_by_id("submitOrder_id")  # 找到下方的提交订单按钮
                    commit.click()  #点击提交
                    WebDriverWait(self.brower, 1000).until \
                        (ec.presence_of_element_located((By.CLASS_NAME, 'dhtmlx_window_active'))) #等待最后的确认信息弹窗
                    WebDriverWait(self.brower, 1000).until \
                        (ec.element_to_be_clickable((By.ID, 'qr_submit_id')))  #等待确认按钮可以点击
                    yes = self.brower.find_element_by_id('qr_submit_id')    #找到确认按钮
                    yes.click()  #点击
                    try:
                        while yes:  #重复点击几次
                            yes.click()
                            yes = self.brower.find_element_by_id('qr_submit_id')
                    except:
                        print("结束")
                    return

    def run(self):
        self._login()
        self._tickle()
if __name__ == "__main__":
    spider = Qiangpiao()
    spider.run()








































