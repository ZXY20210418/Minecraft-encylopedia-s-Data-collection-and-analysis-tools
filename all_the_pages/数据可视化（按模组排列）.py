# 导入必要的模块
from pathlib import Path
import plotly.express as px  # 用于生成交互式图表
from collections import Counter  # 用于统计元素出现的频率
import json  # 处理JSON数据
import os  # 文件系统操作

# 定义文件路径
path = Path('20240801~20240831.json')

# 获取文件名
filename = os.path.basename(path)

# 解析文件名中的日期信息
start_year = filename[0:4]
start_date = filename[4:8]
end_year = filename[9:13]
end_date = filename[13:17]

# 尝试读取文件内容，如果默认编码不适用，则使用UTF-8编码
try:
    contents = path.read_text()
except UnicodeDecodeError:
    contents = path.read_text(encoding='utf-8')

# 将读取的内容解析为JSON对象
summary = json.loads(contents)

# 提取包含'class'字段的mods_info元组，并形成一个新的列表
list_mods_info = [(mods_info[1], mods_info[4]) for mods_info in summary if any('class' in item for item in mods_info)]

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

# 将图表写入HTML文件
fig.write_html(html_filename)

# 显示图表
fig.show()
