from flask import Blueprint, request, current_app
from flask_cors import cross_origin
from config import baseDir, UPLOAD_FOLDER, REULTS_FOLDER
import os, time, base64
from ..utils.utils import decodeImage
from predict.infer_app import infer_object_extraction

extraction = Blueprint('extraction', __name__, url_prefix='/extraction')

fileDir = os.path.join(baseDir, UPLOAD_FOLDER)


# 目标提取预测
@extraction.route('/predict', methods=['POST'])
@cross_origin(supports_credentials=True)
def predict():
    current_app.logger.info("调用 目标提取预测 接口，ip:{}，method:{}".format(request.referrer, request.method))

    fileName = request.json.get("fileName")

    if fileName is None:
        imageData = request.json.get("imageData")
        if imageData is None:
            current_app.logger.warning("参数错误...")
            return {'success': False, 'msg': '参数错误！'}
        else:
            fileName = decodeImage(imageData)

    current_app.logger.info("fileName:{}".format(fileName))

    file = os.path.join(fileDir, fileName)
    if not os.path.exists(file):
        current_app.logger.warning("文件不存在！")
        return {'success': False, 'msg': '文件不存在！'}

    try:
        current_app.logger.info("开始调用模型预测...")
        t0 = time.time()

        # 调用模型预测
        resultFileName = infer_object_extraction(file)
        # time.sleep(7)
        # resultFileName = 'oe_result.png'

        t1 = time.time()
        t = t1 - t0

        current_app.logger.info("模型预测成功！时间：{}；结果文件名：{}".format(t, resultFileName))

        resultFile = open(os.path.join(REULTS_FOLDER, resultFileName), 'rb')
        base64Data = base64.b64encode(resultFile.read())

        result = {"time": round(t, 2), "fileName": resultFileName, "data": str(base64Data, encoding='utf-8')}
        return {'success': True, 'msg': '模型预测成功！', 'result': result}
    except Exception as e:
        current_app.logger.error("模型预测失败，{}".format(e))
        return {'success': False, 'msg': '模型预测失败！'}