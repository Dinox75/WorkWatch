import time
from datetime import datetime
from monitor.window_tracker import salvar_linha

def analisar_multitarefa(historico):
    """
    Recebe uma lista com histórico recente de janelas.
    Retorna um evento se detectar padrão de multitarefa.
    """
    pass  # implementar depois

def monitorar_multitarefa(stop_event, interval):
    """
    Loop contínuo que analisa o histórico de janelas.
    """
    historico = []  # armazenar últimas janelas
    try:
        while not stop_event.is_set():
            # aqui vamos buscar as últimas janelas salvas
            # e aplicar a lógica de detecção
            time.sleep(interval)
    except Exception as e:
        print(f"[monitorar_multitarefa] erro: {e}")
    finally:
        print("monitorar_multitarefa finalizado")
