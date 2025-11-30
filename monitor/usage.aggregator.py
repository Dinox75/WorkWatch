from datetime import datetime
import csv
import os

class UsageAggregator:
    def __init__(self):
        self.programa_atual = None       # programa atualmente em uso
        self.hora_inicial = None         # quando começamos a usar esse programa
        self.tempo_total = {}            # dicionário: programa -> segundos acumulados

    def trocar_janela(self, novo_programa):
        agora = datetime.now()

        #  Se já havia um programa ativo, calcula o tempo gasto nele

        if self.programa_atual is not None and self.hora_inicial is not None:
            tempo_decorrido = (agora - self.hora_inicial).total_seconds()

            # Soma no acumulador do programa
            if self.programa_atual not in self.tempo_total:
                self.tempo_total[self.programa_atual] = 0

            self.tempo_total[self.programa_atual] += tempo_decorrido

                #  Atualiza para o novo programa
        self.programa_atual = novo_programa
        self.hora_inicial = agora

    def salvar_resumo(self):
        """
        Salva os tempos acumulados em storage/usage_summary.csv
        Cada linha: data, hora, programa, tempo_em_segundos
        """

        caminho = "storage/usage_summary.csv"
        arquivo_existe = os.path.exists(caminho)

        with open(caminho, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Cabeçalho só na criação do arquivo
            if not arquivo_existe:
                writer.writerow(["data", "hora", "programa", "tempo_segundos"])

            agora = datetime.now()
            data = agora.strftime("%Y-%m-%d")
            hora = agora.strftime("%H:%M:%S")

            for programa, tempo in self.tempo_total.items():
                writer.writerow([data, hora, programa, int(tempo)])
