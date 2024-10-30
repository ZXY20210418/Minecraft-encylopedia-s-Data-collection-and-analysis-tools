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
        edition_start_time = int(edition_start_time_list[0] + edition_start_time_list[1]) * 100 + 0o01
        edition_start_time_stamp = int(datetime.strptime(str(edition_start_time), '%Y%m%d').timestamp())

        try:
            # 用户输入开始和结束的时间（格式为YYYYMM）
            start_time = input('请输入开始年/月份（格式YYYYMM）：')
            end_time = input('请输入结束年/月份（格式YYYYMM）：')
            date_format = "%Y%m%d"  # 时间格式

            # 验证输入的时间长度是否符合要求
            if len(start_time) != 6 or len(end_time) != 6:
                print('起始时间和结束时间必须按格式输入')

            # 补全时间格式
            regular_start_time = str(int(start_time) * 100 + 0o01)
            regular_end_time = str(int(end_time) * 100 + 0o01)

            # 将时间字符串转换为时间戳
            st_object = int(datetime.strptime(regular_start_time, date_format).timestamp())
            et_object = int(datetime.strptime(regular_end_time, date_format).timestamp())

            # 验证时间范围是否合理
            if st_object > et_object:
                print('结束时间不得大于开始时间')
            elif st_object < edition_start_time_stamp or et_object < edition_start_time_stamp:
                print(f'{edition_start_time_list[0]}年{edition_start_time_list[1]}月MC'
                      f'百科才开始收录模组{mod.name}，你搁这时空穿越呢')
            elif st_object > time_now_stamp or et_object > time_now_stamp:
                print(f'现在是{time[0]}年{time[1]}月，你搁这预知未来呢')
            elif et_object - st_object < 2592000:  # 至少一个月的时间跨度
                print('最少一月')
            else:
                break
        except ValueError:
            # 如果输入的时间格式不正确
            print('请输入正确的时间格式（YYYYMM）')
        except Exception as ex:
            # 如果发生其他未知错误
            print(f'未知错误：{ex}')

    # 初始化每月编辑记录列表
    monthly_info = []
    all_info = {}  # 用于存储头部信息

    # 循环遍历时间范围内的每个月
    for end in range(st_object, et_object, 2592000):
        # 构造请求URL
        response = requests.get(f'{mod.edition_link}?starttime={end}&endtime={end + 2592000}',
                                headers=mod.headers)

        # 检查请求是否成功
        if response.ok:
            html = response.text  # 获取响应内容
            search = BeautifulSoup(html, 'lxml')  # 解析HTML

            try:
                # 尝试获取分页信息中的编辑数量
                edition_per_month = search.select('ul.pagination>span')[0]
            except IndexError:
                # 如果没有分页信息，则尝试获取历史列表中的元素数量
                edition_per_month = search.select('div.history-list-frame li')
                line_str = str(len(edition_per_month))
            else:
                # 从分页信息中提取编辑数量
                line_str = re.findall(r'(\d+).条', edition_per_month.string)[0]

            # 格式化时间
            start_time_final = str(datetime.fromtimestamp(end))[0:10]
            end_time_final = str(datetime.fromtimestamp(end + 2592000))[0:10]

            # 记录时间段及其编辑次数
            summary = [f'{start_time_final}~{end_time_final}', line_str]
            monthly_info.append(summary)

            # 输出结果
            print(f'时间段：{summary[0]}，编辑次数：{summary[1]}')
        else:
            # 如果请求失败，输出错误信息
            print(f'请求失败，状态码：{response.status_code}')

    # 组装头部信息
    all_info['type'] = 'monthly'
    all_info['name'] = mod.name
    all_info['start_time'] = start_time
    all_info['end_time'] = end_time
    all_info['link'] = mod.link
    all_info['edition'] = monthly_info
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

if __name__ == '__main__':
    main()
