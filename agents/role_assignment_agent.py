class RoleAssignmentAgent:
    def run(self, notes):
        melody = [n for n in notes if n["pitch"] >= 72]
        bass = [n for n in notes if n["pitch"] <= 45]
        harmony = [n for n in notes if n not in melody and n not in bass]
        return melody, harmony, bass
