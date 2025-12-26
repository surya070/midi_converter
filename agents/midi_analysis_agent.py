import pretty_midi

class MIDIAnalysisAgent:
    def run(self, midi_path):
        midi = pretty_midi.PrettyMIDI(midi_path)
        notes = []

        for inst in midi.instruments:
            for n in inst.notes:
                notes.append({
                    "pitch": n.pitch,
                    "start": n.start,
                    "duration": n.end - n.start
                })

        notes.sort(key=lambda x: (x["start"], -x["pitch"]))
        return notes, midi.estimate_tempo()
