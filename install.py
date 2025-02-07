import subprocess
import re
import os
from argparse import ArgumentParser
from shutil import copy2
import logging
import sys

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_input(prompt, default=None, validation=None):
    while True:
        user_input = input(prompt)
        if not user_input and default is not None:
            return default
        if validation and not validation(user_input):
            logging.warning("输入无效，请重试。")
            continue
        return user_input

class Install:
    def __init__(self):
        self.host = args.host
        self.port = args.port
        self.username = args.username
        self.password = args.password
        self.dbname = args.dbname
        self.email = args.email
        self.email_password = args.email_password
        # 设置源文件
        self.src = "docker/docker-compose.yaml"
        self.dst = "./docker-compose.yml"
    def get_user_input(self):
        if not self.host:
            self.host = get_user_input("请输入数据库地址: ")
        if not self.port:
            self.port = get_user_input("请输入数据库端口，默认: 3306: ", default=3306, validation=lambda x: re.match(r"^[0-9]+$", x))
        if not self.username:
            self.username = get_user_input("请输入数据库用户名，默认: thrive: ", default="thrive")
        if not self.password:
            self.password = get_user_input("请输入数据库密码: ", validation=lambda x: "|" not in x)
        if not self.dbname:
            self.dbname = get_user_input("请输入数据库名称，默认: ThriveX: ", default="ThriveX")
        if not self.email:
            self.email = get_user_input("请输入你的邮箱地址，默认: 123456789@qq.com: ", default="123456789@qq.com", validation=lambda x: "|" not in x)
        if not self.email_password:
            self.email_password = get_user_input("请输入你的邮箱密码，默认: 123456789: ", default="123456", validation=lambda x: "|" not in x)

    def replace_in_file(self, pattern, replacement):
        try:
            with open(self.dst, 'r', encoding='utf-8') as file:
                content = file.read()
                file.close()
        except Exception as e:
            logging.error(f"读取文件失败: {e}")
            sys.exit(1)
        content = re.sub(pattern, replacement, content)
        try:
            with open(self.dst, 'w', encoding='utf-8') as file:
                file.write(content)
                file.close()
        except Exception as e:
            logging.error(f"写入文件失败: {e}")
            sys.exit(1)
    def get_docker_status(self):
        if subprocess.getstatusoutput("docker ps > /dev/null 2>&1")[0] != 0:
            logging.error("Docker 未运行，请启动 Docker 后重试。")
            sys.exit(1)
    def copy(self):
        if os.path.isfile(self.src):
            try:
                copy2(self.src, self.dst)
            except Exception as e:
                logging.error(f"复制文件失败: {e}")
                sys.exit(1)
        else:
            logging.error(f"未找到 {self.src} 文件")
            sys.exit(1)
    def replace(self):
        self.replace_in_file(r"DbHost", self.host)
        self.replace_in_file(r"Port3306", str(self.port))
        self.replace_in_file(r"DbNameThriveX", self.dbname)
        self.replace_in_file(r"DbUserThrive", self.username)
        self.replace_in_file(r"DB_PASSWORD_ThriveX@123\?", self.password)
        self.replace_in_file(r"123456789@qq\.com", self.email)
        self.replace_in_file(r"123456789Password", self.email_password)
    def build(self):
        try:
            result = subprocess.getstatusoutput("docker compose -p thrive up -d --build")
            if result[0] != 0:
                logging.error(f"构建失败: {result[1]}")
                sys.exit(1)
            logging.info("构建成功")
        except Exception as e:
            logging.error(f"构建失败: {e}")
            sys.exit(1)
    def start(self):
        self.get_docker_status()
        self.copy()
        self.get_user_input()
        self.replace()
        self.build()


if __name__ == "__main__":
    arg = ArgumentParser(description='当前脚本版本: 1.0', prog="ThriveXServer")
    arg.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    arg.add_argument('-H', '--host', default=None, help='数据库地址', dest='host')
    arg.add_argument('-p', '--password', default=None, help='数据库密码', dest='password')
    arg.add_argument('-u', '--username', default=None, help='数据库用户名', dest='username')
    arg.add_argument('-d', '--dbname', default=None, help='数据库名称', dest='dbname')
    arg.add_argument('-e', '--email', default=None, help='邮箱地址', dest='email')
    arg.add_argument('-E', '--email_password', default=None, help='邮箱密码', dest='email_password')
    args = arg.parse_args()
    s = Install()
    s.start()
