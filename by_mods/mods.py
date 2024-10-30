import requests  # 导入用于发送HTTP请求的库
from bs4 import BeautifulSoup  # 导入用于解析HTML文档的库
import re  # 导入正则表达式库，用于字符串匹配


class Mods:
    def __init__(self, name):  # 初始化类实例
        self.datetime = None  # 模组的收录日期
        self.name = name  # 模组名称
        self.edition_link = None  # 版本历史链接
        self.link = None
        self.headers = {  # 设置请求头，模拟浏览器访问
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }

    def get_mod_info(self):  # 获取模组信息的方法
        try:
            # 发送GET请求到指定的模组搜索URL
            mods_response = requests.get(f'https://search.mcmod.cn/s?key={self.name}', headers=self.headers)
            if mods_response.ok:  # 如果请求成功
                # 解析返回的HTML文档
                bs_search = BeautifulSoup(mods_response.text, 'lxml')
                # 选择第一个搜索结果的头部信息
                search_info = bs_search.select('div.head > a')[0]
                self.name = search_info.text  # 更新模组名
                self.link = search_info['href']  # 获取搜索结果的链接
                # 发送GET请求到搜索结果页面
                datetime_response = requests.get(self.link, headers=self.headers)
                # 解析返回的HTML文档
                bs_datetime_response = BeautifulSoup(datetime_response.text, 'lxml')
                # 获取模组的收录日期
                self.datetime = bs_datetime_response.select('li.col-lg-4[data-toggle="tooltip"]')[0]['data-original-title']
                # 使用正则表达式从链接中提取出需要的部分，并拼接成版本历史编辑页面的链接
                split_link = re.findall(r'(.*class)(.*)', self.link)[0]
                self.edition_link = split_link[0] + '/history' + split_link[1]
                # 当脚本被直接运行时，跳过用户交互部分
                if __name__ == '__main__':
                    return
                # 提示用户确认是否继续
                user_choice = input(f'您要查找的模组：{self.name}\n'
                                    f'链接：{self.link}\n'
                                    f'收录日期：{self.datetime}\n'
                                    f'确定要查找吗（输入y确定，输入其他退出）？')
                if user_choice != 'y':  # 如果用户不确认，则退出程序
                    return 'exit'
            else:  # 如果请求失败
                print(f'请求失败，状态码：{mods_response.status_code}')
                return 'exit'  # 退出程序
        except IndexError:  # 如果找不到元素
            print(f'您要查找的{self.name}不存在')
            return 'exit'  # 退出程序
        except Exception as e:  # 如果发生其他异常
            print(f'未知错误：{e}')
            return 'exit'  # 退出程序


if __name__ == '__main__':  # 当脚本被直接运行时
    mod = Mods(input('请输入您要查询的模组名称（打全名）：'))  # 创建一个Mods类的实例，参数为模组名称
    mod.get_mod_info()  # 调用get_mod_info方法获取模组信息
    print(mod.name, mod.datetime, mod.edition_link)  # 打印模组的信息
