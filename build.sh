#!/usr/bin/env bash
set -e
set -x
src=docker/docker-compose.yaml
if [[ ! -f ${src} ]]; then
  echo "Not found docker-compose.yml file"
  exit 1
fi
cp -r ${src} ./docker-compose.yml
if [[ $? -ne 0 ]]; then
  echo "Copy docker-compose.yml failed"
  exit 1
fi
echo "Building..."
docker ps > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
  echo "Docker is not running, please start docker and try again."
  exit 1
fi
# 输入数据库地址
echo "Please input your database address(请输入数据库地址):"
read host
if [[ -z "$host" ]]; then
  echo "Database address cannot be empty, please try again."
  exit 1
fi
echo "Please input your database port,Default:3306(请输入数据库端口,默认:3306):"
read port
if [[ -z "$port" ]]; then
  port=3306
fi
# 检查端口是否为数字
if ! [[ $port =~ ^[0-9]+$ ]] ; then
  echo "Port must be a number, please try again."
  exit 1
fi
echo "Please input your database username, Default: thrive (请输入数据库用户名,默认:thrive):"
read username
if [[ -z "$username" ]]; then
  username=thrive
fi
echo "Please input your database password(请输入数据库密码):"
read password
if [[ -z "$password" ]]; then
  echo "Database password cannot be empty, please try again."
  exit 1
fi
echo $password | grep \|
if [[ $? -eq 0 ]]; then
  echo "Database password cannot contain |, please try again."
  exit 1
fi
echo "Please input your database name, Default:ThriveX(请输入数据库名称,默认:ThriveX):"
read dbname
if [[ -z "$dbname" ]]; then
  dbname=ThriveX
fi
# 输入邮箱地址
echo "Please input your email address, Default:123456789@qq.com(请输入你的邮箱地址):"
read email
if [[ -z "$email" ]]; then
  email="123456789@qq.com"
fi
echo $email
echo $email | grep \|
if [[ $? -eq 0 ]]; then
  echo "Email address cannot contain |, please try again."
  exit 1
fi
# 输入邮箱密码
echo "Please input your email password, Default:123456789(请输入你的邮箱密码):"
read email_password
if [[ -z "$email_password" ]]; then
  email_password="123456"
fi
echo $email_password | grep \|
if [[ $? -eq 0 ]]; then
  echo "Email password cannot contain |, please try again."
  exit 1
fi
# 开始替换
echo "Start replacing..."
sed -i "s@DbHost@${host}@" docker-compose.yml
sed -i "s@Port3306@${port}@" docker-compose.yml
sed -i "s@DbUserThrive@${username}@" docker-compose.yml
sed -i "s|DB_PASSWORD_ThriveX@123?|${password}|" docker-compose.yml
# 替换邮箱
sed -i "s|123456789@qq.com|${email}|" docker-compose.yml
sed -i "s|123456789Password|${email_password}|" docker-compose.yml
docker compose -p thrive up -d --build
if [[ $? -ne 0 ]]; then
  echo "Build failed"
  exit 1
fi
echo "Build success"