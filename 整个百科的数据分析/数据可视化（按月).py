from pathlib import Path
import plotly.express as px
import json
import os


path = Path('2014-04-01~2024-09-01.json')  # 文件路径

# 获取文件名
filename = os.path.basename(path)

# 提取起始和结束日期
start_year = filename[0:4]  # 开始年份
start_date = filename[5:7]  # 开始月份
end_year = filename[11:15]  # 结束年份
end_date = filename[16:18]  # 结束月份

# 读取文件内容，并处理可能的Unicode解码错误
try:
    contents = path.read_text()  # 尝试默认编码读取
except UnicodeDecodeError:
    contents = path.read_text(encoding='utf-8')  # 如果有Unicode解码错误，则使用utf-8编码读取

# 将文件内容转换为Python字典
summary = json.loads(contents)

# 处理数据
timer = [times[0].split('~')[0] for times in summary]  # 取出开始日期
frequencies = [int(frequency[1]) for frequency in summary]  # 转换为整数

# 构建图表标题和轴标签
title = f'MC百科{start_year}年{start_date}月至{end_year}年{end_date}月模组编辑情况'
labels = {'x': '时间', 'y': '编辑次数'}

# 使用Plotly创建柱状图
fig = px.bar(x=timer, y=frequencies, title=title, labels=labels)

# 更新图表布局，设置字体大小
fig.update_layout(
    title_font_size=28,  # 设置标题字体大小
    xaxis_title_font_size=20,  # 设置X轴标题字体大小
    yaxis_title_font_size=20,  # 设置Y轴标题字体大小
)

# 保存图表为HTML文件
html_filename = f'{start_year}年{start_date}月至{end_year}年{end_date}月MC百科模组编辑数据.html'
fig.write_html(html_filename)

# 显示图表
fig.show()
