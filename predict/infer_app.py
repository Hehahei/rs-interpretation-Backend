# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 14:16
# @Author  : xuxing
# @Site    : 
# @File    : infer_app.py
# @Software: PyCharm

import numpy as np
from PIL import Image
import paddlers as pdrs
import sys
import os, uuid
from utils_preprocess import object_detection_show,style_transfer
from config import REULTS_FOLDER, OD_MODEL, OE_MODEL, TC_MODEL, CD_MODEL


# 目标检测
def infer_object_detection(image, model=OD_MODEL):
    # 将导出模型所在目录传入Predictor的构造方法中
    predictor = pdrs.deploy.Predictor(model)
    # img_file参数指定输入图像路径
    result = predictor.predict(img_file=image)
    fileName = '{}.png'.format(str(uuid.uuid4()))
    file = os.path.join(REULTS_FOLDER, fileName)
    fig = object_detection_show(image=image, result=result)
    fig.savefig(file)
    return fileName

# 目标提取
def infer_object_extraction(image, model=OE_MODEL):
    # 将导出模型所在目录传入Predictor的构造方法中
    predictor = pdrs.deploy.Predictor(model)
    # img_file参数指定输入图像路径
    result = predictor.predict(img_file=image)['label_map']
    fileName = '{}.png'.format(str(uuid.uuid4()))
    file = os.path.join(REULTS_FOLDER, fileName)
    Image.fromarray(np.array(result)*255).convert('RGB').save(file)
    return fileName

# 地物分类
def infer_image_classification(image, model=TC_MODEL):
    predictor = pdrs.deploy.Predictor(model)
    # img_file参数指定输入图像路径
    result = predictor.predict(img_file=image)['label_map']
    result = get_lut()[result]
    fileName = '{}.png'.format(str(uuid.uuid4()))
    file = os.path.join(REULTS_FOLDER, fileName)
    Image.fromarray(np.array(result)).save(file)
    return fileName

# 变化检测
def infer_change_detection(image1, image2, model=CD_MODEL):
    # 将导出模型所在目录传入Predictor的构造方法中
    predictor = pdrs.deploy.Predictor(model)
    # img_file参数指定输入图像路径
    result = predictor.predict(img_file=(image1, image2))[0]['label_map']
    fileName = '{}.png'.format(str(uuid.uuid4()))
    file = os.path.join(REULTS_FOLDER, fileName)
    Image.fromarray(np.array(result)*255).convert('RGB').save(file)
    return fileName

def get_lut():
    """
    用于语义分割结果上色
    :return:
    """
    lut = np.zeros((256,3), dtype=np.uint8)
    lut[0] = [255, 0, 0]
    lut[1] = [30, 255, 142]
    lut[2] = [60, 0, 255]
    lut[3] = [255, 222, 0]
    lut[4] = [0, 0, 0]
    return lut



if __name__ == '__main__':
    pass
    # object detection
    # image = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_detection\image\playground_108.jpg'
    # model = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_detection\model'
    # save_path = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_detection\infer_result'
    # infer_object_detection(image, model, save_path)
    
    # object extraction
    # image = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_extraction\image\img-1.png'
    # model = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_extraction\model'
    # save_path = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_extraction\infer_result'
    # infer_object_extraction(image, model, save_path)

    # image classification
    # image = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\terrain_classification\image\T004027.jpg'
    # model = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\terrain_classification\model'
    # save_path = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\terrain_classification\infer_result'
    # infer_image_classification(image, model, save_path)
    
    
    # change detection
    # image1 = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\change_detection\image_A\test_1.png'
    # image2 = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\change_detection\image_B\test_1.png'
    # model = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\change_detection\model\bit'
    # save_path = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\change_detection\infer_result'
    # infer_change_detection(image1,image2, model, save_path)
