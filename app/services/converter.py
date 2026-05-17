"""
Silnik konwersji PNG → WebP oparty na Pillow.

Wybór biblioteki: Pillow (PIL Fork)
- Najdojrzalsze, stabilne wsparcie WebP na Windows.
- Pełna kontrola jakości (lossless/lossy, quality 0-100).
- Natywne wsparcie kanału alpha (RGBA → WebP z przezroczystością).
- Brak dodatkowych binarnych zależności – webp obsługiwany przez wbudowany
  backend libwebp dołączany do kół Pillow dla Windows.
- Alternatywy (opencv-python, imageio) dodają ~50 MB overhead bez korzyści.
"""
from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from app.models.conversion_job import ConversionJob, JobStatus

logger = logging.getLogger(__name__)


def convert_png_to_webp(job: ConversionJob) -> ConversionJob:
    """
    Konwertuje pojedynczy plik PNG na WebP.
    Modyfikuje job.status oraz rozmiary w miejscu i zwraca job.
    Nie rzuca wyjątków – błędy trafiają do job.error_message.
    """
    source = job.source_path
    output = job.output_path

    try:
        job.source_size_bytes = source.stat().st_size
    except OSError:
        job.source_size_bytes = 0

    try:
        output.parent.mkdir(parents=True, exist_ok=True)

        img: Image.Image = Image.open(source)

        # Zachowaj przezroczystość (PNG może mieć RGBA, P+transparency, LA)
        if img.mode in ("P", "LA"):
            img = img.convert("RGBA")
        elif img.mode not in ("RGBA", "RGB"):
            img = img.convert("RGB")

        save_kwargs: dict = {}
        if job.mode == "lossless":
            save_kwargs["lossless"] = True
        else:
            save_kwargs["quality"] = max(1, min(100, job.quality))
            save_kwargs["method"] = 6  # najlepsza kompresja (wolniej, ale lepiej)

        img.save(output, format="WEBP", **save_kwargs)
        img.close()

        try:
            job.output_size_bytes = output.stat().st_size
        except OSError:
            job.output_size_bytes = 0

        job.status = JobStatus.DONE
        logger.debug(
            "OK: %s → %s  (%d B → %d B)",
            source.name,
            output.name,
            job.source_size_bytes,
            job.output_size_bytes,
        )

    except UnidentifiedImageError:
        job.status = JobStatus.ERROR
        job.error_message = "Plik nie jest rozpoznawalnym obrazem."
        logger.warning("UnidentifiedImageError: %s", source)

    except PermissionError as exc:
        job.status = JobStatus.ERROR
        job.error_message = f"Brak uprawnień: {exc}"
        logger.error("PermissionError: %s – %s", source, exc)

    except Exception as exc:  # noqa: BLE001
        job.status = JobStatus.ERROR
        job.error_message = str(exc)
        logger.error("Błąd konwersji %s: %s", source, exc)

    return job
