import ultralytics
import cv2
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt

ultralytics.checks()

from ultralytics import YOLO

model = YOLO(r'C:\Users\user\OneDrive\桌面\GitHub\yolov8\best.pt')

img_path = r'C:\Users\user\OneDrive\桌面\GitHub\yolov8\biological_1.jpg'

results = model(img_path)

# results 通常是一個 list，此處假設只有一張影像
r = results[0]  
# r.boxes 中包含坐標、類別與信心度資料
boxes = r.boxes
# boxes.xyxy 包含邊框資訊
# boxes.conf 包含 confidence
# boxes.cls  包含 class id

data = []
for box in boxes:
    # box.xyxy 是一個 Tensor，形式為 [xmin, ymin, xmax, ymax]
    xyxy = box.xyxy.cpu().numpy().flatten().tolist()
    confidence = box.conf.item()
    class_id = int(box.cls.item())
    # 若想取得類別名稱，需要透過 model.names 或您的自訂 names
    class_name = model.names[class_id]

    data.append({
        'xmin': xyxy[0],
        'ymin': xyxy[1],
        'xmax': xyxy[2],
        'ymax': xyxy[3],
        'confidence': confidence,
        'class': class_id,
        'name': class_name
    })

    print("座標:", xyxy, "信心度:", confidence, "類別:", class_name)

df = pd.DataFrame(data)

# 載入原始影像 (BGR)
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"Image not found at {img_path}")

for i in range(len(df)):
    xmin = int(df.iloc[i]['xmin'])
    ymin = int(df.iloc[i]['ymin'])
    xmax = int(df.iloc[i]['xmax'])
    ymax = int(df.iloc[i]['ymax'])
    confidence = df.iloc[i]['confidence']
    class_name = df.iloc[i]['name']

    # 繪製偵測框（bounding box）
    color = (0, 255, 0)  # 綠色框線
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)

    # 標註文字 (類別名與信心度)
    label = f"{class_name} {confidence:.2f}"

    # 計算文字大小
    font_scale = 0.8  # 比預設大一點的字型
    thickness = 2
    (text_width, text_height), baseline = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
    )

    # 計算文字顯示位置：嘗試顯示在框內或框上方
    # 框的高度
    box_height = ymax - ymin

    # 如果框的高度大於文字高度＋額外空間，就顯示在框內
    # 否則顯示在框上方
    if box_height > (text_height + 10):
        # 顯示在框內：將文字背景畫在框的左上角內部
        text_bg_xmin = xmin
        text_bg_ymin = ymin
        text_bg_xmax = xmin + text_width
        text_bg_ymax = ymin + text_height + 10

        # 調整文字繪製座標(文字的左下角為基準)
        text_x = xmin
        text_y = ymin + text_height
    else:
        # 顯示在框上方：將文字背景畫在框上方，避免跑出圖片範圍
        text_bg_xmin = xmin
        text_bg_ymin = max(0, ymin - text_height - 10)
        text_bg_xmax = xmin + text_width
        text_bg_ymax = max(0, ymin - 10)

        text_x = xmin
        text_y = max(text_height, ymin - 5)

    # 畫背景條(黑色)
    cv2.rectangle(img, (text_bg_xmin, text_bg_ymin), (text_bg_xmax, text_bg_ymax), (0, 0, 0), -1)

    # 在背景條上印出文字(白色)
    cv2.putText(img, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
