import time
from datetime import datetime
from monitor.window_tracker import obter_janela_ativa, salvar_linha


def analisar_multitarefa(historico):
    """
    Recebe uma lista com histórico recente de programas.
    Retorna um evento se detectar padrão de multitarefa.
    """

    # só começa a analisar quando tiver pelo menos 3 registros
    if len(historico) < 3:
        return None

    # --- TROCA RÁPIDA ---
    ultimas3 = historico[-3:]
    if len(set(ultimas3)) == 3:
        return "TROCA_RAPIDA"

    # --- OSCILAÇÃO ENTRE APPS (ABAB) ---
    if len(historico) >= 4:
        ultimas4 = historico[-4:]

        # deve haver apenas 2 apps diferentes
        if len(set(ultimas4)) == 2:
            a, b, c, d = ultimas4
            # padrão A B A B
            if a != b and a == c and b == d:
                return "OSCILACAO_ENTRE_APPS"

    return None


def monitorar_multitarefa(stop_event, interval):
    """
    Loop contínuo que analisa o histórico de programas usados.
    """
    historico = []     # últimos programas usados
    max_itens = 10     # manter apenas os últimos 10

    try:
        while not stop_event.is_set():

            janela = obter_janela_ativa()

            if janela:
                programa = janela.get("programa")

                if programa:
                    historico.append(programa)

                    # limitar histórico
                    if len(historico) > max_itens:
                        historico.pop(0)

                    # aplicar análise
                    evento = analisar_multitarefa(historico)
                    if evento:
                        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        data, hora = agora.split(" ")
                        linha = f"{data},{hora},EVENTO_MULTITAREFA,{evento}\n"
                        salvar_linha(linha)

            # respeitar intervalo configurado
            time.sleep(interval)

    except Exception as e:
        print(f"[monitorar_multitarefa] erro: {e}")

    finally:
        print("monitorar_multitarefa finalizado")
