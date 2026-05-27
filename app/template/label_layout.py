class LabelLayout:
    """
    Configuração central da etiqueta (100x60mm - Zebra 300 DPI)
    Layout convertido corretamente de mm → pixels
    """

    # ==========================================
    # DPI BASE
    # ==========================================
    DPI = 300

    # ==========================================
    # DIMENSÕES REAIS (100mm x 60mm)
    # ==========================================
    WIDTH = int((100 / 25.4) * DPI)   # ≈ 1181 px
    HEIGHT = int((60 / 25.4) * DPI)   # ≈ 708 px

    # ==========================================
    # MARGENS
    # ==========================================
    PADDING_X = 24
    PADDING_Y = 18

    # ==========================================
    # HEADER
    # ==========================================
    HEADER_HEIGHT = 90

    # ==========================================
    # FONTES (AJUSTADAS PARA 300 DPI)
    # ==========================================
    TITLE_SIZE = 36
    MATERIAL_SIZE = 48
    LABEL_SIZE = 22
    TEXT_SIZE = 28
    SMALL_TEXT_SIZE = 24
    BIG_TEXT_SIZE = 42
    BARCODE_TEXT_SIZE = 28

    # ==========================================
    # LOGO
    # ==========================================
    LOGO_WIDTH = 380

    # ==========================================
    # BARCODE (CRÍTICO PARA LEITURA EM 300 DPI)
    # ==========================================
    BARCODE_WIDTH = 420
    BARCODE_HEIGHT = 140

    BARCODE_MODULE_WIDTH = 0.40
    BARCODE_MODULE_HEIGHT = 110
    BARCODE_QUIET_ZONE = 6.0

    # ==========================================
    # AJUSTES VISUAIS DO BLOCO
    # ==========================================
    BARCODE_TEXT_HEIGHT = 36
    BARCODE_ROTATION = 90

    # ==========================================
    # CORES
    # ==========================================
    BACKGROUND = "#FFFFFF"  # melhor para impressão (evita “acinzentado”)
    BORDER_COLOR = "black"
    DIVIDER_COLOR = "#888"  # mais contraste para impressão