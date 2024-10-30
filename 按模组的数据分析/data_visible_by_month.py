import json  # 导入json模块，用于处理JSON数据
import os
from pathlib import Path  # 导入Path类，用于处理文件路径
import plotly.express as px  # 导入Plotly Express模块，用于绘制图表


def main(file_name):
    # 定义文件路径
    path = Path(file_name)

    # 读取文件内容，指定UTF-8编码
    contents = path.read_text(encoding='utf-8')

    # 将文件内容转换为Python字典
    mod_info = json.loads(contents)

    # 检查数据类型是否为每月编辑记录
    if mod_info['type'] != 'monthly':
        print('这不是按月查找的文件，请重新输入文件')
        exit()  # 如果不是每月记录，则退出程序

    # 从字典中提取编辑记录
    summary = mod_info['edition']

    # 提取起始和结束年月
    start_year = mod_info['start_time'][0:4]
    start_month = mod_info['start_time'][4:7]
    end_year = mod_info['end_time'][0:4]
    end_month = mod_info['end_time'][4:7]

    # 获取模组名称和链接
    mod_name = mod_info['name']
    mod_link = mod_info['link']

    # 从编辑记录中提取时间信息
    timer = [times[0].split('~')[0] for times in summary]

    # 提取编辑次数
    frequencies = [int(frequency[1]) for frequency in summary]

    # 构建图表标题，包括模组名称和时间范围，并添加链接
    title = (
        f'MC百科{start_year}年{start_month}月至{end_year}年{end_month}月'
        f'<a href="{mod_link}" target="_blank">{mod_name}</a>模组编辑情况'
        '<br><a href="https://www.bilibili.com/video/BV1GJ411x7h7" target="_blank">展开</a>'
    )

    # 设置图表轴标签
    labels = {'x': '时间', 'y': '编辑次数'}

    # 使用Plotly创建条形图
    fig = px.bar(x=timer, y=frequencies, title=title, labels=labels)

    # 更新图表布局，设置字体大小
    fig.update_layout(
        title_font_size=28,  # 设置标题字体大小
        xaxis_title_font_size=20,  # 设置X轴标题字体大小
        yaxis_title_font_size=20,  # 设置Y轴标题字体大小
    )

    # 构建HTML文件名
    html_filename = f'{start_year}年{start_month}月至{end_year}年{end_month}月MC百科{mod_name}模组编辑数据.html'
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

