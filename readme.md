#  中国医科大学自动预约宿舍洗澡位置

基于FastAPI开发

## 实现功能：

1. 可以发送单请求直接预约到指定楼栋、指定楼层、指定位置的洗澡位
2. 可以24小时监视您想要的洗澡位置，实现在学校允许洗澡的时间内在您想要的位置上随时可以洗
3. 避免学校宿舍洗浴系统前端崩溃问题

## 运行流程：

### 服务端

1. 准备一台带有公网IP的服务器（或者也可以选择内网部署）
2. clone本仓库，使用pip install -r requirements.txt安装本项目的所有依赖
3. 运行python main.py，启动Uvicorn，大功告成

### 客户端

由于构建请求需要学校洗浴系统的cookie，故需要先使用抓包软件进行抓包。iOS端可以使用Stream APP，安卓端可以使用Packet Capture，如果使用PC可以通过代理将手机流量代理到Fiddler或Charles上进行抓包。

FastAPI自带Swagger文档，在服务运行之后可以使用http://{服务器IP}:7767/docs访问文档

可查看client_demo.py作为客户端开发参考

## 注意事项

开发者本人不承担任何由于使用此项目导致的后果，请自觉遵守道德底线，不要使用本项目做出任何有损他人利益的行为

夏季高峰期，洗澡需要排队，本项目不能解决排队问题，也请不要提相关issue

