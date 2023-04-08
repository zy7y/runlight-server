#!/bin/bash

message=$1

# 检查提交信息是否为空
if [ -z "$message" ]; then
    echo "请提供提交信息"
    exit 1
fi

# 提交并推送修改
git add .
git commit -m "$message"
git push origin master

echo "提交成功"
