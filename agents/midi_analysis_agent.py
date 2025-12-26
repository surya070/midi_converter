import pretty_midi

class MIDIAnalysisAgent:
    def run(self, midi_path):
        midi = pretty_midi.PrettyMIDI(midi_path)
        notes = []

        tempo = midi.estimate_tempo()
        seconds_per_quarter = 60.0 / tempo

        for inst in midi.instruments:
            for n in inst.notes:
                notes.append({
                    "pitch": n.pitch,
                    "offset": n.start / seconds_per_quarter,
                    "duration": (n.end - n.start) / seconds_per_quarter
                })

        notes.sort(key=lambda x: (x["offset"], -x["pitch"]))
        return notes, tempo
