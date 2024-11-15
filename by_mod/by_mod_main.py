from by_mod import get_data_by_day
from by_mod import get_data_by_month
from data_visible import data_visible_by_month, data_visible_by_editor, data_visible_by_day


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
        final_file_path = data_visible_by_editor.main(file_path)
        print(f'生成的文件路径：{final_file_path}')
    elif re_user_choice_num == '0':
        print(f'生成的文件路径（数据）：{file_path}')
    input('按回车键继续')

def by_mod():
    while True:
        print('您正在使用的功能是：按模组查找')
        print('1.按月查找（最少一个月）\n2.按日查找（最大30天）\n0.返回上一级')
        try:
            user_choice_num = input('请选择要执行的操作：')
            if user_choice_num == '1':
                show_data_by_month()
            elif user_choice_num == '2':
                show_data_by_daily()
            elif user_choice_num == '0':
                break
            else:
                print('您输入的数字有误，请重新输入')
        except Exception as e:
            print(f'未知错误：{e}')
if __name__ == '__main__':
    by_mod()
