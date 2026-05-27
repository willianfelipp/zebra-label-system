import pandas as pd

from app.core.logger import logger


class ExcelReader:

    @staticmethod
    def read_excel(file_path, sheet_name):

        logger.info(f"Lendo arquivo: {file_path}")
        logger.info(f"Aba: {sheet_name}")

        try:

            dataframe = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                dtype=str
            )

            dataframe = dataframe.fillna("")

            # ==========================================
            # NORMALIZAR NOMES DAS COLUNAS
            # ==========================================

            dataframe.columns = (
                dataframe.columns
                .str.strip()
                .str.upper()
            )

            logger.info(
                f"Arquivo carregado com sucesso | "
                f"Linhas: {len(dataframe)}"
            )

            logger.info(
                f"Colunas encontradas: "
                f"{list(dataframe.columns)}"
            )

            return dataframe

        except Exception as error:

            logger.error(f"Erro ao ler Excel: {error}")

            raise