class MusicRulesServer:
    INSTRUMENT_RANGES = {
        "Violin": (60, 96),
        "Viola": (55, 80),
        "Cello": (36, 60),
        "Bass": (28, 45),
        "Flute": (60, 96),
        "French Horn": (40, 75),
        "Percussion": (35, 35)
    }

    def validate_pitch(self, instrument, pitch):
        low, high = self.INSTRUMENT_RANGES[instrument]
        return low <= pitch <= high
