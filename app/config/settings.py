from pathlib import Path

# ==========================================
# DIRETÓRIOS PRINCIPAIS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_DIR = BASE_DIR / "storage"

TEMPLATES_DIR = STORAGE_DIR / "templates"
LOGS_DIR = STORAGE_DIR / "logs"
CACHE_DIR = STORAGE_DIR / "cache"
EXPORTS_DIR = STORAGE_DIR / "exports"
BACKUPS_DIR = STORAGE_DIR / "backups"
TEMP_DIR = STORAGE_DIR / "temp"

# ==========================================
# CONFIGURAÇÕES SISTEMA
# ==========================================

APP_NAME = "Zebra Label System"

APP_VERSION = "1.0.0"

DEFAULT_DPI = 300

# Etiqueta padrão
LABEL_WIDTH_MM = 100
LABEL_HEIGHT_MM = 60