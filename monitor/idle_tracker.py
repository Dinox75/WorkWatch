import time
import ctypes
from datetime import datetime
from monitor.window_tracker import salvar_linha

def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)
    
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info)):
        millis = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime
        return millis / 1000  # segundos
    else:
        return 0

def monitorar_inatividade(stop_event, interval):
    estava_inativo = False

    try:
        while not stop_event.is_set():
            idle_seconds = get_idle_time()

            # se passou de 60 segundos → está inativo
            inativo_agora = idle_seconds >= 60

            if inativo_agora != estava_inativo:
                agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data, hora = agora.split(" ")

                evento = "INATIVO" if inativo_agora else "ATIVO"

                linha = f"{data},{hora},EVENTO_INATIVIDADE,{evento}\n"
                salvar_linha(linha)

                estava_inativo = inativo_agora

            # aguarda intervalo (configurável)
            time.sleep(interval)

    except Exception as e:
        print(f"[monitorar_inatividade] erro: {e}")
    finally:
        print("monitorar_inatividade finalizado")
