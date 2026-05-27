from app.models.material_data import MaterialData


class MaterialParser:

    @staticmethod
    def clean_value(value):

        if value is None:
            return ""

        return str(value).strip()

    @classmethod
    def parse_dataframe(cls, dataframe):

        materials = []

        for _, row in dataframe.iterrows():

            material = MaterialData(

                material=cls.clean_value(
                    row.get("MATERIAL", "")
                ),

                descricao=cls.clean_value(
                    row.get("TEXTO BREVE MATERIAL", "")
                ),

                composicao=cls.clean_value(
                    row.get("COMPOSIÇÃO", "")
                ),

                gramatura=cls.clean_value(
                    row.get("GRAMATURA FINAL", "")
                ),

                largura=cls.clean_value(
                    row.get(
                        "LARGURA PADRÃO DA MALHA",
                        ""
                    )
                )

            )

            materials.append(material)

        return materials