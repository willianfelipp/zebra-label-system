from pathlib import Path

from PIL import Image

from app.core.logger import logger


class PDFGenerator:

    @staticmethod
    def generate_pdf(
        images_folder,
        output_pdf
    ):

        logger.info(
            "Iniciando geração do PDF..."
        )

        images_folder = Path(images_folder)

        image_files = sorted(
            images_folder.glob("label_*.png")
        )

        if not image_files:

            raise Exception(
                "Nenhuma imagem encontrada "
                "para gerar PDF"
            )

        image_list = []

        for image_file in image_files:

            image = Image.open(image_file)

            if image.mode == "RGBA":

                image = image.convert("RGB")

            image_list.append(image)

        first_image = image_list[0]

        remaining_images = image_list[1:]

        output_pdf = Path(output_pdf)

        output_pdf.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        first_image.save(
            output_pdf,
            save_all=True,
            append_images=remaining_images
        )

        logger.info(
            f"PDF gerado com sucesso: "
            f"{output_pdf}"
        )