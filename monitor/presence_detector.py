# --------------------------------------------------------
# WorkWatch - Módulo: presence_detector.py
# Função: Detectar presença do usuário via webcam
# --------------------------------------------------------

import cv2
from cvzone.FaceDetectionModule import FaceDetector

def detectar_presenca():
    # Força driver correto no Windows
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Verifica se a câmera abriu
    if not cap.isOpened():
        print("Erro: Webcam não pôde ser inicializada.")
        return False

    # Tenta capturar 1 frame
    success, img = cap.read()

    if not success:
        print("Erro: não foi possível capturar imagem da webcam.")
        cap.release()
        return False

    detector = FaceDetector()
    img, bboxs = detector.findFaces(img)

    cap.release()

    if bboxs and len(bboxs) > 0:
        return True
    else:
        return False


# 3. Função: monitorar_presenca()
#    - loop contínuo
#    - verifica presença em intervalos
#    - registra entradas e saídas
#    - (futuramente) salva logs

def monitorar_presenca():
    pass  # lógica será implementada depois
