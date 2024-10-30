# 引入相关模块
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# 引导用户输入时间查询并获取当前时间
# 使用正则表达式提取当前时间的年月日
time1 = re.findall(r'(.{4})-(.{2})-(.{2})', str(datetime.now()))
time = time1[0]  # 当前时间的年月日
time_now = int(time[0] + time[1] + time[2])  # 当前时间的年月日作为整数

# 用户输入开始和结束时间
starttime = input('请输入开始时间（用年月日表示，月，日不过10的前面补0）：')
endtime = input('请输入结束时间（用年月日表示，月，日不过10的前面补0）：')
date_format = "%Y%m%d"  # 日期格式

# 对用户输入的时间进行判断
try:
    stt = int(starttime)
    ett = int(endtime)

    # 检查输入长度是否正确
    if len(starttime) != 8 or len(endtime) != 8:
        print('起始时间和结束时间必须按格式输入')
        exit()

    # 将时间字符串转换为时间戳
    st_object = datetime.strptime(starttime, date_format).timestamp()
    et_object = datetime.strptime(endtime, date_format).timestamp()

    # 验证时间范围
    if stt > ett:
        print('结束时间不得大于开始时间')
        exit()
    elif stt < 20140330 or ett < 20140330:
        print('2014年3月30号MC百科才开始收录模组，你搁这时空穿越呢')
        exit()
    elif stt > time_now or ett > time_now:
        print(f'现在是{time[0]}年{time[1]}月{time[2]}日，你搁这预知未来呢')
        exit()
    elif et_object - st_object > 2592000:  # 大约一个月
        print('最多支持30天的数据查询')
        exit()

except ValueError:
    print('请输入正确的时间格式（YYYYMMDD）')
    exit()
except Exception as ex:
    print(f'未知错误：{ex}')
    exit()

# 获取相关信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

# 发送HTTP请求获取初始页面数据
response = requests.get(f'https://www.mcmod.cn/history.html?starttime={st_object}&endtime={et_object}', headers=headers)

# 检查响应状态
if response.ok:
    summary = []  # 存储爬取的数据

    # 解析HTML
    html = response.text
    search = BeautifulSoup(html, 'html.parser')

    # 找到包含页码信息的元素
    sc = search.find('ul', attrs={'class': 'pagination'})

    # 提取总页数和条目数
    length = sc.find('span')
    lines = int(re.findall(r'(\d+).页', length.string)[0])
    linestr = re.findall(r'(\d+).条', length.string)[0]
    print(f'共{linestr}条')

    # 循环遍历每一页
    for cycle in range(lines):
        # 发送HTTP请求获取每一页的内容
        page = requests.get(f'https://www.mcmod.cn/history.html?starttime={st_object}&endtime={et_object}&page={cycle}',
                            headers=headers).text
        sech = BeautifulSoup(page, 'html.parser')

        # 找到评论列表
        comments = sech.find('div', attrs={'class': 'history-list-frame'}).find('ul').findAll('li')

        # 遍历每条评论
        for comment in comments:
            links = comment.findAll('a')  # 找到链接
            match = re.findall(r'由 (.*) [在|编].* (.*) 中.*?。(.*) ', comment.text)  # 匹配文本中的模式

            # 如果匹配成功
            if match:
                matchest = match[0]
                matches = list(matchest)

                # 添加链接到匹配的结果中
                for link in links:
                    matches.append(link.get('href'))

                # 将数据添加到总结列表
                if matches:
                    summary.append(matches)

        # 打印当前进度
        print(f'已爬取{len(summary)}条数据')

    # 将数据写入JSON文件
    with open(f'{starttime}~{endtime}MC百科编辑数据.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(summary, ensure_ascii=False, indent=4))
else:
    # 如果请求失败，打印状态码
    print(f'请求失败，状态码：{response.status_code}')
