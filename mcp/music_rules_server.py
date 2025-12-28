class MusicRulesServer:
    INSTRUMENT_RANGES = {
        # Strings
        "Violin": (55, 96),  # G3-C7 (extended range)
        "Viola": (48, 84),  # C3-C6
        "Cello": (36, 72),  # C2-C5
        "Double Bass": (28, 55),  # E1-G3
        "Bass": (28, 55),  # Alias for Double Bass
        "Harp": (23, 103),  # B0-G7 (very wide range)
        "Guitar": (40, 88),  # E2-E6
        "Electric Guitar": (40, 88),
        "Bass Guitar": (28, 67),  # E1-G4
        
        # Woodwinds
        "Flute": (60, 96),  # C4-C7
        "Piccolo": (74, 108),  # D5-C8
        "Alto Flute": (55, 84),  # G3-C6
        "Oboe": (58, 91),  # Bb3-G6
        "English Horn": (50, 79),  # D3-G5
        "Clarinet": (50, 91),  # D3-G6
        "Bass Clarinet": (35, 72),  # B1-C5
        "Bassoon": (34, 75),  # Bb1-E5
        "Contrabassoon": (22, 58),  # Bb0-Bb3
        "Recorder": (60, 96),  # C4-C7
        
        # Brass
        "French Horn": (40, 79),  # E2-G5
        "Trumpet": (58, 88),  # Bb3-E6
        "Cornet": (58, 88),  # Bb3-E6
        "Trombone": (40, 72),  # E2-C5
        "Bass Trombone": (29, 67),  # B1-G4
        "Tuba": (29, 58),  # B1-Bb3
        
        # Keyboard/Pitched Percussion
        "Piano": (21, 108),  # A0-C8 (full range)
        "Electric Piano": (21, 108),
        "Harpsichord": (21, 108),
        "Celesta": (60, 108),  # C4-C8
        "Organ": (21, 108),  # A0-C8
        "Accordion": (48, 96),  # C3-C7
        
        # Percussion (single note or wide range)
        "Timpani": (36, 60),  # C2-C4
        "Xylophone": (65, 108),  # F4-C8
        "Marimba": (48, 96),  # C3-C7
        "Vibraphone": (53, 89),  # F3-F6
        "Glockenspiel": (79, 108),  # G5-C8
        "Tubular Bells": (60, 84),  # C4-C6
        "Drum Set": (35, 35),  # Unpitched
        "Snare Drum": (38, 38),  # Unpitched
        "Bass Drum": (36, 36),  # Unpitched
        "Cymbals": (49, 49),  # Unpitched
        "Triangle": (81, 81),  # Unpitched
        "Tambourine": (54, 54),  # Unpitched
        "Percussion": (35, 35),
        
        # Voice
        "Soprano": (60, 96),  # C4-C7
        "Alto": (55, 84),  # G3-C6
        "Tenor": (48, 79),  # C3-G5
        "Bass": (40, 67),  # E2-G4 (voice)
        "Choir Aahs": (48, 84),  # C3-C6
        "Voice Oohs": (48, 84),  # C3-C6
    }

    def validate_pitch(self, instrument, pitch):
        """
        Validate if a pitch is within the instrument's playable range.
        Returns True if valid, False if out of range.
        If instrument is not in ranges dict, returns True (backward compatible).
        """
        if instrument not in self.INSTRUMENT_RANGES:
            # Unknown instrument - allow all pitches (backward compatible)
            return True
        
        low, high = self.INSTRUMENT_RANGES[instrument]
        return low <= pitch <= high
    
    def find_suitable_instrument(self, pitch, current_instrument=None, preferred_instruments=None):
        """
        Find a suitable instrument for a given pitch.
        Returns instrument name or None if no suitable instrument found.
        """
        if preferred_instruments is None:
            preferred_instruments = []
        
        # First, try preferred instruments
        for inst in preferred_instruments:
            if inst in self.INSTRUMENT_RANGES and self.validate_pitch(inst, pitch):
                return inst
        
        # Then, search all instruments
        for inst, (low, high) in self.INSTRUMENT_RANGES.items():
            if inst == current_instrument:
                continue  # Skip current instrument
            if low <= pitch <= high:
                return inst
        
        return None
    
    def filter_notes_by_range(self, instrument, notes):
        """
        Filter notes to only include those within the instrument's range.
        Returns tuple: (valid_notes, invalid_notes)
        """
        if instrument not in self.INSTRUMENT_RANGES:
            # Unknown instrument - return all notes (backward compatible)
            return notes, []
        
        valid_notes = []
        invalid_notes = []
        
        for note in notes:
            if self.validate_pitch(instrument, note["pitch"]):
                valid_notes.append(note)
            else:
                invalid_notes.append(note)
        
        return valid_notes, invalid_notes
