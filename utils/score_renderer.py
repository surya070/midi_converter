from music21 import stream, note, instrument, duration

def quantize_duration(q_len):
    # Allowed musical durations (quarter lengths)
    allowed = [
        4.0, 3.0, 2.0, 1.5, 1.0,
        0.75, 0.5, 0.25, 0.125
    ]
    return min(allowed, key=lambda x: abs(x - q_len))


def render_pdf(parts):
    score = stream.Score()

    for inst_name, notes in parts.items():
        part = stream.Part()
        part.insert(0, instrument.fromString(inst_name))

        for n in notes:
            ql = quantize_duration(n["duration"])
            d = duration.Duration(ql)
            nt = note.Note(n["pitch"])
            nt.duration = d
            part.append(nt)

        score.append(part)

    score.write("musicxml", "orchestral_score.musicxml")
