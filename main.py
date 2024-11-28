import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from download_operate import 获取目标网页内文件
import pandas as pd
from time import sleep, strftime

def handle_target(form_data):
    url='https://www.bosera.com/column/index.do?classid=00020002000200020002'

    driver = webdriver.Chrome()  # 或 Edge、Firefox 等
    driver.get(url)
    # 等待页面加载完全（可根据目标元素设置条件）
    WebDriverWait(driver, 2)

    driver.find_element(By.NAME, "title").send_keys(form_data["title"])
    driver.find_element(By.NAME, "content").send_keys(form_data["content"])
    driver.find_element(By.NAME, "startDate").clear()
    driver.find_element(By.NAME, "startDate").send_keys(form_data["startDate"].strftime('%Y-%m-%d'))
    driver.find_element(By.NAME, "endDate").clear()
    driver.find_element(By.NAME, "endDate").send_keys(form_data["endDate"].strftime('%Y-%m-%d'))

    # 提交表单
    submit_button = driver.find_element(By.ID, "submit")
    ActionChains(driver).move_to_element(submit_button).click().perform()

    WebDriverWait(driver, 2)

    # 获取页面HTML
    page_source = driver.page_source

    # 关闭浏览器
    driver.quit()

    # 提取页面内容
    html = driver.page_source

    # 转换为 BeautifulSoup 对象
    soup = BeautifulSoup(html, 'html.parser')

    # 打印/处理解析后的数据
    links = soup.find_all(class_='info_link')  # 根据class筛选
    base_url = "https://www.bosera.com/"
    for link in links:
        href = link.get('href')  # 获取链接的href属性
        full_url = urljoin(base_url, href)
        获取目标网页内文件(full_url)

if __name__ == '__main__':

    file_path = "目标.xlsx"
    df = pd.read_excel(file_path)
    data_list = df.to_dict(orient="records")
    for data in data_list:
        handle_target(data)
