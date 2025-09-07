import cv2
import cv2.aruco as aruco
import numpy as np
import os



marker_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)


marker_id = 42


marker_size = 500


output_image_name = f"aruco_marker_id_{marker_id}.png"

#crea y devuelve la imagen directamente.
marker_image = aruco.generateImageMarker(marker_dict, marker_id, marker_size)

# Guardar la imagen 
cv2.imwrite(output_image_name, marker_image)

print(f"¡Éxito! Se ha generado el marcador ArUco con ID {marker_id}.")
print(f"La imagen se guardó como: '{os.path.abspath(output_image_name)}'")

# Opcional: Mostrar la imagen generada
cv2.imshow("Marcador ArUco Generado", marker_image)
cv2.waitKey(0)
cv2.destroyAllWindows()