from music21 import stream, note, instrument, duration

def quantize_duration(q_len):
    allowed = [4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 0.25, 0.125]
    return min(allowed, key=lambda x: abs(x - q_len))


def render_pdf(parts):
    score = stream.Score()

    for inst_name, notes in parts.items():
        part = stream.Part()
        part.insert(0, instrument.fromString(inst_name))

        for n in notes:
            nt = note.Note(n["pitch"])
            nt.duration = duration.Duration(quantize_duration(n["duration"]))
            part.insert(n["offset"], nt)

        # Quantize notes + rests safely
        part = part.quantize(quarterLengthDivisors=(1, 2, 4, 8))

        score.append(part)

    score.write("musicxml", "orchestral_score.musicxml")
