# =============================================================================
# exporter.py
# Responsável por estruturar os dados coletados em um DataFrame Pandas
# e exportar o resultado final para um arquivo CSV.
# =============================================================================

import pandas as pd
from pathlib import Path


def exportar_csv(vagas: list[dict], caminho: str = "data/vagas.csv") -> None:
    """
    Recebe a lista de vagas, estrutura em um DataFrame e exporta para CSV.

    Args:
        vagas (list[dict]): Lista de dicionários com os dados das vagas
        caminho (str): Caminho de destino do arquivo CSV
    """

    # Garante que a pasta 'data/' existe antes de salvar
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)

    # Cria o DataFrame a partir da lista de dicionários
    df = pd.DataFrame(vagas)

    # Remove linhas completamente duplicadas (segurança)
    df = df.drop_duplicates()

    # Substitui valores N/A por vazio — mais limpo no CSV
    df = df.replace("N/A", "")

    # Exporta para CSV com encoding UTF-8 (suporte a acentos)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")

    print(f"[exporter] {len(df)} vagas exportadas para '{caminho}'")
    print(f"[exporter] Colunas: {list(df.columns)}")
    print(f"\n[exporter] Prévia dos dados:\n")
    print(df.head(5).to_string(index=False))