from collections import defaultdict

class FeatureExtractionAgent:
    def run(self, roles, tempo):
        seconds_per_beat = 60.0 / tempo
        features = {}

        for role, role_notes in roles.items():
            if not role_notes:
                features[role] = {}
                continue

            durations_ql = [
                n["duration"] / seconds_per_beat
                for n in role_notes
            ]

            pitches = [n["pitch"] for n in role_notes]

            features[role] = {
                "avg_pitch": sum(pitches) / len(pitches),
                "note_density": len(role_notes) / max(
                    (role_notes[-1]["start"] - role_notes[0]["start"]), 0.001
                ),
                "avg_duration_ql": sum(durations_ql) / len(durations_ql)
            }

        return features

 

    def _estimate_polyphony(self, notes):
        timeline = {}

        for n in notes:
            t = round(n["start_ql"], 2)
            timeline[t] = timeline.get(t, 0) + 1

        return max(timeline.values()) if timeline else 1

