from dataclasses import dataclass


@dataclass
class LabelData:

    # ==========================================
    # ZPP297
    # ==========================================

    material: str = ""
    lote: str = ""

    denominacao: str = ""

    utilizacao_livre: str = ""
    umb: str = ""

    utilizacao_kg: str = ""
    utilizacao_m: str = ""

    codigo_barras: str = ""

    posicao_deposito: str = ""

    ud: str = ""

    # ==========================================
    # ZQMM004
    # ==========================================

    composicao: str = ""

    largura: str = ""

    gramatura: str = ""

    descritivo_cor: str = ""

    nome_fantasia: str = ""

    # ==========================================
    # CONTROLE
    # ==========================================

    material_encontrado: bool = True