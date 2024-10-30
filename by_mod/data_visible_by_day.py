import os
from pathlib import Path  # 导入Path类，用于处理文件路径
import plotly.express as px  # 导入Plotly Express模块，用于绘制图表
from collections import Counter  # 导入Counter类，用于统计元素出现的频率
import json  # 导入json模块，用于处理JSON数据


def main(file_name):
    # 定义文件路径
    path = Path(file_name)
    # 读取文件内容，指定UTF-8编码
    contents = path.read_text(encoding='utf-8')

    # 将文件内容转换为Python字典
    mod_info = json.loads(contents)

    # 检查数据类型是否为每日编辑记录
    if mod_info['type'] != 'daily':
        print('这不是按日查找的文件，请重新输入文件')
        exit()  # 如果不是每日记录，则退出程序

    # 从字典中提取编辑记录
    summary = mod_info['edition']
    # 提取起始和结束日期
    start_year = mod_info['start_time'][0:4]
    start_date = mod_info['start_time'][4:9]
    end_year = mod_info['end_time'][0:4]
    end_date = mod_info['end_time'][4:9]
    mod_name = mod_info['name']  # 模组名称
    mod_link = mod_info['link']  # 模组链接

    # 提取每天的日期
    timely = [time_info[1].split(' ')[0] for time_info in summary]

    # 使用Counter统计每天的编辑次数
    listr = Counter(timely)

    # 初始化时间列表和频率列表
    timels, frequencies = [], []

    # 将Counter对象转换为两个列表
    for timel, frequency in listr.items():
        timels.append(timel)
        frequencies.append(frequency)

    # 构建图表标题，包括模组名称和时间范围，并添加链接
    title = (
        f'MC百科{start_year}年{start_date[0:2]}月{start_date[2:4]}日至{end_year}年{end_date[0:2]}月{end_date[2:4]}日'
        f'<a href="{mod_link}" target="_blank">{mod_name}</a>模组编辑情况'
        '<br><a href="https://www.bilibili.com/video/BV1GJ411x7h7" target="_blank">展开</a>'
    )
    labels = {'x': '时间', 'y': '编辑次数'}  # 图表轴标签

    # 使用Plotly创建柱状图
    fig = px.bar(x=timels, y=frequencies, title=title, labels=labels)

    # 更新图表布局，设置字体大小
    fig.update_layout(
        title_font_size=28,  # 设置标题字体大小
        xaxis_title_font_size=20,  # 设置X轴标题字体大小
        yaxis_title_font_size=20,  # 设置Y轴标题字体大小
    )

    # 构建HTML文件名
    html_filename = (
        f'{start_year}年{start_date[0:2]}月{start_date[2:4]}日至{end_year}年{end_date[0:2]}月{end_date[2:4]}日'
        f'{mod_name}模组编辑数据.html'
    )
    # 如果 files 文件夹不存在，则创建它
    if not os.path.exists('files'):
        os.makedirs('files')
    # 构建完整的文件路径
    file_path = os.path.join('files', html_filename)
    # 将图表保存为HTML文件
    fig.write_html(file_path)
    user_choice = input('图表生成完成！是否立即查看（输入y确定，输入其他退出）？')
    if user_choice == 'y':
        # 显示图表
        fig.show()
    return file_path
if __name__ == '__main__':
    main(input('请将文件地址复制到此处：'))
