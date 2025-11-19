# --------------------------------------------------------
# WorkWatch - Módulo: presence_detector.py
# Função: Detectar presença do usuário via webcam
# --------------------------------------------------------

import cv2
from cvzone.FaceDetectionModule import FaceDetector
import time
from monitor.window_tracker import salvar_linha  # reaproveitamos o sistema de logs
from datetime import datetime

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


def monitorar_presenca():
    status_anterior = None  # True = presente, False = ausente

    try:


        while True:
            status_atual = detectar_presenca()  # True ou False

            # Se houve mudança (True->False ou False->True)
            if status_atual != status_anterior:

                agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if status_atual is True:
                    evento = "PRESENTE"
                else:
                    evento = "AUSENTE"

                # montar linha CSV
                data, hora = agora.split(" ")
                linha = f"{data},{hora},EVENTO_PRESENCA,{evento}\n"

                # salvar evento
                salvar_linha(linha)

                # atualizar status
                status_anterior = status_atual

            time.sleep(10)  # verifica a cada 10 segundosis
    except KeyboardInterrupt:
        print("Monitoramento de presença interrompido pelo usuário.")