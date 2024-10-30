from pathlib import Path
import plotly.express as px
from collections import Counter
import json
import os

# 定义文件路径
path = Path('20240801~20240831.json')

# 获取文件名
filename = os.path.basename(path)

# 提取起始和结束日期
start_year = filename[0:4]
start_date = filename[4:8]
end_year = filename[9:13]
end_date = filename[13:17]

# 读取文件内容，并尝试处理编码问题
try:
    contents = path.read_text()
except:
    contents = path.read_text(encoding='utf-8')

# 将文件内容转换为Python字典
summary = json.loads(contents)

# 从summary中提取日期，并去除时间部分
timely = [time_info[2].split(' ')[0] for time_info in summary]

# 统计每个日期出现的次数
listr = Counter(timely)

# 准备绘图的数据
timels, frequencies = [], []
for timel, frequency in listr.items():
    timels.append(timel)
    frequencies.append(frequency)

# 构建图表标题和轴标签
title = f'MC百科{start_year}年{start_date[0:2]}月{start_date[2:4]}日至{end_year}年{end_date[0:2]}月{end_date[2:4]}日模组编辑情况'
labels = {'x': '时间', 'y': '编辑次数'}

# 使用Plotly创建柱状图
fig = px.bar(x=timels, y=frequencies, title=title, labels=labels)

# 更新图表布局
fig.update_layout(
    title_font_size=28,    # 标题字体大小
    xaxis_title_font_size=20,  # X轴标题字体大小
    yaxis_title_font_size=20,  # Y轴标题字体大小
)

# 保存图表为HTML文件
html_filename = f'{start_year}年{start_date[0:2]}月{start_date[2:4]}日至{end_year}年{end_date[0:2]}月{end_date[2:4]}日MC百科模组编辑次数数据.html'
fig.write_html(html_filename)

# 显示图表
fig.show()
