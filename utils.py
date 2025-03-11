# utils.py
import os
from django.conf import settings
from django.core.files.storage import default_storage

import logging

from principal.models import Image

logger = logging.getLogger(__name__)


def clean_orphaned_images():
    # 1. Lista todas as imagens no diretório do disco
    media_path = os.path.join(settings.MEDIA_ROOT, 'product/images')
    disk_files = set()

    for root, dirs, files in os.walk(media_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, settings.MEDIA_ROOT)
            disk_files.add(relative_path.replace('\\', '/'))  # Normaliza para formato URL

    # 2. Lista todas as imagens registradas no banco
    db_files = set(Image.objects.values_list('photo', flat=True))

    # 3. Encontra arquivos no disco que não estão no banco
    orphans = disk_files - db_files

    # 4. Remove os arquivos órfãos do disco
    deleted_count = 0
    for file_path in orphans:
        try:
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.isfile(full_path):
                os.remove(full_path)
                deleted_count += 1
                logger.info(f"Arquivo órfão removido: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao remover {file_path}: {str(e)}")

    return deleted_count
