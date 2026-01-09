# 🎼 MIDI-to-Orchestral Score Generator

A **notation-first orchestration system** that converts a single **MIDI file** into a fully synchronized **orchestral MusicXML score**.

The system **does not generate new music**. Instead, it preserves the original pitch, rhythm, and tempo, and redistributes notes across orchestral instruments using **deterministic rules + constrained GenAI reasoning**.

---
<img width="2559" height="1599" alt="image" src="https://github.com/user-attachments/assets/458efc8e-b09c-4c18-9116-16801071d00d" />

---

## What It Does

✔ MIDI → Orchestral **MusicXML**
✔ Preserves musical structure and timing
✔ Produces readable, notation-valid scores
✔ Explainable and reproducible outputs

✘ No note generation
✘ No audio synthesis
✘ No black-box modeling

---

## How It Works (High Level)

```
MIDI → Analysis → Role Classification → Feature Extraction
     → GenAI Orchestration (Gemini) → Note Assignment
     → Timing Normalization → MusicXML
```

* **Rule-based agents** extract symbolic notes and musical roles (melody, harmony, bass)
* **Gemini** is used only to select appropriate orchestral instruments
* Original notes are copied **verbatim** and kept perfectly synchronized
* Timing is normalized for clean MusicXML export

---

## Key Design Highlights

* **Notation-first** (symbolic correctness over audio realism)
* **Explainable AI** (GenAI selects instruments, never notes)
* **Deterministic pipeline** (same input → same output)
* **Multi-agent architecture** with clear separation of concerns

---

## Output

* Conductor-style **orchestral MusicXML score**
* Multiple synchronized instrument parts
* Compatible with **MuseScore** and standard notation tools

---
<img width="2490" height="1277" alt="image" src="https://github.com/user-attachments/assets/72688d76-cb4c-442e-b992-081208c0a3c6" />

---

## Limitations (By Design)

* No dynamics or articulations
* Performance-level microtiming is normalized
* Not intended for audio rendering

---

## Why This Is Interesting

This project shows how **Generative AI can be used as a controlled reasoning component**, not a black box — combining classical rule-based systems with modern GenAI in a **clean, interpretable orchestration pipeline**.

---
