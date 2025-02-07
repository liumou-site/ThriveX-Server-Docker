import subprocess
import re
import os
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

def replace_in_file(file_path, pattern, replacement):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    src = "docker/docker-compose.yaml"
    if not os.path.isfile(src):
        logging.error("未找到 docker-compose.yml 文件")
        sys.exit(1)

    try:
        copy2(src, "./docker-compose.yml")
    except Exception as e:
        logging.error(f"复制 docker-compose.yml 失败: {e}")
        sys.exit(1)

    logging.info("正在构建...")
    if subprocess.getstatusoutput("docker ps > /dev/null 2>&1")[0] != 0:
        logging.error("Docker 未运行，请启动 Docker 后重试。")
        sys.exit(1)

    host = get_user_input("请输入数据库地址: ")
    port = get_user_input("请输入数据库端口，默认: 3306: ", default=3306, validation=lambda x: re.match(r"^[0-9]+$", x))
    # 端口类型转换
    try:
        port = int(port)
    except ValueError:
        logging.error("端口格式错误，请输入数字。")
        sys.exit(1)
    username = get_user_input("请输入数据库用户名，默认: thrive: ", default="thrive")
    password = get_user_input("请输入数据库密码: ", validation=lambda x: "|" not in x)
    dbname = get_user_input("请输入数据库名称，默认: ThriveX: ", default="ThriveX")

    email = get_user_input("请输入你的邮箱地址，默认: 123456789@qq.com: ", default="123456789@qq.com", validation=lambda x: "|" not in x)
    email_password = get_user_input("请输入你的邮箱密码，默认: 123456789: ", default="123456", validation=lambda x: "|" not in x)

    logging.info("开始替换...")
    replace_in_file("docker-compose.yml", r"DbHost", host)
    replace_in_file("docker-compose.yml", r"Port3306", str(port))
    replace_in_file("docker-compose.yml", r"DbNameThriveX", dbname)
    replace_in_file("docker-compose.yml", r"DbUserThrive", username)
    replace_in_file("docker-compose.yml", r"DB_PASSWORD_ThriveX@123\?", password)
    replace_in_file("docker-compose.yml", r"123456789@qq\.com", email)
    replace_in_file("docker-compose.yml", r"123456789Password", email_password)

    result = subprocess.getstatusoutput("docker compose -p thrive up -d --build")
    if result[0] != 0:
        logging.error(f"构建失败: {result[1]}")
        sys.exit(1)

    logging.info("构建成功")

if __name__ == "__main__":
    main()
