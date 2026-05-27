import os
import platform
import subprocess

from pathlib import Path

from app.core.logger import logger


class ZebraPrinter:

    @staticmethod
    def print_zpl_file(
        file_path,
        printer_name
    ):

        logger.info(
            f"Enviando arquivo para impressora: "
            f"{file_path}"
        )

        file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(
                f"Arquivo não encontrado: "
                f"{file_path}"
            )

        system = platform.system()

        # ==========================================
        # WINDOWS
        # ==========================================

        if system == "Windows":

            command = (
                f'copy /b "{file_path}" '
                f'"\\\\localhost\\{printer_name}"'
            )

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                raise Exception(
                    result.stderr
                )

        # ==========================================
        # LINUX
        # ==========================================

        elif system == "Linux":

            command = [
                "lp",
                "-d",
                printer_name,
                str(file_path)
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                raise Exception(
                    result.stderr
                )

        else:

            raise Exception(
                f"Sistema operacional "
                f"não suportado: {system}"
            )

        logger.info(
            "Impressão enviada com sucesso"
        )