#!/usr/bin/bash

# 判断环境变量值是否为空
if [[ -z "${DB_INFO}" ]]; then
  echo "DB_INFO is empty"
  exit 1
fi
# 判断端口变量是否为空
if [[ -z "${PORT}" ]]; then
  export PORT=9003
  echo "PORT is empty, use default value:9003"
fi
# 判断数据库用户及密码是否为空
if [[ -z "${DB_USER}" || -z "${DB_PASSWORD}" ]]; then
  echo "DB_USER or DB_PASSWORD is empty"
  exit 1
fi
# 判断 EMAIL_HOST 是否为空
if [[ -z "${EMAIL_HOST}" ]]; then
  echo "EMAIL_HOST is empty"
  exit 1
fi
# 判断EMAIL_PORT 是否为空,如果为空则默认为465
if [[ -z "${EMAIL_PORT}" ]]; then
  export EMAIL_PORT=465
  echo "EMAIL_PORT is empty, use default value:465"
fi
# 判断邮箱用户及密码是否为空
if [[ -z "${EMAIL_USER}" || -z "${EMAIL_PASSWORD}" ]]; then
  echo "EMAIL_USER or EMAIL_PASSWORD is empty"
  exit 1
fi
echo "---------------------------打印数据库配置----------------------------"
echo ${DB_INFO}
echo "---------------------------打印数据库配置----------------------------"
echo "Starting server..."
cmd="java -jar blog.jar --PORT=${PORT} --DB_INFO=${DB_INFO} --DB_USERNAME=${DB_USERNAME} --DB_PASSWORD=${DB_PASSWORD} --EMAIL_HOST=${EMAIL_HOST} --EMAIL_PORT=${EMAIL_PORT} --EMAIL_USERNAME=${EMAIL_USERNAME} --EMAIL_PASSWORD=${EMAIL_PASSWORD}"
echo "Running: $cmd"
eval $cmd
