# 基于PaddleRS的遥感智能解译平台

## 1 项目说明

本项目为第十一届 “中国软件杯”大学生软件设计大赛遥感解译赛道中web系统前端项目（不包含模型）。

## 2 团队成员

- 续兴
- 冯湛芸
- 何宇嘉
- 陈佳乐

## 3 环境要求

- Windows10 / Linux
- Python3.8
- paddlepaddle≥2.2.0
- 至少一块nvidia显卡：避免预测时间过长

## 4 依赖安装

本项目需要安装Flask，paddlepaddle等见requirements.txt，控制台执行以下命令

```shell
pip install requirements.txt
```

## 5 相关配置

修改config.py文件，可修改后端监听端口，日志文件存放位置，上传图片存放位置，相应模型文件路径等。

## 6 项目启动

在控制台执行以下命令，启动后后端地址即为ip:port，默认为localhost:8887

```shell
# 切换到项目文件夹下
cd rs-interpretation-Backend
python run.py
```
