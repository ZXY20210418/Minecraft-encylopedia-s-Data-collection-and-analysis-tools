import json
import re
from pathlib import Path
from all_the_page import all_the_page_main
from by_mod import by_mod_main
from data_visible import data_visible_by_day,data_visible_by_editor,data_visible_by_mod_name,data_visible_by_month


def find_data_by_path():
    # 创建一个Path对象并使用rglob方法找到所有匹配的文件
    dir_path = Path('data')
    json_files = list(dir_path.rglob('*json'))
    if len(json_files) == 0:
        print('当前还没有文件，请添加文件或直接查找')
    print(f'已找到{len(json_files)}个文件')
    file_index = 0
    print('序号\t\t文件类型\t\t查找范围\t\t\t文件名')
    print('-' * 50)
    for file in json_files:
        print(file_index, end='\t\t')
        content = json.loads(file.read_text(encoding='utf-8'))
        if content['type'] == 'daily':
            print('按日', end='\t\t\t')
        elif content['type'] == 'monthly':
            print('按月', end='\t\t\t')
        else:
            print('未知', end='\t\t\t')
        if 'link' in content:
            print('单个模组', end='\t\t\t')
        else:
            print('整个百科', end='\t\t\t')
        print(file.name)
        file_index += 1
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
            if 'link' not in content:
                print('该文件的查找范围是：整个百科')
                is_all_mods = True
            else:
                print(f'该文件的查找范围是：{content['name']}模组')
                is_all_mods = False
            while True:
                print('1.按编辑日期可视化\n2.按编辑人可视化')
                if is_all_mods:
                    print('3.按模组可视化\n0:返回主菜单')
                else:
                    print('0:返回主菜单')
                re_user_choice_num = input('请选择要执行的操作：')
                if re_user_choice_num == '1':
                    final_file_path = data_visible_by_day.main(file_path)
                    print(f'生成的文件路径：{final_file_path}')
                    input('按回车键继续')
                    break
                elif re_user_choice_num == '2':
                    final_file_path = data_visible_by_editor.main(file_path)
                    print(f'生成的文件路径：{final_file_path}')
                    input('按回车键继续')
                    break
                elif re_user_choice_num == '0':
                    break
                else:
                    if is_all_mods:
                        if re_user_choice_num == '3':
                            final_file_path = data_visible_by_mod_name.main(file_path)
                            print(f'生成的文件路径：{final_file_path}')
                            input('按回车键继续')
                            break
                        else:
                            print('您输入的数字有误，请重新输入')
                    else:
                        print('您输入的数字有误，请重新输入')
        elif content['type'] == 'monthly':
            print('您输入的文件类型为：按月查找数据')
            if 'link' not in content:
                print('该文件的查找范围是：整个百科')
            else:
                print(f'该文件的查找范围是：{content['name']}模组')
            while True:
                print('1.数据可视化\n0.返回上一级')
                re_user_choice_num = input('请选择要执行的操作：')
                if re_user_choice_num == '1':
                    final_file_path = data_visible_by_month.main(file_path)
                    print(f'生成的文件路径：{final_file_path}')
                    input('按回车键继续')
                    break
                elif re_user_choice_num == '0':
                    break
                else:
                    print('您输入的数字有误，请重新输入')
            break
        else:
            print('该文件结构错误，请重新输入文件')

def main():
    while True:
        print('*' * 50)
        print('欢迎使用【MC模组数据收集和可视化系统】V1.0\n\n1.按模组查找\n2.从整个百科查找\n3.使用现有数据可视化\n\n0.退出系统')
        print('*' * 50)
        try:
            user_choice_num = input('请选择要执行的操作：')
            if user_choice_num == '1':
                by_mod_main.by_mod()
            elif user_choice_num == '2':
                all_the_page_main.all_the_page()
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

if __name__ == '__main__':
    main()
