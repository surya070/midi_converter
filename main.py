import os
from dotenv import load_dotenv

from agents.midi_analysis_agent import MIDIAnalysisAgent
from agents.role_assignment_agent import RoleAssignmentAgent
from agents.note_assignment_agent import NoteAssignmentAgent
from agents.feature_extraction_agent import FeatureExtractionAgent
from utils.score_renderer import render_score

load_dotenv()

INPUT_MIDI = "input.mid"

midi_agent = MIDIAnalysisAgent()
role_agent = RoleAssignmentAgent()
note_agent = NoteAssignmentAgent()
feature_agent = FeatureExtractionAgent()

notes, tempo = midi_agent.run(INPUT_MIDI)
melody, harmony, bass = role_agent.run(notes)
roles = {
    "Melody": melody,
    "Harmony": harmony,
    "Bass": bass
}
features = feature_agent.run(roles, tempo)

assignments = note_agent.run(roles,features)
for inst, notes in assignments.items():
    print(inst, notes[0])
    break

render_score(assignments, tempo)

print("✅ Orchestral MusicXML generated in ./output/")
