import sys
import platform
import numpy as np


# # # # Do not change # # # #
# Slash symbol
SLASH = '\\' if platform.system() == 'Windows' else '/'
# Colab flag
RUNNING_IN_COLAB = 'google.colab' in sys.modules


# Types
CV2_IMAGE = np.ndarray  # Used for type hinting

# Trace
TRACE_DEBUG = 0
TRACE_INFO = 1
TRACE_WARNING = 2
TRACE_ERROR = 3
TRACE_NONE = 1000

# Prepare image method
STAGE_PREPARE_IMAGE_RESIZE = 0
# Size mismatch results in using STAGE_PREPARE_IMAGE_CUT_MIDDLE
STAGE_PREPARE_IMAGE_BLACK_BARS = 1
# Size mismatch results in using STAGE_PREPARE_IMAGE_BLACK_BARS
STAGE_PREPARE_IMAGE_CUT_MIDDLE = 2          # NotImplemented
STAGE_PREPARE_IMAGE_CUT_TOP_LEFT = 3        # NotImplemented
STAGE_PREPARE_IMAGE_CUT_TOP_RIGHT = 4       # NotImplemented
STAGE_PREPARE_IMAGE_CUT_BOTTOM_LEFT = 5     # NotImplemented
STAGE_PREPARE_IMAGE_CUT_BOTTOM_RIGHT = 6    # NotImplemented

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # Set your preferences # # # #
# Prepare image method
STG_PREPARE_METHOD = STAGE_PREPARE_IMAGE_RESIZE

# Trace
TRACE_LOG_PATH_FILE = r'C:\Studia\AAW\Projekt\log_file.txt' if platform.system() == 'Windows' \
    else '/content/log_file.txt'
# TRACE_ALLOW = TRACE_INFO  # Allow this and higher
TRACE_ALLOW = TRACE_DEBUG   # Allow this and higher
# TRACE_ALLOW = TRACE_NONE  # Disabling traces
