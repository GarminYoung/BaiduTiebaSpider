from bs4 import BeautifulSoup
import requests
import random
import time
import pandas as pd
from ua_info import ua_list


# 请求函数
def get_html(url, param):
    # 重构请求头，使用自定义UA标识池
    headers = {'User-Agent': random.choice(ua_list)}
    response = requests.get(url=url, params=param, headers=headers)
    # 每爬取一个页面随机休眠1-2秒钟的时间
    time.sleep(random.randint(1, 2))
    return response


# 解析函数
def parse_html(response):
    # 生成BeautifulSoup对象
    soup = BeautifulSoup(response.text, 'html.parser')
    post_list = soup.find_all("div", {'class': 's_post'})
    lt = []
    for posts in post_list:
        post = {}
        tag = posts.find_all("font", {'class': "p_violet"})
        post['吧名'] = tag[0].get_text()
        post['作者'] = tag[1].get_text()
        post['标题'] = posts.find('a', {'class': "bluelink"}).get_text()
        post['内容'] = posts.find('div', {'class': "p_content"}).get_text()
        # 数据清洗
        if "回复" in post['标题']:
            pass
        elif "转贴" in post['标题']:
            pass
        else:
            # 列表拼接成字典
            lt.append(post)
    return lt


# 保存文件
def save_csv(dic, filename):
    df = pd.DataFrame(dic)
    df.to_csv(filename, index=False)


# 主函数
def run():
    url = 'https://tieba.baidu.com/f/search/res'  # 目标url
    kw = input("请输入吧名")  # 吧名
    content = input("请输入要查询的内容")  # 内容
    page_start = int(input("请输入开始页码"))  # 页码
    page_end = int(input("请输入结束页码")) + 1  # 页码
    filename = input("请输入要存入的文件名（使用csv后缀）")  # 文件名
    lt2 = []  # 新建空列表用于存储数据

    for page in range(page_start, page_end, 1):
        param = {
            'ie': 'utf-8',  # 编码方式
            'kw': kw,  # 吧名
            'qw': content,  # 内容
            'pn': page  # 页码
        }
        res = get_html(url, param)
        lt1 = parse_html(res)
        # 列表拼接
        lt2.extend(lt1)
    save_csv(lt2, filename)


# 异常处理机制
try:
    run()
except Exception as e:
    print("错误:", e)
