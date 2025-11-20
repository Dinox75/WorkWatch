# tests/test_iniciar_monitoramento_manual.py (exemplo)
import threading, time
from monitor.window_tracker import iniciar_monitoramento

stop = threading.Event()

t = threading.Thread(target=iniciar_monitoramento, args=(stop,))
t.start()

# deixa rodar 12 segundos
time.sleep(12)
stop.set()  # sinaliza encerramento
t.join()
print("Teste de window tracker finalizado")
