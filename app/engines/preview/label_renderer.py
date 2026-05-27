from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont
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

        image = Image.new("RGB", (WIDTH, HEIGHT), LabelLayout.BACKGROUND)
        draw = ImageDraw.Draw(image)

        # ==========================================
        # FONTES (BOLD + leve aumento, sem quebrar layout)
        # ==========================================
        try:
            font_path = "storage/fonts/arialbd.ttf"

            title_font = ImageFont.truetype(font_path, LabelLayout.TITLE_SIZE)
            material_font = ImageFont.truetype(font_path, LabelLayout.MATERIAL_SIZE)
            label_font = ImageFont.truetype(font_path, LabelLayout.LABEL_SIZE)
            text_font = ImageFont.truetype(font_path, LabelLayout.TEXT_SIZE)
            small_font = ImageFont.truetype(font_path, LabelLayout.SMALL_TEXT_SIZE)
            big_font = ImageFont.truetype(font_path, LabelLayout.BIG_TEXT_SIZE)
            barcode_font = ImageFont.truetype(font_path, LabelLayout.BARCODE_TEXT_SIZE)

        except Exception as error:
            logger.warning(f"Erro fonte bold: {error}")

            title_font = ImageFont.load_default()
            material_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            big_font = ImageFont.load_default()
            barcode_font = ImageFont.load_default()

        # ==========================================
        # BORDA + HEADER (sem aumentar altura!)
        # ==========================================
        draw.rectangle(
            [(2, 2), (WIDTH - 3, HEIGHT - 3)],
            outline="black",
            width=3
        )

        header_height = LabelLayout.HEADER_HEIGHT

        draw.rectangle([(0, 0), (WIDTH, header_height)], fill="#FFF")
        draw.line([(0, header_height), (WIDTH, header_height)], fill="black", width=4)

        draw.text(
            (LabelLayout.PADDING_X, 14),
            "ETIQUETA DE AMOSTRA",
            fill="black",
            font=title_font
        )

        # ==========================================
        # CONTEÚDO (ajuste mínimo só de legibilidade)
        # ==========================================
        x = LabelLayout.PADDING_X
        y = header_height + 14

        draw.text((x, y), str(label_data.material), fill="black", font=material_font)
        y += 44

        draw.text((x, y), "DESCRIÇÃO", fill="black", font=label_font)
        y += 18

        descricao = label_data.denominacao or ""
        for line in textwrap.wrap(descricao, width=34)[:2]:
            draw.text((x, y), line, fill="black", font=text_font)
            y += 24

        y += 8

        # ==========================================
        # LINHA
        # ==========================================
        line_y = y
        draw.line([(x, line_y), (WIDTH - x, line_y)], fill="black", width=1)
        y += 14

        # ==========================================
        # LOTE / POSIÇÃO (inalterado funcionalmente)
        # ==========================================
        draw.rounded_rectangle([(x, y), (320, y + 40)], 8, outline="black", width=2)
        draw.text((x + 14, y + 10), f"LOTE: {label_data.lote}", font=small_font, fill="black")

        posicao = (label_data.posicao_deposito or "")[:18]

        draw.rounded_rectangle([(340, y), (620, y + 40)], 8, outline="black", width=2)
        draw.text((355, y + 10), f"POSIÇÃO: {posicao}", font=small_font, fill="black")

        y += 56

        # ==========================================
        # DADOS (SEM REMOVER NADA)
        # ==========================================
        draw.text((x, y), f"COMPOSIÇÃO: {label_data.composicao}", font=small_font, fill="black")
        y += 36

        draw.text((x, y), f"GRAMATURA: {label_data.gramatura}", font=text_font, fill="black")
        draw.text((340, y), f"LARGURA: {label_data.largura}", font=text_font, fill="black")
        y += 36

        cor = (label_data.descritivo_cor or "")[:40]
        draw.text((x, y), f"COR: {cor}", font=text_font, fill="black")
        y += 34

        nome = (label_data.nome_fantasia or "")[:42]
        draw.text((x, y), f"NOME: {nome}", font=small_font, fill="black")

        # ==========================================
        # QTD (mantido visível sempre)
        # ==========================================
        qtd_text = f"QTD: {label_data.utilizacao_livre} {label_data.umb}"

        bbox = draw.textbbox((0, 0), qtd_text, font=big_font)
        qtd_h = bbox[3] - bbox[1]

        draw.text(
            (x, HEIGHT - qtd_h - 20),
            qtd_text,
            font=big_font,
            fill="black"
        )

        # ==========================================
        # BARCODE (inalterado funcionalmente)
        # ==========================================
        try:
            barcode_path = "storage/temp/barcode"

            barcode = Code128(str(label_data.codigo_barras), writer=ImageWriter())

            barcode.save(barcode_path, options={
                "module_width": LabelLayout.BARCODE_MODULE_WIDTH,
                "module_height": LabelLayout.BARCODE_MODULE_HEIGHT,
                "quiet_zone": LabelLayout.BARCODE_QUIET_ZONE,
                "font_size": 0,
                "text_distance": 0,
                "write_text": False,
                "dpi": LabelLayout.DPI
            })

            barcode_img = Image.open(f"{barcode_path}.png").convert("RGB")

            barcode_img = barcode_img.resize(
                (LabelLayout.BARCODE_WIDTH, LabelLayout.BARCODE_HEIGHT),
                Image.Resampling.LANCZOS
            )

            code_text = str(label_data.codigo_barras)

            text_img = Image.new(
                "RGBA",
                (barcode_img.width, LabelLayout.BARCODE_TEXT_HEIGHT),
                (255, 255, 255, 0)
            )

            td = ImageDraw.Draw(text_img)

            tb = td.textbbox((0, 0), code_text, font=barcode_font)
            tw = tb[2] - tb[0]

            td.text(
                ((barcode_img.width - tw) // 2, 5),
                code_text,
                font=barcode_font,
                fill="black"
            )

            block = Image.new(
                "RGBA",
                (barcode_img.width, text_img.height + barcode_img.height),
                (255, 255, 255, 0)
            )

            block.paste(text_img, (0, 0))
            block.paste(barcode_img, (0, text_img.height))

            block = block.rotate(LabelLayout.BARCODE_ROTATION, expand=True)

            bx = WIDTH - block.width - LabelLayout.PADDING_X
            by = line_y + 6

            image.paste(block, (bx, by), block)

        except Exception as error:
            logger.warning(f"Barcode erro: {error}")

        # ==========================================
        # EXPORT (300 DPI correto)
        # ==========================================
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        image.save(output_path, dpi=(300, 300))

        logger.info(f"Etiqueta salva: {output_path}")