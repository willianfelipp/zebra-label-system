from pathlib import Path
import textwrap

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from barcode import Code128
from barcode.writer import ImageWriter

from app.core.logger import logger
from app.template.label_layout import LabelLayout


class LabelRenderer:

    @staticmethod
    def render_label(label_data, output_path):

        logger.info(f"Renderizando etiqueta: {label_data.material}")

        WIDTH = LabelLayout.WIDTH
        HEIGHT = LabelLayout.HEIGHT

        image = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            LabelLayout.BACKGROUND
        )

        draw = ImageDraw.Draw(image)

        # ==================================================
        # FONTES
        # ==================================================
        try:

            font_path = "storage/fonts/arialbd.ttf"

            title_font = ImageFont.truetype(
                font_path,
                LabelLayout.TITLE_SIZE
            )

            material_font = ImageFont.truetype(
                font_path,
                LabelLayout.MATERIAL_SIZE
            )

            label_font = ImageFont.truetype(
                font_path,
                LabelLayout.LABEL_SIZE
            )

            text_font = ImageFont.truetype(
                font_path,
                LabelLayout.TEXT_SIZE
            )

            small_font = ImageFont.truetype(
                font_path,
                LabelLayout.SMALL_TEXT_SIZE
            )

            big_font = ImageFont.truetype(
                font_path,
                LabelLayout.BIG_TEXT_SIZE
            )

            barcode_font = ImageFont.truetype(
                font_path,
                LabelLayout.BARCODE_TEXT_SIZE
            )

        except Exception as error:

            logger.warning(f"Erro carregando fonte: {error}")

            title_font = ImageFont.load_default()
            material_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            big_font = ImageFont.load_default()
            barcode_font = ImageFont.load_default()

        # ==================================================
        # BORDA
        # ==================================================
        draw.rectangle(
            [(2, 2), (WIDTH - 3, HEIGHT - 3)],
            outline=LabelLayout.BORDER_COLOR,
            width=3
        )

        # ==================================================
        # HEADER
        # ==================================================
        header_height = LabelLayout.HEADER_HEIGHT

        draw.rectangle(
            [(0, 0), (WIDTH, header_height)],
            fill="white"
        )

        draw.line(
            [(0, header_height), (WIDTH, header_height)],
            fill="black",
            width=4
        )

        # ==================================================
        # TÍTULO
        # ==================================================
        draw.text(
            (LabelLayout.PADDING_X, 24),
            "ETIQUETA DE AMOSTRA",
            fill="black",
            font=title_font
        )

        # ==================================================
        # LOGO
        # ==================================================
        try:

            logo_path = "storage/assets/GMalwee_logotivo_positiva.png"

            logo = Image.open(logo_path).convert("RGBA")

            ratio = logo.height / logo.width

            logo_width = LabelLayout.LOGO_WIDTH
            logo_height = int(logo_width * ratio)

            logo = logo.resize(
                (logo_width, logo_height),
                Image.Resampling.LANCZOS
            )

            logo_x = WIDTH - logo_width - 24
            logo_y = 10

            image.paste(
                logo,
                (logo_x, logo_y),
                logo
            )

        except Exception as error:

            logger.warning(f"Erro ao carregar logo: {error}")

        # ==================================================
        # ÁREA CONTEÚDO
        # ==================================================
        x = LabelLayout.CONTENT_X
        y = LabelLayout.CONTENT_Y

        content_limit = LabelLayout.CONTENT_WIDTH

        # ==================================================
        # MATERIAL
        # ==================================================
        draw.text(
            (x, y),
            str(label_data.material),
            fill="black",
            font=material_font
        )

        y += 74

        # ==================================================
        # DESCRIÇÃO
        # ==================================================
        draw.text(
            (x, y),
            "DESCRIÇÃO",
            fill="black",
            font=label_font
        )

        y += 34

        descricao = label_data.denominacao or ""

        descricao_lines = textwrap.wrap(
            descricao,
            width=28
        )[:2]

        for line in descricao_lines:

            draw.text(
                (x, y),
                line,
                fill="black",
                font=text_font
            )

            y += 42

        y += 12

        # ==================================================
        # DIVISÓRIA
        # ==================================================
        line_y = y

        draw.line(
            [(x, line_y), (content_limit, line_y)],
            fill=LabelLayout.DIVIDER_COLOR,
            width=2
        )

        y += 24

        # ==================================================
        # LOTE
        # ==================================================
        draw.rounded_rectangle(
            [(x, y), (520, y + 60)],
            10,
            outline="black",
            width=2
        )

        draw.text(
            (x + 20, y + 12),
            f"LOTE: {label_data.lote}",
            font=small_font,
            fill="black"
        )

        y += 84

        # ==================================================
        # COMPOSIÇÃO
        # ==================================================
        composicao = str(label_data.composicao or "")

        composicao_lines = textwrap.wrap(
            composicao,
            width=34
        )[:2]

        for idx, line in enumerate(composicao_lines):

            prefix = "COMPOSIÇÃO: " if idx == 0 else ""

            draw.text(
                (x, y),
                f"{prefix}{line}",
                font=small_font,
                fill="black"
            )

            y += 36

        y += 8

        # ==================================================
        # GRAMATURA / LARGURA
        # ==================================================
        draw.text(
            (x, y),
            f"GRAMATURA: {label_data.gramatura}",
            font=text_font,
            fill="black"
        )

        draw.text(
            (450, y),
            f"LARGURA: {label_data.largura}",
            font=text_font,
            fill="black"
        )

        y += 48

        # ==================================================
        # COR
        # ==================================================
        cor = (label_data.descritivo_cor or "")[:32]

        draw.text(
            (x, y),
            f"COR: {cor}",
            font=text_font,
            fill="black"
        )

        y += 46

        # ==================================================
        # NOME
        # ==================================================
        nome = (label_data.nome_fantasia or "")[:34]

        draw.text(
            (x, y),
            f"NOME: {nome}",
            font=small_font,
            fill="black"
        )

        # ==================================================
        # QTD
        # ==================================================
        qtd_text = f"QTD: {label_data.utilizacao_livre} {label_data.umb}"

        bbox = draw.textbbox(
            (0, 0),
            qtd_text,
            font=big_font
        )

        qtd_h = bbox[3] - bbox[1]

        draw.text(
            (x, HEIGHT - qtd_h - 24),
            qtd_text,
            font=big_font,
            fill="black"
        )

        # ==================================================
        # BARCODE
        # ==================================================
        try:

            Path("storage/temp").mkdir(
                parents=True,
                exist_ok=True
            )

            barcode_path = "storage/temp/barcode"

            barcode = Code128(
                str(label_data.codigo_barras),
                writer=ImageWriter()
            )

            barcode.save(
                barcode_path,
                options={
                    "module_width": LabelLayout.BARCODE_MODULE_WIDTH,
                    "module_height": LabelLayout.BARCODE_MODULE_HEIGHT,
                    "quiet_zone": LabelLayout.BARCODE_QUIET_ZONE,
                    "font_size": 0,
                    "text_distance": 0,
                    "write_text": False,
                    "dpi": LabelLayout.DPI
                }
            )

            barcode_img = Image.open(
                f"{barcode_path}.png"
            ).convert("RGBA")

            # ==================================================
            # RESIZE BARCODE
            # ==================================================
            barcode_img = barcode_img.resize(
                (
                    LabelLayout.BARCODE_WIDTH,
                    LabelLayout.BARCODE_HEIGHT
                ),
                Image.Resampling.NEAREST
            )

            code_text = str(label_data.codigo_barras)

            # ==================================================
            # TEXTO DO CÓDIGO
            # ==================================================
            text_img = Image.new(
                "RGBA",
                (
                    barcode_img.width,
                    LabelLayout.BARCODE_TEXT_HEIGHT
                ),
                (255, 255, 255, 0)
            )

            td = ImageDraw.Draw(text_img)

            tb = td.textbbox(
                (0, 0),
                code_text,
                font=barcode_font
            )

            tw = tb[2] - tb[0]
            th = tb[3] - tb[1]

            td.text(
                (
                    (barcode_img.width - tw) // 2,
                    (LabelLayout.BARCODE_TEXT_HEIGHT - th) // 2 - 2
                ),
                code_text,
                font=barcode_font,
                fill="black"
            )

            # ==================================================
            # BLOCO COMPLETO
            # ==================================================
            block = Image.new(
                "RGBA",
                (
                    barcode_img.width,
                    barcode_img.height + text_img.height
                ),
                (255, 255, 255, 0)
            )

            block.paste(text_img, (0, 0))
            block.paste(barcode_img, (0, text_img.height))

            # ==================================================
            # ROTACIONA VERTICAL
            # ==================================================
            block = block.rotate(
                LabelLayout.BARCODE_ROTATION,
                expand=True
            )

            # ==================================================
            # AJUSTE DE SEGURANÇA
            # ==================================================
            max_height = HEIGHT - header_height - 30

            if block.height > max_height:

                scale = max_height / block.height

                new_width = int(block.width * scale)
                new_height = int(block.height * scale)

                block = block.resize(
                    (new_width, new_height),
                    Image.Resampling.NEAREST
                )

            # ==================================================
            # POSICIONAMENTO
            # ==================================================
            bx = WIDTH - block.width - 18
            by = header_height + 10

            logger.info(
                f"Barcode final size: {block.width}x{block.height}"
            )

            logger.info(
                f"Barcode position: X={bx} Y={by}"
            )

            # ==================================================
            # PASTE
            # ==================================================
            image.paste(
                block,
                (bx, by),
                block
            )

        except Exception as error:

            logger.warning(f"Erro barcode: {error}")

        # ==================================================
        # EXPORTAÇÃO
        # ==================================================
        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        image.save(
            output_path,
            dpi=(300, 300)
        )

        logger.info(f"Etiqueta salva: {output_path}")