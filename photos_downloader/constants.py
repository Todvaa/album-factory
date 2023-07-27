import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

PREVIEW_DIR = 'preview'
SM_PH_DIR = os.path.join(PREVIEW_DIR, 'small')
LG_PH_DIR = os.path.join(PREVIEW_DIR, 'large')
ORIG_PH_DIR = 'original'

SM_PH_SZ = 'L'
LG_PH_SZ = 'XL'

BUCKET_PHOTO = 'photos-storage'
