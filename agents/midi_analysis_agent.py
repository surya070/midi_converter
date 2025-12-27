import pretty_midi

class MIDIAnalysisAgent:
    def run(self, midi_path):
        midi = pretty_midi.PrettyMIDI(midi_path)
        notes = []

        for inst in midi.instruments:
            for n in inst.notes:
                notes.append({
                    "pitch": n.pitch,
                    "start": float(n.start),               # ✅ REQUIRED
                    "duration": float(n.end - n.start)     # ✅ REQUIRED
                })

        notes.sort(key=lambda x: (x["start"], -x["pitch"]))
        tempo = midi.estimate_tempo()
        return notes, tempo
