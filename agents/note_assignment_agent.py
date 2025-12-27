from google import genai
import os
import json
import re

class NoteAssignmentAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        x=self.client.models.list()
        for m in x:
            print(m.name)
        self.model = "gemini-3-flash-preview"

    def _extract_json(self, text):
        """
        Extract first JSON object found in text
        """
        match = re.search(r'\{[\s\S]*\}', text)
        if not match:
            return None
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    def run(self, roles, features):
        prompt = f"""
You are an orchestration expert.

You are given symbolic musical features extracted from a MIDI file.
Your task is to choose orchestral instruments that best preserve the original sound.

For each role, you are given:
- Average pitch
- Note density
- Average duration
- Polyphony level

Use these features to select instruments. You can select multiple instruments per role if needed to mimick the original sound exactly.

Allowed instrument names:
Violin, Viola, Cello, Double Bass, Harp, Guitar, Electric Guitar, Bass Guitar,
Flute, Piccolo, Alto Flute, Oboe, English Horn, Clarinet, Bass Clarinet,
Bassoon, Contrabassoon, Recorder,
French Horn, Trumpet, Cornet, Trombone, Bass Trombone, Tuba,
Piano, Electric Piano, Harpsichord, Celesta, Organ, Accordion,
Timpani, Xylophone, Marimba, Vibraphone, Glockenspiel, Tubular Bells,
Drum Set, Snare Drum, Bass Drum, Cymbals, Triangle, Tambourine,
Soprano, Alto, Tenor, Bass, Choir Aahs, Voice Oohs

Rules:
- Do NOT change notes or timing
- Only assign instruments to existing roles
- Avoid redundancy
- Prefer fewer instruments if possible
- Return STRICT JSON ONLY
- NO explanations
- NO markdown

Output format:
{{
  "Melody": ["InstrumentName"],
  "Harmony": ["InstrumentName"],
  "Bass": ["InstrumentName"]
}}

FEATURES:

Melody:
Average pitch: {features["Melody"]["avg_pitch"]:.2f}
Note density: {features["Melody"]["note_density"]:.2f}
Average duration (quarter lengths): {features["Melody"]["avg_duration_ql"]:.2f}

Harmony:
Average pitch: {features["Harmony"]["avg_pitch"]:.2f}
Note density: {features["Harmony"]["note_density"]:.2f}
Average duration (quarter lengths): {features["Harmony"]["avg_duration_ql"]:.2f}

Bass:
Average pitch: {features["Bass"]["avg_pitch"]:.2f}
Note density: {features["Bass"]["note_density"]:.2f}
Average duration (quarter lengths): {features["Bass"]["avg_duration_ql"]:.2f}

"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        raw_text = response.text or ""
        print("\n--- Gemini raw response ---")
        print(raw_text)
        print("----------------------------\n")

        MAX_PER_ROLE = {
            "Melody": 2,
            "Harmony": 2,
            "Bass": 2
        }

        def trim_plan(plan):
            trimmed = {}
            for role, instruments in plan.items():
                trimmed[role] = instruments[:MAX_PER_ROLE.get(role, 1)]
            return trimmed

        plan = self._extract_json(raw_text)
        plan = trim_plan(plan)

        # 🔁 FALLBACK (CRITICAL FOR STABILITY)
        if plan is None:
            print("⚠️ Gemini returned invalid JSON. Using fallback instrumentation.")
            plan = {
                "Melody": ["Violin"],
                "Harmony": ["Viola"],
                "Bass": ["Cello"]
            }

        INSTRUMENT_MAP = {
            "Piano": "Piano",
            "Strings Section": "Violin",
            "String Section": "Violin",
            "Contrabass": "Double Bass",
            "Double Bass": "Double Bass",
            "Bass": "Double Bass",
            "Violin": "Violin",
            "Viola": "Viola",
            "Cello": "Cello",
            "Flute": "Flute",
            "Clarinet": "Clarinet",
            "Oboe": "Oboe",
            "Bassoon": "Bassoon",
            "Horn": "French Horn",
            "French Horn": "French Horn",
            "Trumpet": "Trumpet",
            "Trombone": "Trombone"
        }


        assignments = {}

        def normalize(inst):
            return inst  # prompt already constrained to valid names

        for role, instruments in plan.items():
            for inst in instruments:
                assignments.setdefault(normalize(inst), []).extend(roles[role])



        return assignments
