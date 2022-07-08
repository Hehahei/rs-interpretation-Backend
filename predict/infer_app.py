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
from predict.utils_preprocess import object_detection_show,style_transfer
from config import REULTS_FOLDER, OD_MODEL, OE_MODEL, TC_MODEL, CD_MODEL
import paddle

paddle.device.set_device(device='gpu')


def filter_threshold(result,threshold:0.5):
    result = [x for x in result if x['score']>threshold]
    return result


def image32_24(image):
    path = image
    image = np.array(Image.open(image).convert('RGB'))
    Image.fromarray(image).save(path)


# 目标检测
def infer_object_detection(image, model=OD_MODEL):
    # 将导出模型所在目录传入Predictor的构造方法中
    predictor = pdrs.deploy.Predictor(model)
    # img_file参数指定输入图像路径
    result = predictor.predict(img_file=image,warmup_iters=10)
    result = filter_threshold(result,threshold=0.5)
    fileName = '{}.png'.format(str(uuid.uuid4()))
    file = os.path.join(REULTS_FOLDER, fileName)
    fig = object_detection_show(image=image, result=result)
    fig.savefig(file,bbox_inches = 'tight',dpi=fig.dpi,pad_inches = 0)#去除白边
    return fileName

# 目标提取
def infer_object_extraction(image, model=OE_MODEL):
    # 将导出模型所在目录传入Predictor的构造方法中
    image32_24(image)
    predictor = pdrs.deploy.Predictor(model)
    # img_file参数指定输入图像路径
    result = predictor.predict(img_file=image,warmup_iters=10)['label_map']
    fileName = '{}.png'.format(str(uuid.uuid4()))
    file = os.path.join(REULTS_FOLDER, fileName)
    Image.fromarray(np.array(result)*255).convert('RGB').save(file)
    return fileName

# 地物分类
def infer_image_classification(image, model=TC_MODEL):
    image32_24(image)
    predictor = pdrs.deploy.Predictor(model)
    # img_file参数指定输入图像路径
    result = predictor.predict(img_file=image,warmup_iters=10)['label_map']
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
    result = predictor.predict(img_file=(image1, image2),warmup_iters=10)[0]['label_map']
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
    image = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend\playground.png'
    model = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_detection\model'
    # save_path = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_detection\infer_result'
    # image32_24(r'C:\Users\xuxing\Desktop\road.png')
    infer_object_detection(image, model)
    
    # object extraction
    # image = r'C:\Users\xuxing\Desktop\road.png'
    # model = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_extraction\model'
    # save_path = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\object_extraction\infer_result'
    # infer_object_extraction(image, model)

    # image classification
    # image = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\terrain_classification\image\T004027.jpg'
    # model = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\terrain_classification\model'
    # save_path = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\terrain_classification\infer_result'
    # infer_image_classification(image, model)
    
    
    # change detection
    # image1 = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\change_detection\image_A\test_1.png'
    # image2 = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\change_detection\image_B\test_1.png'
    # model = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\change_detection\model\bit'
    # save_path = r'D:\master\competetion\20220503baidu_proj\rs-interpretation-Backend-main\app\blues\change_detection\infer_result'
    # infer_change_detection(image1,image2, model)
