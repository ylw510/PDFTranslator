#!/bin/bash
# 使用国内镜像安装依赖

# 常用国内镜像源
# 清华大学: https://pypi.tuna.tsinghua.edu.cn/simple
# 阿里云: https://mirrors.aliyun.com/pypi/simple/
# 中科大: https://pypi.mirrors.ustc.edu.cn/simple/
# 豆瓣: https://pypi.douban.com/simple/

echo "使用清华大学镜像源安装依赖..."
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "安装完成！"
