import cv2
import numpy as np
from IPython import display
from matplotlib import pyplot as plt
from scipy.spatial import Delaunay, delaunay_plot_2d, Voronoi, voronoi_plot_2d

cnt=0
last_x_point=0
last_y_point=0
points=[]
list_points=[]
def imshow(img, format=".jpg", **kwargs):
    """ndarray 配列をインラインで Notebook 上に表示する。
    """
    img = cv2.imencode(format, img)[1]
    img = display.Image(img, **kwargs)
    display.display(img)


# 画像を読み込む。
img = cv2.imread("test.png",-1)

# グレースケールに変換する。
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2値化する
ret, bin_img = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
# 輪郭を抽出する。
contours, hierarchy = cv2.findContours(
    bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# 小さい輪郭は誤検出として削除する
contours = list(filter(lambda x: cv2.contourArea(x) > 5000, contours))

# 輪郭を描画する。
cv2.drawContours(img, contours, -1, color=(0, 0, 255), thickness=2)

# 輪郭点の描画
for contour in contours:
    for point in contour:
        x_point=point[0][0]
        y_point=point[0][1]
        if (x_point < last_x_point-15 or x_point > last_x_point+15) or (y_point < last_y_point-15 or y_point > last_y_point+15):
            cv2.circle(img, point[0], 1, (0, 255, 0), 2)
            points.append((point[0]))
            #今回の座標を記憶
            last_x_point=point[0][0]
            last_y_point=point[0][1]
#内部点描写
height, width, ch = img.shape
for i in range(0,height,30):
    for j in range(0,width,30):
        #輪郭内に含まれてるか判定
        if cv2.pointPolygonTest(contour, (j, i), False) >= 0:
            cv2.circle(img,(j, i) , 1, (0, 255,0), 2)
            points.append(np.array([j,i],dtype = int))
#ドロネー三角形分割0
points=np.array(points)
tris = Delaunay(points)
tris=(points[tris.simplices])
for i in range(0,len(tris)):
    if abs(tris[i][0][0]-tris[i][1][0])>35 or abs(tris[i][0][0]-tris[i][2][0])>35 or abs(tris[i][1][0]-tris[i][2][0])>35 or abs(tris[i][0][1]-tris[i][1][1])>35 or abs(tris[i][0][1]-tris[i][2][1])>35 or abs(tris[i][1][1]-tris[i][2][1])>35:
        pass
    else:
        cv2.polylines(img, [tris[i]], True, (0, 255, 255), thickness=1)
imshow(img)

#アフィン変換
af = cv2.getAffineTransform(np.array([tris[0][0],tris[0][1],tris[0][2]],np.float32),np.array([tris[0][0],tris[0][1],(0,0)],np.float32))
affine_img_half = cv2.warpAffine(img,af,(width,height))
imshow(affine_img_half)