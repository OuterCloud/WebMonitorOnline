## 接口检测平台
###环境需求

 1. 安装python flask框架；
 2. 安装python的requests库、bs库；
 3. 需要[Auty测试框架](https://github.com/OuterCloud/Auty.git)的支持，需要把Auty文件夹放到根目录下才能正常使用接口检测平台。

###使用说明

 本地运行run.py文件，然后访问 “http://127.0.0.1:5000” 即可。如果放置在公司服务器端，需要运维帮忙设置nginx并开通端口访问权限。并在服务器运行命令“nohup python run.py”来启动项目。
