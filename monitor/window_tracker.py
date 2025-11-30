#   WorkWatch - Módulo: window_tracker.py
#   Função: Monitorar a janela ativa do computador

# 1. Importar bibliotecas necessárias
import pygetwindow as gw
import win32process
import psutil
from datetime import datetime
import time
from monitor.app_classifier import classificar_programa, registrar_classificacao

#Função para obter a janela ativa
def obter_janela_ativa():
    if janela_ativa := gw.getActiveWindow():                        #Verifica se há uma janela ativa 
        hadle = janela_ativa._hWnd                                  #Obtém o handle da janela ativa
        _, pid = win32process.GetWindowThreadProcessId(hadle)       #Obtém o ID do processo associado à janela ativa
        processo = psutil.Process(pid)                              #Obtém o processo usando o ID
        nome_programa = processo.name()                             #Obtém o nome do programa associado ao processo 
        return {
            "titulo": janela_ativa.title,
            "programa": nome_programa
        }
    return None


# 3. Função: registrar_janela()
def registrar_janela(info_janela):
    agora = datetime.now()
    texto = agora.strftime("%Y-%m-%d %H:%M:%S")
    data, hora = texto.split(" ")
    linha = f"{data},{hora},{info_janela['titulo']},{info_janela['programa']}\n"
    return linha


# 4. Função: salvar_linha()
def salvar_linha(linha):
    with open("storage/logs.csv", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)
    

# 5. Função: iniciar_monitoramento()
def iniciar_monitoramento(stop_event, interval):
    janela_anterior = None  # Armazena a última janela registrada

    try:
        while not stop_event.is_set():
            janela_atual = obter_janela_ativa()  # Obtém a janela ativa agora

            # Se a janela mudou, registra no log
            if janela_atual is not None and janela_atual != janela_anterior:
                # 1. Registrar a janela ativa
                linha = registrar_janela(janela_atual)
                salvar_linha(linha)

                # 2. Classificar o programa detectado
                programa = janela_atual.get("programa")
                if programa:  # só tenta classificar se existir nome válido
                    registrar_classificacao(programa)

                # Atualizar referência da janela anterior
                janela_anterior = janela_atual

            # Delay com verificação contínua de stop_event
            total_wait = interval
            step = 0.5
            waited = 0

            while waited < total_wait:
                if stop_event.is_set():
                    break
                time.sleep(step)
                waited += step

    except Exception as e:
        print(f"[iniciar_monitoramento] Ocorreu um erro: {e}")
    finally:
        print("iniciar_monitoramento finalizado.")