from dotenv import load_dotenv
load_dotenv()

from agents.midi_analysis_agent import MIDIAnalysisAgent
from agents.role_assignment_agent import RoleAssignmentAgent
from agents.orchestration_planner_agent import OrchestrationPlannerAgent
from agents.note_assignment_agent import NoteAssignmentAgent
from agents.validation_agent import ValidationAgent
from agents.explanation_agent import ExplanationAgent
from utils.score_renderer import render_pdf

analysis = MIDIAnalysisAgent()
roles = RoleAssignmentAgent()
planner = OrchestrationPlannerAgent()
assigner = NoteAssignmentAgent()
validator = ValidationAgent()
explainer = ExplanationAgent()

notes, tempo = analysis.run("input.mid")
melody, harmony, bass = roles.run(notes)

plan = planner.run()  # logged / explainable
parts = assigner.run(melody, harmony, bass)
validated = validator.run(parts)

render_pdf(validated)

print("\n--- Orchestration Explanation ---\n")
print(explainer.run())
