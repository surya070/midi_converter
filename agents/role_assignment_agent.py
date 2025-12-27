class RoleAssignmentAgent:
    def run(self, notes):
        melody = []
        harmony = []
        bass = []

        for n in notes:
            if n["pitch"] >= 72:
                melody.append(n)
            elif n["pitch"] >= 55:
                harmony.append(n)
            else:
                bass.append(n)

        return melody, harmony, bass
