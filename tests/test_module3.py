import unittest
import sys
import os

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import ExecutionPlanningEngine
import constants

class TestExecutionPlanningEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ExecutionPlanningEngine()

    def test_learning_low_confidence(self):
        """Test learning intent with low confidence generates appropriate steps"""
        intent = {
            "intent_type": constants.INTENT_LEARNING,
            "confidence_level": constants.CONFIDENCE_LOW,
            "constraints": [],
            "resolution_status": constants.RES_ASSUMPTIONS
        }
        plan = self.engine.generate_plan(intent)
        self.assertEqual(plan['execution_strategy'], "Curriculum & skill progression")
        self.assertEqual(len(plan['recommended_next_steps']), 3)
        self.assertIn("Identify Core Concepts", plan['recommended_next_steps'][0]['action'])
        self.assertIn("High uncertainty", plan['risk_flags'][0])

    def test_building_high_confidence_with_constraints(self):
        """Test building intent with high confidence and time constraints"""
        intent = {
            "intent_type": constants.INTENT_BUILDING,
            "confidence_level": constants.CONFIDENCE_HIGH,
            "constraints": ["Time constraint mentioned"],
            "resolution_status": constants.RES_ASSUMPTIONS
        }
        plan = self.engine.generate_plan(intent)
        
        # Strategy check
        self.assertEqual(plan['execution_strategy'], "System design & milestone breakdown")
        
        # Check constraint step insertion
        self.assertEqual(len(plan['recommended_next_steps']), 4)
        self.assertEqual(plan['recommended_next_steps'][0]['action'], "Review Constraints")
        
        # Check resource validation
        self.assertTrue(len(plan['suggested_tools_or_resources']) > 0)

    def test_planning_emotion_handling(self):
        """Test planning intent with stressed emotion"""
        intent = {
            "intent_type": constants.INTENT_PLANNING,
            "confidence_level": constants.CONFIDENCE_MEDIUM,
            "emotional_signal": constants.EMOTION_STRESSED,
            "resolution_status": constants.RES_ASSUMPTIONS
        }
        plan = self.engine.generate_plan(intent)
        
        # Check risk flags for burnout warning
        risk_flags = plan['risk_flags']
        self.assertTrue(any("burnout" in flag for flag in risk_flags))

    def test_clarification_blocks_execution(self):
        """Ensure execution halts if clarification is required"""
        intent = {
            "intent_type": constants.INTENT_PLANNING,
            "resolution_type": constants.RES_CLARIFICATION
        }
        plan = self.engine.generate_plan(intent)
        self.assertIn("error", plan)
        self.assertEqual(plan['error'], "Plan generation halted: Clarification required.")

if __name__ == '__main__':
    unittest.main()
