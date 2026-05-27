class LabelLayout:
    """
    Configuração central da etiqueta
    Zebra 100x60mm - 300 DPI
    """

    # ==========================================
    # DPI
    # ==========================================
    DPI = 300

    # ==========================================
    # TAMANHO REAL
    # ==========================================
    WIDTH = int((100 / 25.4) * DPI)
    HEIGHT = int((60 / 25.4) * DPI)

    # ==========================================
    # CORES
    # ==========================================
    BACKGROUND = "#FFFFFF"
    BORDER_COLOR = "black"
    DIVIDER_COLOR = "#555555"

    # ==========================================
    # MARGENS
    # ==========================================
    PADDING_X = 26
    PADDING_Y = 18

    # ==========================================
    # HEADER
    # ==========================================
    HEADER_HEIGHT = 105

    # ==========================================
    # LOGO
    # ==========================================
    LOGO_WIDTH = 520

    # ==========================================
    # ÁREA BARCODE
    # ==========================================
    BARCODE_AREA_WIDTH = 320

    # ==========================================
    # ÁREA CONTEÚDO
    # ==========================================
    CONTENT_X = PADDING_X
    CONTENT_Y = HEADER_HEIGHT + 20

    CONTENT_WIDTH = WIDTH - BARCODE_AREA_WIDTH - (PADDING_X * 4)

    # ==========================================
    # ESPAÇAMENTOS
    # ==========================================
    SECTION_GAP = 18
    LINE_GAP = 12

    # ==========================================
    # FONTES
    # ==========================================
    TITLE_SIZE = 38

    MATERIAL_SIZE = 60

    LABEL_SIZE = 26

    TEXT_SIZE = 34

    SMALL_TEXT_SIZE = 32

    BIG_TEXT_SIZE = 56

    BARCODE_TEXT_SIZE = 38

    # ==========================================
    # BARCODE
    # ==========================================
    BARCODE_WIDTH = 520
    BARCODE_HEIGHT = 190

    # barras mais largas
    BARCODE_MODULE_WIDTH = 0.55

    # altura real do barcode
    BARCODE_MODULE_HEIGHT = 140

    # espaço lateral obrigatório
    BARCODE_QUIET_ZONE = 10.0

    # número do código
    BARCODE_TEXT_HEIGHT = 52
    BARCODE_TEXT_SIZE = 38

    # vertical
    BARCODE_ROTATION = 90