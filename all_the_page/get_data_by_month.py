# 引入相关模块
import json
import os

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def main():
    # 引导用户输入开始和结束年/月份并获取当前年份
    starttime = input('请输入开始年/月份（格式YYYYMM）：')
    endtime = input('请输入结束年/月份（格式YYYYMM）：')
    date_format = "%Y%m%d"  # 日期格式

    # 对用户输入的年份进行判断
    try:
        stt = int(starttime)
        ett = int(endtime)

        # 检查输入长度是否正确
        if len(starttime) != 6 or len(endtime) != 6:
            print('起始年份和结束年份必须按格式输入（YYYYMM）')
            return 'exit'

        # 将年/月份转换为对应日期的时间戳
        st_object = int(datetime.strptime(str(stt * 100 + 1), date_format).timestamp())
        et_object = int(datetime.strptime(str(ett * 100 + 1), date_format).timestamp())

        # 验证日期范围
        if stt > ett:
            print('结束年份不得大于开始年份')
            return 'exit'
        elif stt < 201404 or ett < 201404:
            print('2014年3月30号MC百科才开始收录模组，你搁这时空穿越呢')
            return 'exit'
        elif et_object - st_object < 2592000:  # 一个月大约2592000秒
            print('最小一月')
            return 'exit'

    except ValueError:
        print('请输入正确的年份格式（YYYYMM）')
        return 'exit'
    except Exception as ex:
        print(f'未知错误：{ex}')
        return 'exit'

    # 获取相关信息
    monthly_info = []  # 存储每月的信息列表

    # 设置HTTP头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
    all_info = {}
    # 循环获取每个月的数据
    for end in range(st_object, et_object, 2592000):
        # 发送HTTP请求
        response = requests.get(f'https://www.mcmod.cn/history.html?starttime={end}&endtime={end + 2592000}',
                                headers=headers)

        # 检查响应状态
        if response.ok:
            html = response.text  # 获取网页内容
            search = BeautifulSoup(html, 'html.parser')  # 解析HTML

            # 查找包含页码信息的元素
            sc = search.find('ul', attrs={'class': 'pagination'})

            # 提取总条目数
            length = sc.find('span')
            linestr = re.findall(r'(\d+).条', length.string)[0]

            # 计算实际开始和结束日期
            starttime_final = str(datetime.fromtimestamp(end))[0:10]
            endtime_final = str(datetime.fromtimestamp(end + 2592000))[0:10]

            # 添加汇总信息到列表
            summary = [f'{starttime_final}~{endtime_final}', linestr]
            monthly_info.append(summary)

            # 打印汇总信息
            print(f'时间段：{summary[0]}，编辑次数：{summary[1]}')

        else:
            # 如果请求失败，打印状态码
            print(f'请求失败，状态码：{response.status_code}')
    all_info['type'] = 'monthly'
    all_info['start_time'] = starttime
    all_info['end_time'] = endtime
    all_info['edition'] = monthly_info
    file_name = f'{starttime}~{endtime}MC百科编辑数据.json'
    # 如果 data 文件夹不存在，则创建它
    if not os.path.exists('data'):
        os.makedirs('data')

    # 构建完整的文件路径
    file_path = os.path.join('data', file_name)
    # 将编辑数据写入JSON文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(all_info, ensure_ascii=False, indent=4))
    return file_path

if __name__ == '__main__':
    main()
