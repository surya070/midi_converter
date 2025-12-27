from music21 import stream, note, instrument, tempo, meter

GRID = 0.25  # 16th note (in beats)

def render_score(assignments, tempo_bpm):
    score = stream.Score()
    score.insert(0, tempo.MetronomeMark(number=tempo_bpm))

    seconds_per_beat = 60 / tempo_bpm

    for inst_name, notes in assignments.items():
        part = stream.Part()
        part.insert(0, instrument.fromString(inst_name))
        part.insert(0, meter.TimeSignature('4/4'))

        for n in notes:
            beats = n["start"] / seconds_per_beat
            dur = n["duration"] / seconds_per_beat

            beats = round(beats / GRID) * GRID
            dur = max(round(dur / GRID) * GRID, GRID)

            nt = note.Note(n["pitch"], quarterLength=dur)
            part.insert(beats, nt)

        score.append(part)

    score.write("musicxml", "output/orchestral_score.musicxml")
