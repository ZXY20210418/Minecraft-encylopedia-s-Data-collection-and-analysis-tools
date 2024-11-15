# 导入必要的模块
import os
from pathlib import Path
import plotly.express as px  # 用于生成交互式图表
from collections import Counter  # 用于统计元素出现的频率
import json  # 处理JSON数据

def main(file_name):
    # 定义文件路径
    path = Path(file_name)

    # 读取文件内容，并尝试处理编码问题
    contents = path.read_text(encoding='utf-8')

    # 将文件内容转换为Python字典
    summary = json.loads(contents)

    if summary['type'] != "daily":
        print('这不是按日查找的文件，请重新输入文件')
        return

    # 提取起始和结束日期
    start_year = summary['start_time'][0:4]
    start_date = summary['start_time'][4:8]
    end_year = summary['end_time'][0:4]
    end_date = summary['end_time'][4:8]

    # 提取包含'class'字段的mods_info元组，并形成一个新的列表
    list_mods_info = [(mods_info[1], mods_info[4]) for mods_info in summary['edition'] if any('class' in item for item in mods_info)]

    # 计算每个mods_info项的出现次数并排序
    counted_mods_info = Counter(list_mods_info).items()
    sorted_mods_info = sorted(counted_mods_info, key=lambda x: x[1], reverse=True)

    # 为每个mods_info项创建一个HTML链接
    mods_links = [f"<a href='{tuple_mods_info[0][1]}'>{tuple_mods_info[0][0]}</a>" for tuple_mods_info in sorted_mods_info]

    # 提取出每个项的编辑次数
    frequencies = [frequency[1] for frequency in sorted_mods_info]

    # 定义图表标题
    title = f'MC百科{start_year}年{start_date[0:2]}月{start_date[2:4]}日至{end_year}年{end_date[0:2]}月{end_date[2:4]}日模组编辑次数情况'

    # 定义图表标签
    labels = {'x': '模组', 'y': '编辑次数'}

    # 创建柱状图
    fig = px.bar(x=mods_links, y=frequencies, title=title, labels=labels)

    # 更新图表布局以设置字体大小
    fig.update_layout(title_font_size=28, xaxis_title_font_size=20, yaxis_title_font_size=20)

    # 定义输出HTML文件的名称
    html_filename = (f'{start_year}年{start_date[0:2]}月{start_date[2:4]}日至{end_year}年{end_date[0:2]}月{end_date[2:4]}日MC'
                     f'百科模组编辑次数数据.html')

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
