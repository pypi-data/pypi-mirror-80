from pathlib import Path
import os

SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent
TESTS_DIR = ROOT_DIR / 'tests'
WORKFLOWS_DIR = ROOT_DIR / 'workflows'
INTERFACE_DIR = SRC_DIR / 'interfaces'
SUBWORKFLOWS_DIR = SRC_DIR / 'subworkflows'
IMAGES_DIR = SRC_DIR / 'images'
CACHE_DIR = ROOT_DIR / 'cache'
INV_DIR = SRC_DIR / 'inventory'
TEMPLATES_DIR = SRC_DIR / 'templates'
YADAGE_T_DIR = TEMPLATES_DIR / 'yadage_dir'

if not INV_DIR.exists(): os.mkdir(INV_DIR)
