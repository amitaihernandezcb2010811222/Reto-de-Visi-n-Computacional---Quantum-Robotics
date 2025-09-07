import cv2
import cv2.aruco as aruco
import numpy as np


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)



while True:
    ret, frame = cap.read()
    if not ret:
        break

    corners, ids, rejected_img_points = detector.detectMarkers(frame)

    
    markers_found_info = []

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        
        
        for i, marker_id in enumerate(ids):
            
            marker_corners = corners[i][0]
            
            
            center_x = int(np.mean(marker_corners[:, 0]))
            center_y = int(np.mean(marker_corners[:, 1]))

            
            marker_data = {
                'id': marker_id[0],
                'posicion_x': center_x,
                'posicion_y': center_y
            }
            
            
            markers_found_info.append(marker_data)
            
            
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
            
    
    if markers_found_info:
        print("Marcadores encontrados en este fotograma:")
        print(markers_found_info)
        print("-" * 40)


    cv2.imshow("Detector Múltiple de ArUcos - Bonus", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#limpieza 
cap.release()
cv2.destroyAllWindows()