import threading
import time
import sys

from monitor.window_tracker import iniciar_monitoramento
from monitor.presence_detector import monitorar_presenca

def main():
    stop_event = threading.Event()

    #Inciar as threads de monitoramento
    t_janelas = threading.Thread(target=iniciar_monitoramento, args=(stop_event,))
    t_presenca = threading.Thread(target=monitorar_presenca, args=(stop_event,))

    t_janelas.start()
    t_presenca.start()

    try:
        print("WorkWatch rodando ... Pressione Ctrl+C para parar.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Parando WorkWatch...")
        stop_event.set()

        print("Aguardando threads terminarem...")
        t_janelas.join()
        t_presenca.join()

        print("WorkWatch parado com sucesso.")
        sys.exit(0)

if __name__ == "__main__":
    main()