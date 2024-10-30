import re
from pathlib import Path
import get_data_by_day
import get_data_by_month
import data_visible_by_day
import data_visible_by_month
import data_visible_by_person
import json


def show_data_by_month():
    file_path = get_data_by_month.main()
    if file_path == 'exit':
        return
    print('按月查找数据完成！\n1.数据可视化\n0.返回主菜单')
    re_user_choice_num = input('请选择要执行的操作：')
    if re_user_choice_num == '1':
        final_file_path = data_visible_by_month.main(file_path)
        print(f'生成的文件路径：{final_file_path}')
        input('按回车键继续')
    elif re_user_choice_num == '0':
        print(f'生成的文件路径（数据）：{file_path}')
        input('按回车键继续')


def show_data_by_daily():
    file_path = get_data_by_day.main()
    if file_path == 'exit':
        return
    print('按日查找数据完成！\n1.按编辑日期可视化\n2.按编辑人可视化\n0.返回主菜单')
    re_user_choice_num = input('请选择要执行的操作：')
    if re_user_choice_num == '1':
        final_file_path = data_visible_by_day.main(file_path)
        print(f'生成的文件路径：{final_file_path}')
    elif re_user_choice_num == '2':
        final_file_path = data_visible_by_person.main(file_path)
        print(f'生成的文件路径：{final_file_path}')
    elif re_user_choice_num == '0':
        print(f'生成的文件路径（数据）：{file_path}')
    input('按回车键继续')

def find_data_by_path():
    # 创建一个Path对象并使用rglob方法找到所有匹配的文件
    dir_path = Path('data')
    json_files = list(dir_path.rglob('*json'))
    if len(json_files) == 0:
        print('当前还没有文件，请添加文件或直接查找')
    print(f'已找到{len(json_files)}个文件')
    file_index = 0
    for file in json_files:
        print(f'序号：{file_index}，文件：{file.name}，文件类型：', end='')
        content = json.loads(file.read_text(encoding='utf-8'))
        file_index += 1
        if content['type'] == 'daily':
            print('按日查找')
        elif content['type'] == 'monthly':
            print('按月查找')
        else:
            print('未知')
    while True:
        try:
            user_finding_num = int(input('请选择要可视化的文件（输入序号）：'))
            if 0 <= user_finding_num <= file_index:
                return json_files[user_finding_num]
            else:
                print('序号不能超出范围')
        except ValueError:
            print('您输入的数字有误，请重新输入')

def show_data_by_path():
    while True:
        while True:
            print('1.扫描现有文件\n2.使用外部文件\n0.返回主菜单')
            re_user_choice_num = input('请选择要执行的操作：')
            if re_user_choice_num == '1':
                file_path = find_data_by_path()
                break
            elif re_user_choice_num == '2':
                file_path = input('请将外部文件路径复制到此处：')
                if '"' in file_path:
                    file_path = re.findall(r'\"(.*)\"', file_path)[0]
                break
            elif re_user_choice_num == '0':
                return
            else:
                print('您输入的数字有误，请重新输入')
        path = Path(file_path)
        content = json.loads(path.read_text(encoding='utf-8'))
        print(f'您输入的文件名为：{path.name}')
        if content['type'] == 'daily':
            print('您输入的文件类型为：按日查找数据')
            while True:
                print('1.按编辑日期可视化\n2.按编辑人可视化\n0:返回主菜单')
                re_user_choice_num = input('请选择要执行的操作：')
                if re_user_choice_num == '1':
                    final_file_path = data_visible_by_day.main(file_path)
                    print(f'生成的文件路径：{final_file_path}')
                    input('按回车键继续')
                    break
                elif re_user_choice_num == '2':
                    final_file_path = data_visible_by_person.main(file_path)
                    print(f'生成的文件路径：{final_file_path}')
                    input('按回车键继续')
                    break
                elif re_user_choice_num == '0':
                    input('按回车键继续')
                    break
                else:
                    print('您输入的数字有误，请重新输入')
        elif content['type'] == 'monthly':
            print('您输入的文件类型为：按月查找数据')
            while True:
                print('1.数据可视化\n0.返回上一级')
                re_user_choice_num = input('请选择要执行的操作：')
                if re_user_choice_num == '1':
                    final_file_path = data_visible_by_month.main(file_path)
                    print(f'生成的文件路径：{final_file_path}')
                    input('按回车键继续')
                    break
                elif re_user_choice_num == '0':
                    input('按回车键继续')
                    break
                else:
                    print('您输入的数字有误，请重新输入')
            break
        else:
            print('该文件结构错误，请重新输入文件')


while True:
    print('*' * 50)
    print('欢迎使用【MC模组数据收集和可视化系统】V1.0\n\n1.按月查找（最少一个月）\n2.按日查找（最大30天）\n3.将数据文件可视化\n\n0.退出系统')
    print('*' * 50)
    try:
        user_choice_num = input('请选择要执行的操作：')
        if user_choice_num == '1':
            show_data_by_month()
        elif user_choice_num == '2':
            show_data_by_daily()
        elif user_choice_num == '3':
            show_data_by_path()
        elif user_choice_num == '0':
            print('欢迎再次使用模组数据收集和可视化系统')
            input('按回车键退出')
            break
        else:
            print('您输入的数字有误，请重新输入')
    except Exception as e:
        print(f'未知错误：{e}')
