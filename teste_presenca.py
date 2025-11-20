# tests/test_monitor_presenca_manual.py
import threading, time
from monitor.presence_detector import monitorar_presenca

stop = threading.Event()
t = threading.Thread(target=monitorar_presenca, args=(stop,))
t.start()
time.sleep(20)   # sente/levante/observar logs
stop.set()
t.join()
print("Teste de presence monitor finalizado")
