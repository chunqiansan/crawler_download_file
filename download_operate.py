import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def downlad(url,filename):
    r = requests.get(url, stream=True)#流式下载
    filename = "./下载文件/"+filename
    with open(filename, "wb") as f:
        for bl in r.iter_content(chunk_size=1024):
            if bl:
                f.write(bl)

def 获取目标网页内文件(url):
    # 发起GET请求获取网页内容
    response = requests.get(url)
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找符合条件的标签
        links = soup.find_all(class_='info_link')  # 根据class筛选
        base_url = "https://www.bosera.com/"
        for link in links:
            href = link.get('href')  # 获取链接的href属性
            full_url = urljoin(base_url, href)
            file_name = link.text.strip()
            downlad(url = full_url,filename=file_name)
    else:
        print(f"无法访问网页，状态码：{response.status_code}")

if __name__ == '__main__':
    url = "https://www.bosera.com/column/infoDetail.do?infoid=2962373&classid=00020002000200020002"
    获取目标网页内文件(url)
    
