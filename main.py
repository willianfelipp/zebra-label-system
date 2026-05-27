from pathlib import Path

from app.config.settings import APP_NAME
from app.core.logger import logger

from app.engines.excel.excel_reader import ExcelReader
from app.engines.excel.excel_validator import ExcelValidator
from app.engines.excel.merge_engine import MergeEngine

from app.engines.preview.label_renderer import LabelRenderer

from app.engines.pdf.pdf_generator import PDFGenerator

from app.engines.zpl.zpl_generator import ZPLGenerator

def main():

    logger.info("=" * 60)
    logger.info(f"{APP_NAME} iniciado")
    logger.info("=" * 60)

    try:

        # ==================================================
        # GARANTE PASTAS NECESSÁRIAS
        # ==================================================

        export_folder = Path(
            "storage/exports"
        )

        temp_folder = Path(
            "storage/temp"
        )

        export_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        temp_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(
            "Pastas verificadas com sucesso"
        )

        # ==================================================
        # ARQUIVOS DE TESTE
        # ==================================================

        zpp297_file = Path(
            "storage/test_files/ZPP297.xlsx"
        )

        zqmm004_file = Path(
            "storage/test_files/ZQMM004.xlsx"
        )

        # ==================================================
        # VALIDA EXISTÊNCIA DOS ARQUIVOS
        # ==================================================

        if not zpp297_file.exists():

            raise FileNotFoundError(
                f"Arquivo não encontrado: "
                f"{zpp297_file}"
            )

        if not zqmm004_file.exists():

            raise FileNotFoundError(
                f"Arquivo não encontrado: "
                f"{zqmm004_file}"
            )

        logger.info(
            "Arquivos localizados com sucesso"
        )

        # ==================================================
        # LEITURA DOS EXCELS
        # ==================================================

        zpp297_dataframe = ExcelReader.read_excel(
            file_path=zpp297_file,
            sheet_name="Sheet1"
        )

        zqmm004_dataframe = ExcelReader.read_excel(
            file_path=zqmm004_file,
            sheet_name="Sheet1"
        )

        # ==================================================
        # VALIDAÇÃO DE COLUNAS
        # ==================================================

        ExcelValidator.validate_columns(
            zpp297_dataframe,
            [
                "MATERIAL",
                "LOTE",
                "DENOMINAÇÃO",
                "CÓD. BARRAS"
            ]
        )

        ExcelValidator.validate_columns(
            zqmm004_dataframe,
            [
                "MATERIAL"
            ]
        )

        logger.info(
            "Validação de colunas concluída"
        )

        # ==================================================
        # PROCESSAMENTO / MERGE
        # ==================================================

        labels = MergeEngine.merge_data(
            zpp297_dataframe,
            zqmm004_dataframe
        )

        # ==================================================
        # VALIDA RESULTADO
        # ==================================================

        if not labels:

            logger.warning(
                "Nenhuma etiqueta foi gerada"
            )

            return

        logger.info(
            f"Etiquetas geradas: {len(labels)}"
        )

        # ==================================================
        # EXIBE PRIMEIRAS ETIQUETAS
        # ==================================================

        print("\n" + "=" * 60)
        print("ETIQUETAS GERADAS")
        print("=" * 60)

        for index, label in enumerate(
            labels[:5],
            start=1
        ):

            print(f"\nETIQUETA {index}")
            print("-" * 40)

            print(
                f"MATERIAL: "
                f"{label.material}"
            )

            print(
                f"LOTE: "
                f"{label.lote}"
            )

            print(
                f"DESCRIÇÃO: "
                f"{label.denominacao}"
            )

            print(
                f"QTD: "
                f"{label.utilizacao_livre} "
                f"{label.umb}"
            )

            print(
                f"CÓDIGO BARRAS: "
                f"{label.codigo_barras}"
            )

        # ==================================================
        # LIMPA EXPORTS ANTIGOS
        # ==================================================

        logger.info(
            "Removendo arquivos antigos..."
        )

        for old_file in export_folder.glob("*.png"):

            try:

                old_file.unlink()

            except Exception as error:

                logger.warning(
                    f"Erro ao remover arquivo: "
                    f"{old_file} | {error}"
                )

        # ==================================================
        # GERA TODAS ETIQUETAS
        # ==================================================

        logger.info(
            "Iniciando geração das etiquetas..."
        )

                # ==================================================
        # GERA ARQUIVOS ZPL
        # ==================================================

        logger.info(
            "Gerando arquivos ZPL..."
        )

        for index, label in enumerate(
            labels,
            start=1
        ):

            zpl_output = Path(
                "storage/exports/"
                f"label_{index:03}.zpl"
            )

            ZPLGenerator.generate_zpl(
                label_data=label,
                output_path=zpl_output
            )

        generated_files = []

        for index, label in enumerate(
            labels,
            start=1
        ):

            file_name = (
                f"label_{index:03d}.png"
            )

            output_file = (
                export_folder / file_name
            )

            logger.info(
                f"Gerando etiqueta: "
                f"{file_name}"
            )

            LabelRenderer.render_label(
                label_data=label,
                output_path=str(output_file)
            )

            generated_files.append(
                output_file
            )

        logger.info(
            "Todas etiquetas foram geradas"
        )

        # ==================================================
        # GERA PREVIEW
        # ==================================================

        logger.info(
            "Gerando preview principal..."
        )

        preview_output = (
            export_folder /
            "preview_label.png"
        )

        LabelRenderer.render_label(
            label_data=labels[0],
            output_path=str(preview_output)
        )

        logger.info(
            f"Preview gerado em: "
            f"{preview_output}"
        )

        # ==================================================
        # GERA PDF FINAL
        # ==================================================

        pdf_output = Path(
            "storage/exports/etiquetas.pdf"
        )

        PDFGenerator.generate_pdf(
            images_folder="storage/exports",
            output_pdf=pdf_output
        )

        # ==================================================
        # RESUMO FINAL
        # ==================================================

        print("\n" + "=" * 60)
        print("ARQUIVOS GERADOS")
        print("=" * 60)

        for generated_file in generated_files[:10]:

            print(
                generated_file.name
            )

        if len(generated_files) > 10:

            print("...")

        print("\n" + "=" * 60)

        print(
            f"TOTAL DE ETIQUETAS: "
            f"{len(labels)}"
        )

        print(
            f"TOTAL DE IMAGENS: "
            f"{len(generated_files)}"
        )

        print("=" * 60)

        logger.info(
            "Processamento concluído com sucesso!"
        )

    except Exception as error:

        logger.exception(
            f"Erro durante execução: "
            f"{error}"
        )

        print("\nERRO AO EXECUTAR O SISTEMA")
        print(error)


if __name__ == "__main__":

    main()