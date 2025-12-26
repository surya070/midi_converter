from mcp.music_rules_server import MusicRulesServer

class ValidationAgent:
    def __init__(self):
        self.rules = MusicRulesServer()

    def run(self, parts):
        validated = {}
        for inst, notes in parts.items():
            validated[inst] = [
                n for n in notes if self.rules.validate_pitch(inst, n["pitch"])
            ]
        return validated
