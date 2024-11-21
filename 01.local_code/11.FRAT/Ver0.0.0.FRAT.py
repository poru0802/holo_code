#20241108 Ver0.0.0 メインプログラム作成
import cv2
import torch
import numpy as np
import sys

sys.path.append("C:/Users/10003061970/Desktop/2.コード一覧/11.FRAT/train_log")  
from ECCV2022_RIFE_arxiv_v5_code.model.RIFE_HDv2 import Model 

def interpolate_video(input_video_path,output_video_path):
    model=Model()
    model.load_model("C:/Users/10003061970/Desktop/2.コード一覧/11.FRAT/train_log",1)
    model.eval()
    device = torch.device('cpu')  
    model.device(device) 

    cap=cv2.VideoCapture(input_video_path)
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    fps=int(cap.get(cv2.CAP_PROP_FPS))
    width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    heigt=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out=cv2.VideoWriter(output_video_path,fourcc,fps*2,(width,heigt))

    ret,frame1=cap.read()
    while ret:
        ret,frame2=cap.read()
        if not ret:
            break
        frame1_t=torch.from_numpy(frame1).permute(2,0,1).unsqueeze(0).float()/255.
        frame2_t=torch.from_numpy(frame2).permute(2,0,1).unsqueeze(0).float()/255.
        with torch.no_grad():
            mid_frame_t=model.inference(frame1_t.to(model.device),frame2_t.to(model.device)).cpu()
        mid_frame=(mid_frame_t.squeeze().permute(1,2,0).numpy()*255.).astype(np.uint8)
        out.write(frame1)
        out.write(mid_frame)
        frame1=frame2
    out.release()
    cap.release()
input_video='C:/Users/10003061970/Desktop/2.コード一覧/11.FRAT/test.MTS'
output_video='C:/Users/10003061970/Desktop/2.コード一覧/11.FRAT/out_put.mp4'
interpolate_video(input_video,output_video)