from pathlib import Path
import plotly.express as px
from collections import Counter
import json
import os

# 定义文件路径
path = Path('20230101~20230131.json')

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

# 提取编辑者信息（用户名和链接）
list_editor_info = [(editor_info[0], editor_info[3]) for editor_info in summary]

# 统计每个编辑者的编辑次数
counted_editor_info = Counter(list_editor_info).items()

# 按编辑次数降序排序
sorted_editor_info = sorted(counted_editor_info, key=lambda x: x[1], reverse=True)

# 生成编辑者链接列表
editor_links = [f"<a href='{tuple_editor_info[0][1]}'>{tuple_editor_info[0][0]}</a>" for tuple_editor_info in sorted_editor_info]

# 提取编辑次数列表
frequencies = [frequency[1] for frequency in sorted_editor_info]

# 构建图表标题和轴标签
title = f'MC百科{start_year}年{start_date[0:2]}月{start_date[2:4]}日至{end_year}年{end_date[0:2]}月{end_date[2:4]}日模组编辑人情况'
labels = {'x': '编辑人', 'y': '编辑次数'}

# 使用Plotly创建柱状图
fig = px.bar(x=editor_links, y=frequencies, title=title, labels=labels)

# 更新图表布局
fig.update_layout(
    title_font_size=28,    # 标题字体大小
    xaxis_title_font_size=20,  # X轴标题字体大小
    yaxis_title_font_size=20,  # Y轴标题字体大小
)

# 保存图表为HTML文件
html_filename = (f'{start_year}年{start_date[0:2]}月{start_date[2:4]}日至{end_year}年{end_date[0:2]}月{end_date[2:4]}日MC'
                 f'百科模组编辑人数据.html')
fig.write_html(html_filename)

# 显示图表
fig.show()
