from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import logging
import constants

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class IntentClassificationEngine:
    """
    Intent Classification Engine - Module 1 of IntentBridge
    Converts raw human intent into structured machine-usable representations
    """
    
    def __init__(self):
        self.learning_keywords = ['learn', 'study', 'understand', 'know', 'master', 'acquire', 'practice']
        self.building_keywords = ['build', 'create', 'make', 'develop', 'implement', 'design', 'code', 'program']
        self.planning_keywords = ['plan', 'organize', 'prepare', 'decide', 'schedule', 'roadmap', 'strategy']
        
        self.confused_signals = ['confused', 'lost', 'stuck', 'don\'t know', 'not sure', 'unclear', 'help']
        self.motivated_signals = ['excited', 'ready', 'want to', 'determined', 'committed', 'passionate']
        self.stressed_signals = ['overwhelmed', 'anxious', 'worried', 'pressured', 'urgent', 'rushed']
        self.curious_signals = ['curious', 'interested', 'wondering', 'explore', 'discover']
    
    def classify(self, user_input):
        """
        Execute the 8-step intent classification flow
        
        Args:
            user_input (str): Raw unstructured human intent text
            
        Returns:
            dict: Structured intent representation containing:
                - intent_type: Learning, Building, Planning, or Unknown
                - primary_goal: Main objective extracted from input
                - secondary_goals: Supporting objectives (list)
                - constraints: Explicit limitations mentioned (list)
                - ambiguities: Missing or vague information (list)
                - emotional_signal: Detected emotion (Confused, Motivated, etc.)
                - confidence_level: Low, Medium, or High
        """
        if not user_input or not user_input.strip():
            logger.debug("Empty input received, returning empty response")
            return self._empty_response()
        
        logger.info(f"Starting classification for input of length {len(user_input)}")
        input_lower = user_input.lower()
        
        # STEP 2: Determine intent type (Learning, Building, Planning)
        intent_type = self._classify_intent_type(input_lower)
        logger.debug(f"Intent type classified as: {intent_type}")
        
        # STEP 3: Extract primary goal from the first substantial sentence
        primary_goal = self._extract_primary_goal(user_input)
        
        # STEP 4: Identify secondary goals from remaining context
        secondary_goals = self._extract_secondary_goals(user_input)
        
        # STEP 5: Extract explicit constraints (Time, Skill, Budget)
        constraints = self._extract_constraints(user_input, input_lower)
        
        # STEP 6: Detect ambiguities requiring refinement
        ambiguities = self._detect_ambiguities(user_input, input_lower)
        
        # STEP 7: Detect emotional signal based on keyword sentiment
        emotional_signal = self._detect_emotion(input_lower)
        
        # STEP 8: Assign confidence level (Low, Medium, or High)
        confidence_level = self._calculate_confidence(user_input, primary_goal, ambiguities)
        
        logger.info(f"Classification complete: {intent_type} | {confidence_level} confidence | {emotional_signal}")
        
        return {
            "intent_type": intent_type,
            "primary_goal": primary_goal,
            "secondary_goals": secondary_goals,
            "constraints": constraints,
            "ambiguities": ambiguities,
            "emotional_signal": emotional_signal,
            "confidence_level": confidence_level
        }
    
    def _classify_intent_type(self, input_lower):
        """
        Classify into Learning, Building, Planning, or Unknown
        
        Uses keyword matching to determine the primary intent category.
        Returns Unknown if no keywords match.
        
        Args:
            input_lower (str): Lowercased user input
            
        Returns:
            str: Intent type classification
        """
        learning_score = sum(1 for kw in self.learning_keywords if kw in input_lower)
        building_score = sum(1 for kw in self.building_keywords if kw in input_lower)
        planning_score = sum(1 for kw in self.planning_keywords if kw in input_lower)
        
        if learning_score == 0 and building_score == 0 and planning_score == 0:
            return constants.INTENT_UNKNOWN
        
        max_score = max(learning_score, building_score, planning_score)
        
        if learning_score == max_score:
            return constants.INTENT_LEARNING
        elif building_score == max_score:
            return constants.INTENT_BUILDING
        else:
            return constants.INTENT_PLANNING
    
    def _extract_primary_goal(self, user_input):
        """
        Extract the ultimate objective as one clear sentence
        
        Identifies the main goal from the input by selecting the first
        substantial sentence (minimum 4 words).
        
        Args:
            user_input (str): Original user input (preserves case)
            
        Returns:
            str: Primary goal statement
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', user_input)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return "No clear goal identified"
        
        # Take the first substantial sentence as primary goal
        for sentence in sentences:
            if len(sentence.split()) > (constants.MIN_SENTENCE_LENGTH - 1):
                return sentence
        
        return sentences[0] if sentences else "No clear goal identified"
    
    def _extract_secondary_goals(self, user_input):
        """Extract supporting objectives"""
        secondary = []
        input_lower = user_input.lower()
        
        # Look for explicit secondary indicators
        if 'also' in input_lower or 'additionally' in input_lower or 'and' in input_lower:
            sentences = re.split(r'[.!?]+', user_input)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) > 1:
                for i, sentence in enumerate(sentences[1:], 1):
                    if len(sentence.split()) > (constants.MIN_SENTENCE_LENGTH - 1):
                        secondary.append(sentence)
        
        return secondary
    
    def _extract_constraints(self, user_input, input_lower):
        """Extract only explicitly mentioned constraints"""
        constraints = []
        
        # Skill limitations
        if any(term in input_lower for term in ['beginner', 'new to', 'never', 'no experience', 'don\'t know']):
            constraints.append("Limited or no prior experience mentioned")
        
        # Time limits
        time_patterns = ['in \d+', 'by \d+', 'within', 'quickly', 'fast', 'urgent', 'deadline', 'asap']
        if any(re.search(pattern, input_lower) for pattern in time_patterns):
            constraints.append("Time constraint mentioned")
        
        # Resource limits
        if any(term in input_lower for term in ['no budget', 'free', 'limited resources', 'can\'t afford']):
            constraints.append("Resource limitation mentioned")
        
        # Explicit fears/blockers
        if any(term in input_lower for term in ['afraid', 'scared', 'worried', 'concerned', 'fear']):
            constraints.append("Fear or concern expressed")
        
        return constraints
    
    def _detect_ambiguities(self, user_input, input_lower):
        """Identify missing or vague information"""
        ambiguities = []
        
        # Check for vague time references
        if any(term in input_lower for term in ['soon', 'quickly', 'fast', 'eventually']):
            ambiguities.append("Time availability undefined or vague")
        
        # Check for subjective quality terms
        if any(term in input_lower for term in ['good', 'great', 'simple', 'easy', 'complex', 'advanced', 'professional']):
            ambiguities.append("Subjective quality terms used without specific criteria")
        
        # Check for undefined scope
        if len(user_input.split()) < 10:
            ambiguities.append("Input too brief - scope unclear")
        
        # Check for vague goals
        if any(term in input_lower for term in ['something', 'anything', 'stuff', 'things', 'whatever']):
            ambiguities.append("Goal contains vague or undefined elements")
        
        return ambiguities
    
    def _detect_emotion(self, input_lower):
        """Detect emotional signal from tone and wording"""
        confused_score = sum(1 for signal in self.confused_signals if signal in input_lower)
        motivated_score = sum(1 for signal in self.motivated_signals if signal in input_lower)
        stressed_score = sum(1 for signal in self.stressed_signals if signal in input_lower)
        curious_score = sum(1 for signal in self.curious_signals if signal in input_lower)
        
        scores = {
            constants.EMOTION_CONFUSED: confused_score,
            constants.EMOTION_MOTIVATED: motivated_score,
            constants.EMOTION_STRESSED: stressed_score,
            constants.EMOTION_CURIOUS: curious_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            return constants.EMOTION_NEUTRAL
        
        # Return the emotion with highest score
        for emotion, score in scores.items():
            if score == max_score:
                return emotion
        
        return constants.EMOTION_NEUTRAL
    
    def _calculate_confidence(self, user_input, primary_goal, ambiguities):
        """Calculate confidence level: Low, Medium, or High"""
        word_count = len(user_input.split())
        ambiguity_count = len(ambiguities)
        
        # High confidence criteria
        if word_count >= constants.MIN_WORD_COUNT_HIGH_CONFIDENCE and ambiguity_count <= constants.MAX_AMBIGUITY_HIGH_CONFIDENCE and primary_goal != "No clear goal identified":
            return constants.CONFIDENCE_HIGH
        
        # Low confidence criteria
        if word_count < constants.MIN_WORD_COUNT_LOW_CONFIDENCE or ambiguity_count >= constants.MIN_AMBIGUITY_LOW_CONFIDENCE or primary_goal == "No clear goal identified":
            return constants.CONFIDENCE_LOW
        
        # Medium by default
        return constants.CONFIDENCE_MEDIUM
    
    def _empty_response(self):
        """Return empty structured response"""
        return {
            "intent_type": constants.INTENT_UNKNOWN,
            "primary_goal": "No input provided",
            "secondary_goals": [],
            "constraints": [],
            "ambiguities": ["No input provided"],
            "emotional_signal": constants.EMOTION_NEUTRAL,
            "confidence_level": constants.CONFIDENCE_LOW
        }


class AmbiguityResolutionEngine:
    """
    Ambiguity Resolution Engine - Module 2 of IntentBridge
    Resolves ambiguities in intent objects through clarification or neutral assumptions.
    """

    def __init__(self):
        # Define which ambiguities are considered blocking
        self.blocking_ambiguities = [
            "Input too brief - scope unclear",
            "Goal contains vague or undefined elements",
            "Target level unknown",
            "Domain baseline unknown"
        ]
        
        # Mapping of ambiguity types to default operating assumptions
        self.assumption_map = {
            "Time availability undefined or vague": "Standard part-time availability (10-15 hours/week) is assumed.",
            "Subjective quality terms used without specific criteria": "Standard professional benchmarks for quality will be applied.",
            "Input too brief - scope unclear": "A standard introductory scope for the identified domain is assumed.",
            "Goal contains vague or undefined elements": "The most common interpretation of the stated goal will be used.",
            "No input provided": "Fundamental introductory concepts are assumed as a starting point."
        }

    def resolve(self, intent_object):
        """
        Execute the ambiguity resolution logic
        
        Args:
            intent_object (dict): The output from Module 1
            
        Returns:
            dict: Resolution object with type, question, and assumptions
        """
        ambiguities = intent_object.get("ambiguities", [])
        
        if not ambiguities:
            return {
                "resolution_type": constants.RES_ASSUMPTIONS,
                "clarification_question": "",
                "assumptions": ["Proceeding with the primary goal as stated with no further assumptions required."]
            }

        # STEP 2: Determine if any ambiguity is BLOCKING
        blocking_found = [a for a in ambiguities if a in self.blocking_ambiguities or "time" in a.lower()]
        
        if blocking_found:
            # STEP 3: Select the SINGLE most critical ambiguity (first one found)
            critical = blocking_found[0]
            question = self._generate_clarification_question(critical, intent_object)
            
            return {
                "resolution_type": constants.RES_CLARIFICATION,
                "clarification_question": question,
                "assumptions": []
            }
        else:
            # STEP 4: Generate explicit assumptions for each ambiguity
            assumptions = []
            for ambiguity in ambiguities:
                assumption = self.assumption_map.get(ambiguity, f"A neutral, standard interpretation for '{ambiguity}' is assumed.")
                assumptions.append(assumption)
            
            return {
                "resolution_type": constants.RES_ASSUMPTIONS,
                "clarification_question": "",
                "assumptions": assumptions
            }

    def _generate_clarification_question(self, ambiguity, intent_object):
        """Generate a concise clarification question for blocking ambiguities"""
        if "time" in ambiguity.lower():
            return "How many hours per week can you realistically dedicate to this goal?"
        elif "scope" in ambiguity.lower() or "too brief" in ambiguity.lower():
            return "Could you provide more detail regarding the specific scope or deliverables you have in mind?"
        elif "goal" in ambiguity.lower() or "vague" in ambiguity.lower():
            return "Could you specifically define the primary outcome you expect to achieve?"
        elif "level" in ambiguity.lower():
            return "What is your current proficiency level or target level for this objective?"
        else:
            return f"Could you provide more specific information regarding {ambiguity.lower()}?"


# Initialize the engines
classification_engine = IntentClassificationEngine()
resolution_engine = AmbiguityResolutionEngine()


@app.route('/')
def index():
    """Serve the frontend interface"""
    return render_template('index.html')


@app.route(constants.API_CLASSIFY_ENDPOINT, methods=['POST'])
def classify_intent():
    """
    API endpoint for intent classification
    Expects JSON: {"user_input": "raw intent string"}
    Returns: Structured intent JSON
    """
    try:
        data = request.get_json()
        
        if not data or 'user_input' not in data:
            return jsonify({
                "error": "Missing 'user_input' in request body"
            }), 400
        
        user_input = data['user_input']
        result = classification_engine.classify(user_input)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Internal error: {str(e)}"
        }), 500


@app.route(constants.API_RESOLVE_ENDPOINT, methods=['POST'])
def resolve_ambiguity():
    """
    API endpoint for ambiguity resolution
    Expects JSON: { "intent_type": "...", "primary_goal": "...", ... }
    Returns: Resolution JSON
    """
    try:
        intent_object = request.get_json()
        
        if not intent_object:
            return jsonify({
                "error": "Missing intent object in request body"
            }), 400
        
        # Validate minimal schema
        required_fields = ["intent_type", "primary_goal", "ambiguities"]
        for field in required_fields:
            if field not in intent_object:
                return jsonify({
                    "error": f"Missing required field '{field}' in intent object"
                }), 400

        result = resolution_engine.resolve(intent_object)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Internal error: {str(e)}"
        }), 500


@app.route(constants.API_HEALTH_ENDPOINT, methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "modules": [constants.MODULE_1_NAME, constants.MODULE_2_NAME],
        "version": constants.APP_VERSION
    }), 200


if __name__ == '__main__':
    app.run(debug=constants.DEBUG_MODE, host=constants.DEFAULT_HOST, port=constants.DEFAULT_PORT)
