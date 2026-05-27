from app.core.logger import logger

from app.models.label_data import LabelData


class MergeEngine:

    @staticmethod
    def clean_value(value):

        if value is None:
            return ""

        return str(value).strip()

    @classmethod
    def create_lookup(cls, dataframe):

        lookup = {}

        for _, row in dataframe.iterrows():

            material = cls.clean_value(
                row.get("MATERIAL", "")
            )

            if material:

                lookup[material] = row

        return lookup

    @classmethod
    def merge_data(
        cls,
        zpp297_dataframe,
        zqmm004_dataframe
    ):

        labels = []

        logger.info(
            "Criando lookup da ZQMM004..."
        )

        zqmm_lookup = cls.create_lookup(
            zqmm004_dataframe
        )

        logger.info(
            f"Lookup criado: "
            f"{len(zqmm_lookup)} materiais"
        )

        logger.info(
            "Iniciando merge dos dados..."
        )

        for index, row in zpp297_dataframe.iterrows():

            material = cls.clean_value(
                row.get("MATERIAL", "")
            )

            lote = cls.clean_value(
                row.get("LOTE", "")
            )

            # Ignorar linhas vazias
            if not material or not lote:

                logger.warning(
                    f"Linha ignorada: {index + 2}"
                )

                continue

            complemento = zqmm_lookup.get(material)

            material_encontrado = (
                complemento is not None
            )

            if not material_encontrado:

                logger.warning(
                    f"Material não encontrado "
                    f"na ZQMM004: {material}"
                )

            label = LabelData(

                # ==========================
                # ZPP297
                # ==========================

                material=material,

                lote=lote,

                denominacao=cls.clean_value(
                    row.get("DENOMINAÇÃO", "")
                ),

                utilizacao_livre=cls.clean_value(
                    row.get("UTIL. LIVRE", "")
                ),

                umb=cls.clean_value(
                    row.get("UMB", "")
                ),

                utilizacao_kg=cls.clean_value(
                    row.get("UTIL. LIVRE(KG)", "")
                ),

                utilizacao_m=cls.clean_value(
                    row.get("UTIL. LIVRE(M)", "")
                ),

                codigo_barras=cls.clean_value(
                    row.get("CÓD. BARRAS", "")
                ),

                posicao_deposito=cls.clean_value(
                    row.get("POS.DEPÓSITO", "")
                ),

                ud=cls.clean_value(
                    row.get("U.D.", "")
                ),

                # ==========================
                # ZQMM004
                # ==========================

                composicao=(
                    cls.clean_value(
                        complemento.get(
                            "COMPOSIÇÃO",
                            ""
                        )
                    )
                    if complemento is not None
                    else ""
                ),

                largura=(
                    cls.clean_value(
                        complemento.get(
                            "LARGURA PADRÃO DA MALHA",
                            ""
                        )
                    )
                    if complemento is not None
                    else ""
                ),

                gramatura=(
                    cls.clean_value(
                        complemento.get(
                            "GRAMATURA",
                            ""
                        )
                    )
                    if complemento is not None
                    else ""
                ),

                descritivo_cor=(
                    cls.clean_value(
                        complemento.get(
                            "DESCRITIVO DA COR",
                            ""
                        )
                    )
                    if complemento is not None
                    else ""
                ),

                nome_fantasia=(
                    cls.clean_value(
                        complemento.get(
                            "NOME FANTASIA",
                            ""
                        )
                    )
                    if complemento is not None
                    else ""
                ),

                material_encontrado=material_encontrado
            )

            labels.append(label)

        logger.info(
            f"Etiquetas geradas: {len(labels)}"
        )

        return labels