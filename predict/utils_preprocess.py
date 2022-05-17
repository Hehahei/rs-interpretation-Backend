# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 15:49
# @Author  : xuxing
# @Site    : 
# @File    : utils_preprocess.py
# @Software: PyCharm

import paddle
import numpy as np
import os
from tqdm import tqdm
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from paddlers.tasks.utils.visualize import visualize_detection


"""
fft变换
"""
def style_transfer(source_image, target_image):
    if type(source_image) == str:
        source_image = np.array(Image.open(source_image))
    if type(target_image) == str:
        target_image = np.array(Image.open(target_image))
    h, w, c = source_image.shape
    out = []
    for i in range(c):
        source_image_f = np.fft.fft2(source_image[:, :, i])
        source_image_fshift = np.fft.fftshift(source_image_f)
        target_image_f = np.fft.fft2(target_image[:, :, i])
        target_image_fshift = np.fft.fftshift(target_image_f)
        
        change_length = 1
        source_image_fshift[int(h / 2) - change_length:int(h / 2) + change_length,
        int(h / 2) - change_length:int(h / 2) + change_length] = \
            target_image_fshift[int(h / 2) - change_length:int(h / 2) + change_length,
            int(h / 2) - change_length:int(h / 2) + change_length]
        
        source_image_ifshift = np.fft.ifftshift(source_image_fshift)
        source_image_if = np.fft.ifft2(source_image_ifshift)
        source_image_if = np.abs(source_image_if)
        
        source_image_if[source_image_if > 255] = np.max(source_image[:, :, i])
        out.append(source_image_if)
    out = np.array(out)
    out = out.swapaxes(1, 0).swapaxes(1, 2)
    
    out = out.astype(np.uint8)
    return out


"""
目标检测模块画框和置信度
"""
def object_detection_show(image, result):
    def read_rgb(path):
        im = cv2.imread(path)
        im = im[..., ::-1]
        return im
    
    test_pic = image
    im = read_rgb(test_pic)
    
    def show_images_in_row(ims, fig, title='Det', lut=None):
        n = len(ims)
        fig.suptitle(title)
        ax = fig.subplots(nrows=1, ncols=n)
        # 去掉刻度线和边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        
        ax.imshow(ims[0])
    # 参考 https://stackoverflow.com/a/68209152
    fig = plt.figure(constrained_layout=True)
    fig.suptitle("Test Results")
    
    fig = plt.figure(constrained_layout=True)
    # 绘制目标框
    with paddle.no_grad():
        vis_res = []
        
        pred = result
        
        vis = im
        print(len(pred))
        # 用绿色画出预测目标框
        if len(pred) > 0:
            vis = visualize_detection(
                np.array(vis), pred,
                color=np.asarray([[0, 255, 0]], dtype=np.uint8),
                threshold=0.2, save_dir=None
            )
        vis_res.append(vis)
    show_images_in_row(vis_res, fig, title='')
    
    # 渲染结果
    fig.canvas.draw()
    Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    return fig


