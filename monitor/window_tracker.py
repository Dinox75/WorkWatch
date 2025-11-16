#   WorkWatch - Módulo: window_tracker.py
#   Função: Monitorar a janela ativa do computador

# 1. Importar bibliotecas necessárias
import pygetwindow as gw
import win32process
import psutil
from datetime import datetime
import time


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

def salvar_linha(linha):
    with open("storage/logs.csv", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)
    


# 4. Função principal: iniciar_monitoramento()
#    - Loop contínuo
#    - A cada X segundos:
#         * chama obter_janela_ativa()
#         * envia os dados para registrar_janela()
#    - Não implementaremos o loop ainda, só deixamos a estrutura

def iniciar_monitoramento():
    pass  
