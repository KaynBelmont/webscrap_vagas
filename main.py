# =============================================================================
# main.py
# Ponto de entrada do projeto. Orquestra o scraper, parser e exporter.
# Execute este arquivo para rodar o projeto completo:
#   python main.py
# =============================================================================

from src.scraper  import buscar_pagina
from src.parser   import extrair_vagas
from src.exporter import exportar_csv


def main():
    # -------------------------------------------------------------------------
    # Configurações da coleta
    # -------------------------------------------------------------------------
    TERMO_BUSCA  = "python"   # Termo pesquisado no Vagas.com.br
    TOTAL_PAGINAS = 3         # Número de páginas a coletar (cada página tem ~40 vagas)
    ARQUIVO_CSV  = "data/vagas.csv"

    print("=" * 55)
    print("   Vagas Scraper — Vagas.com.br")
    print("=" * 55)

    todas_vagas = []

    # Percorre cada página de resultados
    for pagina in range(1, TOTAL_PAGINAS + 1):
        print(f"\n[main] Coletando página {pagina} de {TOTAL_PAGINAS}...")
        html  = buscar_pagina(TERMO_BUSCA, pagina)
        vagas = extrair_vagas(html)
        todas_vagas.extend(vagas)

    print(f"\n[main] Total coletado: {len(todas_vagas)} vagas")

    # Exporta tudo para CSV
    exportar_csv(todas_vagas, ARQUIVO_CSV)

    print("\n" + "=" * 55)
    print("   Coleta finalizada com sucesso!")
    print("=" * 55)


if __name__ == "__main__":
    main()