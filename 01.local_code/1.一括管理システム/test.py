import os  
from pdf2image import convert_from_path
from pathlib import Path  
def pdf_to_images(pdf_path, output_folder): 
    # 出力フォルダが存在しない場合は作成する  
    if not os.path.exists(output_folder):  
        os.makedirs(output_folder)  
    # PDFファイルを画像に変換する  
    images = convert_from_path(pdf_path)  
    # 画像を保存する  
    for i, image in enumerate(images):  
        image_path = os.path.join(output_folder, f"page_{i+1}.jpg")  
        image.save(image_path, "JPEG")  
    print("変換が完了しました。")  

# PDFファイルのパスと出力フォルダのパスを指定する  
pdf_path = "C:/Users/10003061970/Desktop/AC100-649-0400F-01.pdf"  
output_folder = "output"  
# PDFを画像に変換する  
#pdf_to_images(pdf_path, output_folder) cv2.imwrite('C:/Users/10003061970/Desktop/re-moji.png', dst)

import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt

#1---画像読込み
img2 = cv2.imread("C:/Users/10003061970/Desktop/output/page_5.jpg")
img3 = cv2.imread("C:/Users/10003061970/Desktop/yousokutei7.png")
img4 = cv2.imread("C:/Users/10003061970/Desktop/yousokutei yoko.png")
# Cannyのエッジ検出
result = cv2.matchTemplate(img2, img3, cv2.TM_CCOEFF_NORMED)
result1 = cv2.matchTemplate(img2, img4, cv2.TM_CCOEFF_NORMED)
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
minVal1, maxVal1, minLoc1, maxLoc1 = cv2.minMaxLoc(result1)
print(f"max value: {maxVal}, position: {maxLoc}")
print(f"max value: {maxVal1}, position: {maxLoc1}")
ys, xs = np.where(result >= 0.8)
ys1, xs1 = np.where(result1 >= 0.8)

# 描画する。
dst = img2.copy()
for x, y in zip(xs, ys):
    cv2.rectangle(
        dst,
        (x, y),
        (x + img3.shape[1], y + img3.shape[0]),
        color=(0, 255, 0),
        thickness=2,
    )
for x, y in zip(xs1, ys1):
    cv2.rectangle(
        dst,
        (x, y),
        (x + img4.shape[1], y + img4.shape[0]),
        color=(0, 255, 0),
        thickness=2,
    )


#5---保存
cv2.imwrite('C:/Users/10003061970/Desktop/re-moji.png', dst)
