import cv2

# URL del flujo de vídeo
url = 'URL'

# Captura el flujo de vídeo
cap = cv2.VideoCapture(url)

# Verifica si la captura se abrió correctamente
if not cap.isOpened():
    print("Error al abrir el flujo de vídeo")
    exit()

# Bucle para leer y mostrar el vídeo
while True:
    ret, frame = cap.read()  # Lee un frame del flujo de vídeo

    # Verifica si se pudo leer el frame
    if not ret:
        print("No se pudo recibir el frame. Finalizando...")
        break

    # Muestra el frame
    cv2.imshow('Video', frame)

    # Espera 1 milisegundo y verifica si se presiona la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()