from app.core.logger import logger


class ExcelValidator:

    @staticmethod
    def validate_columns(dataframe, required_columns):

        missing_columns = []

        for column in required_columns:

            if column not in dataframe.columns:
                missing_columns.append(column)

        if missing_columns:

            logger.error(
                f"Colunas ausentes: {missing_columns}"
            )

            raise Exception(
                f"Colunas ausentes: {missing_columns}"
            )

        logger.info("Validação de colunas concluída")