from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExcelFile:
    path: Path
    sheet_name: str