import cv2  # importamos el modulo de Opencv
import numpy as np  # Importamos el modulo que permite in mejor manejo del rango de colores
import pyttsx3  # Importamos el modulo que permite hablar la parte del texto

engine = pyttsx3.init()#Iniciamos el motor de texto a voz ofline

def dibujar(mask, color):  # Funcion que dibuja a partir de los parametros dados
    contornos, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contornos:  # Permite definir el rango del obj. para eliminar particulas del mismo color
        area = cv2.contourArea(c)
        if area > 2000:
            nuevoContorno = cv2.convexHull(c)
            # Dibuja el contorno del color
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)

            # Menciona el color que se esta capturando en ese momento
            if color == (255, 0, 0):
                engine.say('::: Azul')

            if color == (0, 255, 0):
                engine.say('::: Verde')

            if color == (0, 0, 255):
                engine.say('::: Rojo')
            engine.runAndWait()  # Ejecuta el motor de voz


# Entrada de video, Es streaming que permite ver la camara web
cap = cv2.VideoCapture(0)

# Rango del color azul que va a detectar la camara
Azul0 = np.array([100, 100, 20], np.uint8)
Azul1 = np.array([110, 255, 255], np.uint8)

# Rango del color verde que va a detectar la camara
Verde0 = np.array([35, 100, 20], np.uint8)
Verde1 = np.array([85, 255, 255], np.uint8)

# Rango del color rojo que va a detectar la camara
Rojo00 = np.array([0, 100, 20], np.uint8)
Rojo11 = np.array([5, 255, 255], np.uint8)
Rojo0 = np.array([175, 100, 20], np.uint8)
Rojo1 = np.array([179, 255, 255], np.uint8)


while True:
    ret, frame = cap.read()

    if ret == True:
        # convierte los colores de BGR a HSV(Permite mejor optencion del color)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        maskRed1 = cv2.inRange(frameHSV, Rojo00, Rojo11)
        maskRed2 = cv2.inRange(frameHSV, Rojo0, Rojo1)

        ElAzul = cv2.inRange(frameHSV, Azul0, Azul1)
        ElVerde = cv2.inRange(frameHSV, Verde0, Verde1)
        ElRojo = cv2.add(maskRed1, maskRed2)

        # Se invoca la funcion que dibuja y se le agrega el color color
        dibujar(ElAzul, (255, 0, 0))  # BGR

        dibujar(ElVerde, (0, 255, 0))

        dibujar(ElRojo, (0, 0, 255))

        cv2.imshow('Detector de RGB', frame)  # Titulo de laventana a mostrar

        # Boton de panico que termina la ejecucion del programa
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
