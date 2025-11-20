# --------------------------------------------------------
# WorkWatch - Módulo: presence_detector.py
# Função: Detectar presença do usuário via webcam
# --------------------------------------------------------

import cv2
from cvzone.FaceDetectionModule import FaceDetector
import time
from monitor.window_tracker import salvar_linha                                     # reaproveitamos o sistema de logs
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

# Monitora presença via webcam; registra apenas quando houver mudança.
# stop_event: threading.Event para parada limpa.

def monitorar_presenca(stop_event, interval):
    status_anterior = None                                                  # True = presente, False = ausente

    try:


        while not stop_event.is_set():
            status_atual = detectar_presenca()                              # True ou False

            # Se houve mudança (True->False ou False->True)
            if status_atual != status_anterior:
                agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data, hora = agora.split(" ")
                evento = "PRESENTE" if status_atual else "AUSENTE"
                linha = f"{data},{hora},EVENTO_PRESENCA,{evento}\n"
                salvar_linha(linha)
                status_anterior = status_atual

            total_wait = 10
            step = 1
            waited = 0
            while waited < total_wait:
                if stop_event.is_set():
                    break
                time.sleep(step)
                waited += step
            
    except Exception as e:
        print(f"[monitorar_presenca] erro: {e}")
    finally:
        print("monitorar_presenca finalizado")