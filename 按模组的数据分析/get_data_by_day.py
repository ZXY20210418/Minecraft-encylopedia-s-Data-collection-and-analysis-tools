from mods import Mods  # 导入自定义的Mods模块
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os

def main():
    while True:
        # 创建一个Mods类的实例，并获取用户输入的模组名称
        mod = Mods(input('请输入您要查询的模组名称（打全名）：'))
        code = mod.get_mod_info()  # 调用get_mod_info方法获取模组信息
        if code == 'exit':
            return 'exit'
        # 获取当前时间并转换为字符串格式
        time = re.findall(r'(.{4})-(.{2})-(.{2})', str(datetime.now()))[0]
        time_now = time[0] + time[1] + time[2]
        time_now_stamp = int(datetime.strptime(time_now, '%Y%m%d').timestamp())  # 当前时间戳

        # 获取模组开始收录的时间戳
        edition_start_time_list = re.findall(r'(.{4})-(.{2})-(.{2})', mod.datetime)[0]
        edition_start_time = edition_start_time_list[0] + edition_start_time_list[1] + edition_start_time_list[2]
        edition_start_time_stamp = int(datetime.strptime(edition_start_time, '%Y%m%d').timestamp())

        try:
            # 用户输入开始和结束的时间（格式为YYYYMMDD）
            start_time = input('请输入开始时间（用年月日表示，月，日不过10的前面补0）：')
            end_time = input('请输入结束时间（用年月日表示，月，日不过10的前面补0）：')
            date_format = "%Y%m%d"  # 时间格式

            # 验证输入的时间长度是否符合要求
            if len(start_time) != 8 or len(end_time) != 8:
                print('起始时间和结束时间必须按格式输入')
                exit()

            # 将时间字符串转换为时间戳
            st_object = int(datetime.strptime(start_time, date_format).timestamp())
            et_object = int(datetime.strptime(end_time, date_format).timestamp())

            # 验证时间范围是否合理
            if st_object > et_object:
                print('结束时间不得大于开始时间')
            elif st_object < edition_start_time_stamp or et_object < edition_start_time_stamp:
                print(f'{edition_start_time_list[0]}年{edition_start_time_list[1]}月{edition_start_time_list[2]}号MC'
                      f'百科才开始收录模组{mod.name}，你搁这时空穿越呢')
            elif st_object > time_now_stamp or et_object > time_now_stamp:
                print(f'现在是{time[0]}年{time[1]}月{time[2]}日，你搁这预知未来呢')
            elif et_object - st_object > 2592000:  # 大约30天
                print('最多支持30天的数据查询')
            else:
                break

        except ValueError:
            # 如果输入的时间格式不正确
            print('请输入正确的时间格式（YYYYMMDD）')
        except Exception as ex:
            # 如果发生其他未知错误
            print(f'未知错误：{ex}')

    # 构造请求URL
    response = requests.get(f'{mod.edition_link}?starttime={st_object}&endtime={et_object}', headers=mod.headers)
    if response.ok:
        summary = []  # 初始化编辑记录列表
        all_info = {}  # 用于存储头部信息

        # 解析HTML内容
        html = response.text
        search = BeautifulSoup(html, 'lxml')

        try:
            # 尝试获取分页信息
            sc = search.find('ul', attrs={'class': 'pagination'})
            length = sc.find('span')
            lines = int(re.findall(r'(\d+).页', length.string)[0])
            linestr = re.findall(r'(\d+).条', length.string)[0]
            print(f'共{linestr}条')
        except AttributeError:
            # 如果没有分页信息，则获取所有历史记录
            comments = search.select('div.history-list-frame li')
            for comment in comments:
                links = comment.findAll('a')  # 查找所有的链接
                match = re.findall(r'由 (.*) [在|编].*。(.*) ', comment.text)  # 匹配编辑者和内容
                if match:
                    matchest = match[0]
                    matches = list(matchest)
                    for link in links:
                        matches.append(link.get('href'))  # 添加每个链接的href属性
                    if matches:
                        summary.append(matches)  # 添加到总结列表

        else:
            # 如果有分页信息，则循环遍历每一页
            for cycle in range(lines):
                page = requests.get(f'{mod.edition_link}?starttime={st_object}&endtime={et_object}&page={cycle}', headers=mod.headers)
                sech = BeautifulSoup(page.text, 'lxml')
                comments = sech.select('div.history-list-frame li')
                for comment in comments:
                    links = comment.findAll('a')  # 查找所有的链接
                    match = re.findall(r'由 (.*) [在|编].*。(.*) ', comment.text)  # 匹配编辑者和内容
                    if match:
                        matchest = match[0]
                        matches = list(matchest)
                        for link in links:
                            matches.append(link.get('href'))  # 添加每个链接的href属性
                        if matches:
                            summary.append(matches)  # 添加到总结列表
                print(f'已爬取{len(summary)}条数据')  # 输出当前进度

        # 组装头部信息
        all_info['type'] = 'daily'
        all_info['name'] = mod.name
        all_info['start_time'] = start_time
        all_info['end_time'] = end_time
        all_info['link'] = mod.link
        all_info['edition'] = summary
        file_name = f'{start_time}~{end_time}模组{mod.name}编辑数据.json'
        # 如果 data 文件夹不存在，则创建它
        if not os.path.exists('data'):
            os.makedirs('data')

        # 构建完整的文件路径
        file_path = os.path.join('data', file_name)
        # 将编辑数据写入JSON文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(all_info, ensure_ascii=False, indent=4))
        return file_path
    else:
        # 如果请求失败，输出错误信息
        print(f'请求失败，状态码：{response.status_code}')
if __name__ == '__main__':
    main()
