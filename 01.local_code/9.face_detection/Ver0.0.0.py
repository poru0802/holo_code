import cv2  
import os  
  
# Haar Cascadeファイルのパスを設定  
face_cascade_path = './haarcascade_frontalcatface_extended.xml'  
# パスが存在するか確認  
if not os.path.exists(face_cascade_path):  
    raise FileNotFoundError(f"Haar Cascade file not found at {face_cascade_path}")  
# Haar Cascadeを読み込む  
face_cascade = cv2.CascadeClassifier(face_cascade_path)  
# 画像を読み込む  
src = cv2.imread('./test.jpg')  
if src is None:  
    raise FileNotFoundError("Image file not found or could not be read.")  
# 画像をグレースケールに変換  
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  
# 顔を検出  
faces = face_cascade.detectMultiScale(src_gray, scaleFactor=1.01, minNeighbors=10, minSize=(30, 30))  
print(faces)
# 顔に矩形を描画  
for (x, y, w, h) in faces:  
    cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 2)  
  
# 結果を保存  
output_path = './opencv_face_detect_rectangle.jpg'  
os.makedirs(os.path.dirname(output_path), exist_ok=True)  
cv2.imwrite(output_path, src)  
  
print(f"Detection completed. Results saved to {output_path}")  