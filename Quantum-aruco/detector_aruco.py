import cv2
import cv2.aruco as aruco
import numpy as np

def find_aruco_markers(frame, marker_dict, parameters):
    """
    Detecta marcadores ArUco en un frame de video y devuelve sus esquinas, IDs y centros.
    """
    # frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Para detectar los marcadores
    corners, ids, rejected = aruco.detectMarkers(gray, marker_dict, parameters=parameters)
    
    found_markers = []
    
    if ids is not None:
        # Para detectar marcadores detectados y calcular sus centros
        aruco.drawDetectedMarkers(frame, corners, ids)
        
        for i, corner_set in enumerate(corners):
            # Calcular el centro (x, y) del marcador
            c = corner_set[0]
            center_x = int(np.mean(c[:, 0]))
            center_y = int(np.mean(c[:, 1]))
            
            # Guardar la información en la lista 
            marker_info = {
                'id': ids[i][0],
                'center': (center_x, center_y),
                'corners': corner_set
            }
            found_markers.append(marker_info)
            
            # Dibujar el centro y el ID en el frame
            cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)
            cv2.putText(frame, f"ID: {ids[i][0]}", (center_x, center_y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
    return frame, found_markers

def provide_robot_instructions(frame_width, markers_list):
    """
    Imprime instrucciones de movimiento para el robot basadas en la posición de los marcadores.
    """
    if not markers_list:
        print("Instrucción: No se detectan marcadores. Buscando...")
        return
        
    print("\n--- Información de Marcadores Detectados ---")
    # Imprime la lista de diccionarios 
    print(f"Lista de marcadores: {markers_list}")

    # Para la instrucción de movimiento, nos basaremos en el primer marcador que se detecto
    first_marker = markers_list[0]
    center_x = first_marker['center'][0]
    
    frame_center = frame_width // 2
    
    # Definimos un umbral para considerar que el robot está "centrado"
    dead_zone = 50 
    
    instruction = ""
    if center_x < frame_center - dead_zone:
        instruction = f"Mover a la IZQUIERDA (Centro del ArUco en x={center_x})"
    elif center_x > frame_center + dead_zone:
        instruction = f"Mover a la DERECHA (Centro del ArUco en x={center_x})"
    else:
        instruction = f"¡Robot en el Centro! Completado (Centro del ArUco en x={center_x})"
        
    print(f"Instrucción: {instruction}\n")


if __name__ == "__main__":
    # Iniciar la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.")
        exit()
        
    # Configuración del diccionario y parámetros de ArUco
    marker_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters() 
    
    while True:
        # Leer un frame de la cámara
        ret, frame = cap.read()
        if not ret:
            print("No se pudo recibir el frame. Saliendo...")
            break
            
        # Obtener el ancho del frame para calcular el centro
        frame_height, frame_width, _ = frame.shape
        
        # Detectar marcadores ArUco
        processed_frame, detected_markers = find_aruco_markers(frame, marker_dict, parameters)
        
        # Imprimir las instrucciones en la consola
        provide_robot_instructions(frame_width, detected_markers)
        
        # Mostrar el frame con las detecciones
        cv2.imshow('Detector de ArUcos - Quantum Robotics Challenge', processed_frame)
        
        # Salir del bucle si se presiona la tecla 'a'
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break
            
    # Liberar la cámara y cerrar las ventanas
    cap.release()
    cv2.destroyAllWindows()