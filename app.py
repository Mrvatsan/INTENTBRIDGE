from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re

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
            return self._empty_response()
        
        input_lower = user_input.lower()
        
        # STEP 2: Determine intent type
        intent_type = self._classify_intent_type(input_lower)
        
        # STEP 3: Extract primary goal
        primary_goal = self._extract_primary_goal(user_input)
        
        # STEP 4: Identify secondary goals
        secondary_goals = self._extract_secondary_goals(user_input)
        
        # STEP 5: Extract constraints
        constraints = self._extract_constraints(user_input, input_lower)
        
        # STEP 6: Detect ambiguities
        ambiguities = self._detect_ambiguities(user_input, input_lower)
        
        # STEP 7: Detect emotional signal
        emotional_signal = self._detect_emotion(input_lower)
        
        # STEP 8: Assign confidence level
        confidence_level = self._calculate_confidence(user_input, primary_goal, ambiguities)
        
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
            return "Unknown"
        
        max_score = max(learning_score, building_score, planning_score)
        
        if learning_score == max_score:
            return "Learning"
        elif building_score == max_score:
            return "Building"
        else:
            return "Planning"
    
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
            if len(sentence.split()) > 3:  # At least 4 words
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
                    if len(sentence.split()) > 3:
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
            'Confused': confused_score,
            'Motivated': motivated_score,
            'Stressed': stressed_score,
            'Curious': curious_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            return "Neutral"
        
        # Return the emotion with highest score
        for emotion, score in scores.items():
            if score == max_score:
                return emotion
        
        return "Neutral"
    
    def _calculate_confidence(self, user_input, primary_goal, ambiguities):
        """Calculate confidence level: Low, Medium, or High"""
        word_count = len(user_input.split())
        ambiguity_count = len(ambiguities)
        
        # High confidence criteria
        if word_count >= 15 and ambiguity_count <= 1 and primary_goal != "No clear goal identified":
            return "High"
        
        # Low confidence criteria
        if word_count < 8 or ambiguity_count >= 3 or primary_goal == "No clear goal identified":
            return "Low"
        
        # Medium by default
        return "Medium"
    
    def _empty_response(self):
        """Return empty structured response"""
        return {
            "intent_type": "Unknown",
            "primary_goal": "No input provided",
            "secondary_goals": [],
            "constraints": [],
            "ambiguities": ["No input provided"],
            "emotional_signal": "Neutral",
            "confidence_level": "Low"
        }


# Initialize the engine
engine = IntentClassificationEngine()


@app.route('/')
def index():
    """Serve the frontend interface"""
    return render_template('index.html')


@app.route('/api/classify', methods=['POST'])
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
        result = engine.classify(user_input)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Internal error: {str(e)}"
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "module": "Intent Classification Engine",
        "version": "1.0.0"
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
