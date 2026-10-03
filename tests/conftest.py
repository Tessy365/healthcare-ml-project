# Pytest root configuration

import sys
from pathlib import Path

# Add project root directory to Python search path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))