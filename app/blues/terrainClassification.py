from flask import Blueprint, request, current_app
from flask_cors import cross_origin
from config import baseDir, UPLOAD_FOLDER
import os, time

classify = Blueprint('classify', __name__, url_prefix='/classify')

fileDir = os.path.join(baseDir, UPLOAD_FOLDER)


# 地物分类
@classify.route('/predict', methods=['POST'])
@cross_origin(supports_credentials=True)
def predict():
    current_app.logger.info("调用 地物分类预测 接口，ip:{}，method:{}".format(request.referrer, request.method))

    fileName = request.json.get("fileName")

    if fileName is None:
        current_app.logger.warning("参数错误...")
        return {'success': False, 'msg': '参数错误！'}

    current_app.logger.info("fileName:{}".format(fileName))

    file = os.path.join(fileDir, fileName)
    if not os.path.exists(file):
        current_app.logger.warning("文件不存在！")
        return {'success': False, 'msg': '文件不存在！'}

    try:
        current_app.logger.info("开始调用模型预测...")
        t0 = time.time()
        # TODO
        # 调用模型预测

        t1 = time.time()
        t = t1 - t0

        current_app.logger.info("模型预测成功！时间：{}；结果文件名：{}".format(t, ""))

        result = {"time": round(t, 2), "fileName": "", "data": ""}
        return {'success': True, 'msg': '模型预测成功！', 'result': result}
    except Exception as e:
        current_app.logger.error("模型预测失败，{}".format(e))
        return {'success': False, 'msg': '模型预测失败！'}