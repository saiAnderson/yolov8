import cv2
from ultralytics import YOLO

model = YOLO(r"C:\Users\user\OneDrive\桌面\GitHub\yolov8\best.pt")

# 開啟攝影機 (0 為預設攝影機，若您有多個攝影機可嘗試 1, 2 ...)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("無法開啟攝影機")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("無法從攝影機讀取影像")
        break
    
    # 使用 YOLOv8 推論該幀影像
    # 注意：直接丟 frame (numpy 陣列) 進 YOLO 進行推論
    results = model(frame)

    # YOLOv8 的推論結果為一個列表，對於單張影像結果取 results[0]
    r = results[0]
    boxes = r.boxes

    # 在影像上繪製偵測結果
    for box in boxes:
        # 取得座標與分類資訊
        xyxy = box.xyxy.cpu().numpy().flatten().tolist()
        confidence = box.conf.item()
        class_id = int(box.cls.item())
        class_name = model.names[class_id]

        xmin, ymin, xmax, ymax = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])

        # 繪製框線
        color = (0, 255, 0)
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)

        # 標註文字
        label = f"{class_name} {confidence:.2f}"
        (text_width, text_height), baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )

        # 顯示在框線上方(如有需要可調整)
        cv2.rectangle(frame, (xmin, ymin - text_height - 10), 
                      (xmin + text_width, ymin), color, -1)
        cv2.putText(frame, label, (xmin, ymin - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # 顯示結果影像
    cv2.imshow("Real-Time Detection", frame)

    # 按下 'q' 離開
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
