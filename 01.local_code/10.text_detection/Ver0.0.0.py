import cv2  
import matplotlib.pyplot as plt  
import numpy as np  
  
def find_least_keypoints_region(img, keypoints, face_rects, grid_size=(16, 16)):  
    h, w = img.shape[:2]  # 画像の高さと幅を取得  
    grid_h, grid_w = h // grid_size[0], w // grid_size[1]  
      
    # グリッドごとの特徴点数をカウント  
    keypoint_counts = np.zeros(grid_size, dtype=int)  
    for kp in keypoints:  
        x, y = int(kp.pt[0]), int(kp.pt[1])  
        grid_x = min(x // grid_w, grid_size[1] - 1)  # インデックスが範囲を超えないように調整  
        grid_y = min(y // grid_h, grid_size[0] - 1)  # インデックスが範囲を超えないように調整  
        keypoint_counts[grid_y, grid_x] += 1  
      
    # 特徴点が5個以下のグリッドを取得  
    valid_grids = np.argwhere(keypoint_counts <= 5)  
      
    # 顔に最も近いグリッドを見つける（顔にかぶらないように）  
    min_dist = float('inf')  
    best_grid = None  
    for grid in valid_grids:  
        grid_y, grid_x = grid  
        grid_center = np.array([grid_x * grid_w + grid_w // 2, grid_y * grid_h + grid_h // 2])  
        face_overlap = False  
        for (x, y, w, h) in face_rects:  
            if (grid_x * grid_w < x + w and grid_x * grid_w + grid_w > x and  
                grid_y * grid_h < y + h and grid_y * grid_h + grid_h > y):  
                face_overlap = True  
                break  
  
        if face_overlap:  
            continue  
          
        for (x, y, w, h) in face_rects:  
            face_center = np.array([x + w // 2, y + h // 2])  
            dist = np.linalg.norm(grid_center - face_center)  
            if dist < min_dist:  
                min_dist = dist  
                best_grid = grid  
  
    return best_grid, grid_w, grid_h  
  
def place_text_in_least_keypoints_region(img, text, keypoints, face_rects, grid_size=(16, 16)):  
    min_count_idx, grid_w, grid_h = find_least_keypoints_region(img, keypoints, face_rects, grid_size)  
    if min_count_idx is None:  
        print("No suitable region found.")  
        return img  
    grid_x, grid_y = min_count_idx[1], min_count_idx[0]  
    x, y = grid_x * grid_w, grid_y * grid_h  
  
    # テキストのサイズを取得  
    font = cv2.FONT_HERSHEY_SIMPLEX  
    font_scale = 1  
    thickness = 2  
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]  
  
    # テキストが描画範囲外に行かないように調整  
    text_x = x + (grid_w - text_size[0]) // 2  
    text_y = y + (grid_h + text_size[1]) // 2  
      
    if text_x < 0:  
        text_x = 0  
    elif text_x + text_size[0] > img.shape[1]:  
                text_x = img.shape[1] - text_size[0]  
          
    if text_y < text_size[1]:  
        text_y = text_size[1]  
    elif text_y > img.shape[0]:  
        text_y = img.shape[0]  
  
    # テキストを描画  
    cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 0, 0), thickness, lineType=cv2.LINE_AA)  
    return img  
  
# 顔検出用のHaar Cascadeをロード  
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  
  
# 画像の読み込み  
img = cv2.imread('test.jpg')  
  
# 顔検出  
faces = face_cascade.detectMultiScale(img, scaleFactor=1.05, minNeighbors=5, minSize=(50, 50))  
  
# SIFT検出器の作成  
sift = cv2.SIFT_create()  
  
# 特徴点の検出  
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
keypoints, descriptors = sift.detectAndCompute(gray, None)  
  
# 特徴点を画像上に描画  
img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))  
  
# 顔領域を矩形で描画  
for (x, y, w, h) in faces:  
    cv2.rectangle(img_with_keypoints, (x, y), (x + w, y + h), (255, 0, 0), 2)  
  
# 特徴点が5個以下かつ顔に最も近い領域にテキストを配置  
text = "yu"  
img_with_text = place_text_in_least_keypoints_region(img_with_keypoints, text, keypoints, faces, grid_size=(16, 16))  
  
# 結果を表示  
plt.imshow(cv2.cvtColor(img_with_text, cv2.COLOR_BGR2RGB))  
plt.axis('off')  
plt.show()  