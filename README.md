
# 🎼 MIDI-to-Orchestral Score Generation System

### An Explainable, GenAI-Assisted Symbolic Orchestration Pipeline



## 1. Executive Summary

This project implements a **symbolic, notation-first orchestration system** that automatically converts a single input **MIDI file** into a **synchronized, multi-instrument orchestral score** in **MusicXML** format. The system preserves the **original musical structure, tempo, rhythmic alignment, and pitch content** of the input while redistributing musical material across appropriate orchestral instruments.

The system explicitly avoids music generation or composition. Instead, it combines **deterministic music-theory rules**, **multi-agent system design**, and **constrained Generative AI reasoning** to produce **interpretable, reproducible, and notation-valid outputs** suitable for academic evaluation and real-world notation tools.



## 2. Background and Motivation

Converting MIDI files into readable orchestral notation is a non-trivial task. MIDI encodes **performance-level timing**, whereas musical notation requires **symbolic abstraction**. Existing tools often suffer from one or more of the following limitations:

* Focus on **audio synthesis** rather than notation
* Black-box generative models with no explainability
* Loss of structural timing information
* Manual, expertise-heavy orchestration workflows
* Poor handling of synchronization across multiple instruments

This project was motivated by the absence of systems that can **faithfully translate MIDI into orchestral notation while maintaining interpretability and academic rigor**.


## 3. Problem Definition

**Given:**
A single MIDI file containing monophonic or polyphonic musical material.

**Objective:**
Automatically produce a **valid orchestral MusicXML score** such that:

* The musical content (melody, harmony, rhythm, tempo) is preserved
* Notes are redistributed across orchestral instruments
* All instrument parts remain perfectly synchronized
* The output is playable and readable in standard notation software
* All AI decisions are explainable and constrained



## 4. Design Goals

The system was designed with the following principles:

1. **Notation-First**: Prioritize symbolic correctness over audio realism
2. **Explainability**: All AI decisions must be interpretable
3. **Determinism**: Reproducible outputs given the same input
4. **Separation of Concerns**: Clear division between analysis, AI reasoning, and rendering
5. **Minimal Musical Assumption**: No invention or modification of musical content



## 5. High-Level Architecture


MIDI Input
   ↓
MIDI Analysis Agent
   ↓
Musical Role Classification
   ↓
Feature Extraction (Explainability Layer)
   ↓
GenAI Orchestration Agent (Gemini)
   ↓
Instrument-wise Note Assignment
   ↓
Symbolic Timing Normalization
   ↓
MusicXML Score Generation


The architecture follows a **multi-agent pipeline**, where each stage has a single, clearly defined responsibility.



## 6. MIDI Analysis Agent

### Purpose

The MIDI Analysis Agent parses the raw MIDI file and extracts **symbolic musical events** without altering any musical content.

### Extracted Representation

Each note is converted into a normalized internal representation:

json
{
  "pitch": 73,
  "offset": 8.25,
  "duration": 0.75
}


* `pitch`: MIDI pitch number
* `offset`: Absolute position in **beats (quarter-note units)**
* `duration`: Note length in beats

The system also extracts and preserves the **original tempo**, ensuring global timing consistency.

---

## 7. Musical Role Classification

To enable orchestration without composition, notes are classified into **functional musical roles**:

* **Melody** – highest-register, most prominent material
* **Harmony** – mid-range supporting texture
* **Bass** – lowest sustained foundation

This classification is **rule-based**, deterministic, and independent of instrumentation.



## 8. Feature Extraction and Explainability

For each musical role, the system computes descriptive features:

* Average pitch
* Pitch variance
* Note density
* Mean duration
* Approximate polyphony

These features serve two purposes:

1. Provide structured input to the GenAI agent
2. Enable post-hoc explanation of orchestration decisions

No features are used to generate or modify musical content.



## 9. GenAI-Assisted Orchestration Planning

### Role of Generative AI

A constrained GenAI agent (Gemini) is used **only for high-level orchestration reasoning**.

The AI:

* Receives musical roles and extracted features
* Selects appropriate orchestral instruments
* Outputs **instrument names only**

Example output:

json
{
  "Melody": ["Violin"],
  "Harmony": ["Viola", "Piano"],
  "Bass": ["Cello", "Double Bass"]
}


### Explicit Constraints

The AI:

* Does **not** generate notes
* Does **not** change rhythm or pitch
* Operates within predefined orchestral and pitch-range rules
* Produces structured, machine-readable output

This ensures the system remains explainable and academically defensible.



## 10. Instrument-wise Note Assignment

Once instruments are selected:

* Original notes are **copied verbatim**
* Pitch, offset, and duration are preserved
* Notes are assigned to one or more instruments as required

All parts share a **single timing reference**, guaranteeing synchronization.



## 11. Symbolic Timing Normalization (Critical Component)

### Problem Addressed

* MIDI timing is continuous and expressive
* MusicXML requires discrete rhythmic symbols

### Solution

* All timing is expressed in beats
* Durations are mapped to notation-expressible values
* Notes are inserted using **absolute offsets**, not sequential placement
* Quantization is applied uniformly across all parts

### Guarantees

* Tempo preservation
* Structural alignment across instruments
* MusicXML export validity
* Stable playback in notation software

### Known Trade-off

> Performance-level microtiming (swing, rubato) is normalized to ensure symbolic correctness.

This is an inherent limitation of notation systems and not an implementation flaw.



## 12. Output Specification

### Generated File


/output/orchestral_score.musicxml


### Characteristics

* Single conductor-style score
* Multiple synchronized orchestral parts
* Shared tempo and time signature
* Compatible with professional notation tools such as MuseScore and SoundSlice



## 13. Evaluation Methodology

The system was evaluated using:

* Structural comparison between MIDI and MusicXML
* Tempo consistency verification
* Cross-instrument synchronization tests
* Playback validation in notation environments

The evaluation confirms that when all parts are played together, the **original musical structure is preserved**, with deviations arising only from symbolic notation constraints.


## 14. Known Limitations (Explicitly Acknowledged)

* Output will not replicate expressive MIDI performance
* Articulations and dynamics are not inferred
* Dense MIDI may be rhythmically simplified
* The system is not intended for audio synthesis

These are **design decisions**, not deficiencies.



## 15. Value Beyond Simple API Usage

This project goes beyond basic API integration by:

* Implementing a true multi-agent pipeline
* Combining deterministic logic with constrained GenAI reasoning
* Applying programmable prompt engineering
* Performing advanced symbolic post-processing
* Ensuring reproducibility and explainability



## 16. Future Work

* Performer-specific part extraction
* Dynamics and articulation inference
* Support for tempo changes
* Bidirectional MIDI ↔ MusicXML validation



## 17. Final Summary

This system demonstrates how GenAI can be responsibly integrated into symbolic music workflows to automate orchestration while preserving musical intent, correctness, and explainability.

