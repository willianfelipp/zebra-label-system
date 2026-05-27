from pathlib import Path

from app.core.logger import logger


class ZPLGenerator:

    @staticmethod
    def generate_zpl(
        label_data,
        output_path
    ):

        logger.info(
            f"Gerando ZPL: "
            f"{label_data.material}"
        )

        zpl = f"""
^XA

^PW800
^LL650

^CF0,35

^FO30,20^FD ETIQUETA DE AMOSTRA^FS

^CF0,28

^FO30,90^FDMATERIAL: {label_data.material}^FS

^FO30,130^FDDESC: {label_data.denominacao}^FS

^FO30,170^FDLOTE: {label_data.lote}^FS

^FO30,210^FDPOSICAO: {label_data.posicao_deposito}^FS

^FO30,250^FDCOMPOSICAO: {label_data.composicao}^FS

^FO30,290^FDGRAMATURA: {label_data.gramatura}^FS

^FO420,290^FDLARGURA: {label_data.largura}^FS

^FO30,330^FDCOR: {label_data.descritivo_cor}^FS

^FO30,370^FDNOME: {label_data.nome_fantasia}^FS

^CF0,32

^FO30,430^FDQTD: {label_data.utilizacao_livre} {label_data.umb}^FS

^BY3,3,120

^FO90,470
^BCN,120,Y,N,N
^FD{label_data.codigo_barras}^FS

^FO2,2^GB796,646,3^FS

^XZ
"""

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(zpl)

        logger.info(
            f"Arquivo ZPL salvo: "
            f"{output_path}"
        )