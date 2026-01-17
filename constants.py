"""
Constants for IntentBridge Application
Contains application-wide constant values used across modules
"""

# Application metadata
APP_NAME = 'IntentBridge'
APP_VERSION = '1.1.0'
MODULE_1_NAME = 'Intent Classification Engine'
MODULE_2_NAME = 'Ambiguity Resolution Engine'

# Intent type constants
INTENT_LEARNING = 'Learning'
INTENT_BUILDING = 'Building'
INTENT_PLANNING = 'Planning'
INTENT_UNKNOWN = 'Unknown'

# Confidence level constants
CONFIDENCE_HIGH = 'High'
CONFIDENCE_MEDIUM = 'Medium'
CONFIDENCE_LOW = 'Low'

# Emotional signal constants
EMOTION_CONFUSED = 'Confused'
EMOTION_MOTIVATED = 'Motivated'
EMOTION_STRESSED = 'Stressed'
EMOTION_CURIOUS = 'Curious'
EMOTION_NEUTRAL = 'Neutral'

# Classification thresholds
MIN_WORD_COUNT_HIGH_CONFIDENCE = 15
MIN_WORD_COUNT_LOW_CONFIDENCE = 8
MAX_AMBIGUITY_HIGH_CONFIDENCE = 1
MIN_AMBIGUITY_LOW_CONFIDENCE = 3
MIN_SENTENCE_LENGTH = 4  # Minimum words for a substantial sentence

# Resolution type constants
RES_CLARIFICATION = 'ClarificationRequired'
RES_ASSUMPTIONS = 'AssumptionsMade'

# API endpoints
API_CLASSIFY_ENDPOINT = '/api/classify'
API_RESOLVE_ENDPOINT = '/api/resolve'
API_HEALTH_ENDPOINT = '/health'

# Server configuration
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 5000
DEBUG_MODE = True
