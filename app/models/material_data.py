from dataclasses import dataclass


@dataclass
class MaterialData:

    material: str = ""
    descricao: str = ""
    lote: str = ""
    composicao: str = ""
    gramatura: str = ""
    largura: str = ""
    codigo_barras: str = ""
    posicao: str = ""