# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import sys
import os

# Third party imports
# Local application imports
# hack to import module for iOS/Pythonista/ExternalFiles/WorkingCopy
module_path = os.path.join(os.path.dirname(sys.path[0]), 'hexafid')
sys.path.append(module_path)
