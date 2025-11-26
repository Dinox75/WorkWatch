import threading
import time
import sys
import json

from monitor.window_tracker import iniciar_monitoramento
from monitor.presence_detector import monitorar_presenca
from monitor.idle_tracker import monitorar_inatividade
from monitor.multitask_analyzer import monitorar_multitarefa


def main():
    stop_event = threading.Event()

    # Carregar configurações
    with open("config/config.json", "r") as f:
        config = json.load(f)

    threads = []

    # Iniciar monitor de janelas se estiver habilitado
    if config["window_tracker"]["enabled"]:
        t_janelas = threading.Thread(
            target=iniciar_monitoramento,
            args=(stop_event, config["window_tracker"]["interval_seconds"]),
            name="window_tracker"
        )
        threads.append(t_janelas)
        t_janelas.start()

    # Iniciar monitor de presença se estiver habilitado
    if config["presence_detector"]["enabled"]:
        t_presenca = threading.Thread(
            target=monitorar_presenca,
            args=(stop_event, config["presence_detector"]["interval_seconds"]),
            name="presence_detector"
        )
        threads.append(t_presenca)
        t_presenca.start()

    if config["idle_tracker"]["enabled"]:
        t_idle = threading.Thread(
            target=monitorar_inatividade,
            args=(stop_event, config["idle_tracker"]["interval_seconds"]),
            name="idle_tracker"
        )
        threads.append(t_idle)
        t_idle.start()

    if config["multitask_analyzer"]["enabled"]:
        t_multi = threading.Thread(
            target=monitorar_multitarefa,
            args=(stop_event, config["multitask_analyzer"]["interval_seconds"]),
            name="multitask_analyzer"
        )
        threads.append(t_multi)
        t_multi.start()

    try:
        print("WorkWatch rodando ... Pressione Ctrl+C para parar.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nParando WorkWatch...")
        stop_event.set()

        print("Aguardando threads terminarem...")
        for t in threads:
            t.join()

        print("WorkWatch parado com sucesso.")
        sys.exit(0)


if __name__ == "__main__":
    main()
