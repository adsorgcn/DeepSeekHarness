# iLang IML-VEM v1.2.2

## 感知先行 · 结构先于声音

Video Engineering Manual · iLang IML-VEM v1.2.2

## Scope

End-to-end protocol for producing a scored multi-shot video from a still image or scene description.

Flow: Input → Perception → Temporal Structure (code) → Shot Plan → Per-Shot Execution → Visual Assembly → Audio Render → Final Output.

Each layer validates and locks its output before downstream execution. Audio waveform rendering begins only after the visual track passes assembly verification.

Locking and revision

- Identify each locked specification by version; downstream assets reference their dependencies.
- A controlled revision records changed fields, reason, and affected dependencies. Revalidate affected assets; regenerate or re-conform where necessary.
- Reuse requires the asset to be available and compatible with the active specification. Final output must resolve to one coherent specification.
- Allow at most one controlled upstream revision per run. Regeneration against unchanged requirements is a retry.
- Hard acceptance rules cannot be weakened through retries, revisions, or completion labels.

## Input

Accepted sources

- Still image: source reference and default opening frame.
- Scene description: generate and validate a source image; allow at most two attempts.
- Ambiguous intention: resolve missing creative choices into an explicit scene interpretation and record assumptions.

If no generated source image passes, stop and report the mismatch.

Required parameters

Record target duration, output specification, user constraints, available tools, and resource limits.

Defaults: 30 seconds; 960 × 960; 24 fps; H.264 + AAC; 48 kHz audio; MP4. Record applied defaults. Duration and frame rate must be positive.

Capability inventory

Record supported image conditioning, frame-reference conditioning, native video durations, frame inspection, editing, audio timing control, and encoding.

This inventory states tool capabilities. Feasibility of the concrete timing specification is checked in Temporal Structure, after its construction and before its lock.

Resource limits

Let N₀ be the initial locked shot plan's segment count.

- Video budget: 6 × N₀ submitted generation calls across the run.
- Shot attempts: two per (plan version, interval, shot type).
- Source-image generation: two calls; each shot-start reference candidate: two calls.
- Audio generation or full rerender: two attempts across the run.
- User-specified cost and time ceilings take precedence.

A shot attempt includes reference preparation, video generation, conformance, and judgment. Failure at any step consumes that attempt; reference preparation cannot restart outside it.

Count every submitted generation call, including failures, timeouts, and adapter subcalls; exclude status polling. Revisions and segmentation changes do not reset or enlarge the global budgets. Budget exhaustion blocks new generation, not assembly, verification, or logging of available work.

## Perception — cross-modal constant extraction

One pass, two output faces. Separate source observations, user constraints, and derived creative defaults.

Visual constants

- Palette and lighting: dominant hues, saturation range, light direction and quality.
- Primary anchor: identity, position, pose, and facing.
- Named anchors: secondary objects requiring continuity.
- Negative space: proportion and distribution of unoccupied frame area.
- Permitted changes: intended motion or transformations specified by the user.

Scene constants

- Emotion open / close: three words each.
- Progression: ordered, observable milestones from opening to resolution.
- Tension: the single dramatic thread.
- Energy: low / medium / high.

Default progression is monotonic toward emotion-close. Falling loudness or motion may accompany emotional resolution. Encode any user-requested reversal before locking.

Temporal defaults

| Property | Default derivation |
|---|---|
| Tempo range | Low energy: 60–80 BPM; medium: 80–120; high: 120–160 |
| Mode | Opening and resolution tonalities from the emotional arc |
| Timbre | Warm: acoustic/strings; cool/dark: electronic/ambient; metallic: synthetic pads/low brass |
| Density | More negative space → sparser arrangement; denser composition → fuller arrangement |
| Genre | Human: vocal-compatible; mechanical: electronic; landscape: ambient/orchestral; cosmic: orchestral-ambient without vocals |

These are overridable creative defaults. Record user overrides before locking. Exact tempo and phrase timing are selected in the next stage within the approved constraints.

Perception lock

Validate the interpretation against the source and user intent, resolve conflicting defaults, and define observable acceptance criteria. Lock the resulting scene specification; do not certify a temporal structure that has not yet been constructed.

## Temporal Structure — the skeleton (code, not sound)

Construct a shared timing specification for visual segments and musical events.

Timebase

- Store fps as a positive rational number.
- Use nearest-integer rounding, with half ties rounded upward: round(x) = floor(x + 0.5) for nonnegative values.
- N = round(T_requested × fps); reject N < 1.
- T_effective = N / fps; record requested and effective durations.
- Valid frame indices are 0 through N−1. N is the exclusive end boundary, not a frame index.

Segments are positive-length intervals [start_frame, end_frame) whose union is [0, N), without gaps or overlaps. An end_frame may equal N.

Musical timing defaults

Fixed tempo; 4/4; quarter-note BPM; first downbeat at time 0; typical phrase length four bars. Explicitly define any alternate meter, tempo map, or pickup offset.

Compute each beat from its absolute ideal time, then quantize:

f_k = round(ideal_beat_time(k) × fps)

Populate beat_grid_frames only with distinct indices satisfying 0 ≤ f_k < N. Quantization error per retained event must be at most half a frame. Do not accumulate rounded beat lengths.

Phrases and legal cut points

- Derive phrase lengths from duration, musical structure, and the capability inventory; four bars is a default.
- A shorter final phrase is permitted with an explicit musical ending.
- Internal phrase boundaries belong to the beat grid, preferably at bar boundaries.
- transitions_frames contains those internal phrase boundaries: 0 < frame < N.
- cut_frames is the subset of transitions where the shot actually changes. Other beat-grid positions do not authorize cuts.
- The terminal boundary N may be off-grid. Continuous shots may span multiple phrases.

Example

Illustrative values: 30 seconds, 24 fps, 96 quarter-note BPM. Frame 719 is the final frame; 720 is the end boundary.

```yaml
temporal_structure:
  version: 1
  perception_version: 1
  requested_duration_seconds: 30
  fps: {numerator: 24, denominator: 1}
  total_frames: 720
  effective_duration_seconds: 30
  bpm: 96
  bpm_unit: quarter_note
  time_signature: "4/4"
  first_downbeat_seconds: 0
  tempo_type: constant
  mode: "A minor → C major"
  dynamic_arc: "establish → build and peak → resolve"
  phrases:
    - {id: 1, start_frame: 0, end_frame: 240, dynamic: pp, role: intro}
    - {id: 2, start_frame: 240, end_frame: 480, dynamic: f, role: build_and_peak}
    - {id: 3, start_frame: 480, end_frame: 720, dynamic: mp, role: resolve}
  transitions_frames: [240, 480]
  beat_grid_frames:
    [0, 15, 30, 45, 60, 75, 90, 105,
     120, 135, 150, 165, 180, 195, 210, 225,
     240, 255, 270, 285, 300, 315, 330, 345,
     360, 375, 390, 405, 420, 435, 450, 465,
     480, 495, 510, 525, 540, 555, 570, 585,
     600, 615, 630, 645, 660, 675, 690, 705]
```

Feasibility and lock

After constructing the candidate structure, verify that every interval has a supported generation-and-conformance route under the duration rules, and that the audio method can render or conform to its event times.

Adjust the unlocked candidate within approved perception constraints until feasible. If none is feasible, stop and report the capability gap. Changes to an already locked layer follow Locking and revision.

Lock the feasible structure. Subsequent refinement, including after visual assembly, requires a controlled revision and revalidation of affected dependencies.

Cross-segment continuation

When generating segment N+1 whose input is the final frame of segment N, the executor must transcribe the observed final-frame state of segment N into the generation directive as explicit continuation constraints. Required transcription fields: subject identity, pose, altitude or ground-contact state, visible named-anchor states, and any active motion (velocity direction, rotation phase).  Planned values from the locked specification must not substitute for observed values; the generation directive describes what the camera currently sees, not what the plan intended.  Omitting this transcription is a conformance failure under JG5.  If the observed final-frame state contradicts the locked plan (e.g., the subject did not reach the planned altitude), the executor must note the deviation and generate segment N+1 from the observed state, not the planned state.

## Shot Plan — sequence design

Shot types

| Type | Camera | Use |
|---|---|---|
| `push` | Forward movement toward subject | Opening, tension, intimacy |
| `static` | Locked position and framing | Holding a moment |
| `detail` | Locked close framing on a source element | Texture or emotional emphasis |

Enable only source-eligible, tool-supported templates. New types must declare eligibility, execution, judgment, and fallback position before use.

Sequence rules

1. Assign one segment per phrase and an enabled shot type. Default opener: push; use static when the scene calls for it.
2. Continue the same type across phrases while judgment passes; condition each continuation on the previous accepted segment's actual last frame.
3. After two failed attempts, use the next enabled, unexhausted type for the same interval.
4. Default rotation: push → static → detail, starting at the current type and skipping unavailable or exhausted types. A rotation does not reset counters.

Only acceptance commits a segment and advances the timeline cursor. If [240, 480) fails as push, its replacement still covers [240, 480).

Cut rules

A replacement using a different shot type starts at the current interval's start boundary. A change at 0 selects the opening shot; later changes must belong to transitions_frames.

Recompose the replacement's starting reference from the source and active scene specification. Carry named anchors, palette, and current emotional position across the cut. A same-type continuation retains the previous ending composition.

Lock interval assignments, enabled templates, starting references or reference rules, and fallback order before execution.

## Per-Shot Execution

The VEM orchestrates; each template executes against the locked scene and timing specifications.

IML-SHOT-PUSH

- Eligibility: an identifiable subject and a feasible forward path.
- Execution: move toward the subject along that path; preserve scene geometry. No unplanned orbit, lateral travel, reversal, or zoom substitution.
- Local judgment: forward direction, subject relationships, and motion remain coherent; continuous joins preserve composition and movement.

IML-SHOT-STATIC

- Eligibility: a stable composition that can express the assigned scene milestone without camera movement.
- Execution: lock position and framing; keep ambient motion within the approved range. Allow declared micro-movement or subject action, but no unplanned motion source or displacement.
- Local judgment: no camera drift or zoom creep; subject identity, framing, and ambient-motion intensity remain stable.

IML-SHOT-DETAIL

- Eligibility: identify a named, visible source element with a specific narrative or textural purpose. Its defining shape or texture must remain recognizable at output size without inventing missing structure.
- Selection: record the element, source region, desired framing, focus plane, and permitted motion. Inspect the proposed crop or reframe before generating the segment.
- Execution: lock the close framing; the selected element occupies more than 50% of the frame. Preserve its source identity and geometry. Background softening is allowed; unplanned camera motion and focus pulls are not.
- Local judgment: the selected element stays identifiable, dominant, and consistently focused; framing and geometry remain stable. Added markings, components, or fabricated texture that changes its identity fail judgment.
- Unavailable case: if no qualifying element exists, disable detail and rotate among the other enabled types. Do not invent a focal element to keep this fallback available. A failed reference candidate consumes its shot attempt under Resource limits.

Global judgment

For multi-segment videos, verify that every segment after the first carries a cross-segment continuation block transcribed from observed output, not from planned values (§ Cross-segment continuation).

| Rule | Pass | Fail |
|---|---|---|
| JG1 Palette/light | Matches locked palette and lighting, including intended changes | Unplanned hue, saturation, or light change |
| JG2 Anchors | Identity and spatially coherent presence, entrances, and exits | Teleportation, unexplained disappearance, identity change |
| JG3 Emotion | Holds or advances the approved observable progression | Unplanned reversal or reset |
| JG4 Timing | Exact assigned frame count after permitted conformance | Exact coverage cannot be achieved legally |
| JG5 Temporal coherence | Coherent motion, geometry, identity, and joins | Flicker, deformation, motion jumps, or discontinuous joins. Cross-segment continuation transcription (§ Temporal Structure) is a prerequisite; its absence is an automatic JG5 failure. |

Judgment procedure

Screen first, middle, and last frames; then inspect motion throughout the segment and across its preceding join. Three samples alone do not establish temporal consistency.

Judge the conformed output. Cite observable evidence for each failure, including emotional milestones. If required inspection is unavailable, label the candidate unverified; do not commit it.

Timing admission and conformance

Raw duration must fall within ±0.5 seconds of the assigned duration before conformance.

Conform to exactly end_frame − start_frame frames by trimming expendable material or adjusting playback speed by at most ±2%. Ordinary frame-rate conversion and bounded speed resampling are permitted; undeclared freeze frames, loops, and filler are not.

Recheck motion, emotion, and joins after editing. A raw-duration pass does not imply JG4 acceptance; interval tolerances do not accumulate into the final timeline.

Attempt protocol

For each interval and enabled type, generate → conform → judge. Commit a passing result. Otherwise log the failure and retry within the two-attempt limit; after exhaustion, rotate under Sequence rules.

When all enabled types are exhausted, use the remaining controlled revision only if resources permit a viable revised plan. Otherwise stop generation and classify the available result under Completion criteria.

## Visual Assembly

Assemble accepted segments under the active specification into a silent track.

Within a continuous shot

Hard-concatenate segments whose references inherit the previous actual final frame. Inspect composition and motion across each join. Pixel identity is not required; spatial and temporal continuity are.

At a cut point

Hard-cut at the recorded transition frame. Crossfades, dissolves, and wipes are prohibited in the visual track.

Assembly verification

Verify exact coverage of [0, N), no accidental gaps or duplicated join frames, legal cuts, coherent continuous joins, correct resolution, and correct frame rate.

Output the accepted silent track and its actual cut_frames list.

## Audio Render

Protocol

Render the locked tempo, meter, tonal progression, phrase roles, dynamics, timbre, density, genre, and event times against the accepted visual track.

Permitted methods include controllable composition, sample arrangement, or generated music followed by conformance. Render choices must stay within the locked creative range.

Conformance

Declare operations and limits before use: offset correction, phrase-aware trimming or arrangement, bounded time stretching, and musically appropriate audio crossfades. Regeneration remains subject to the audio budget.

Inspect the full result for musical coherence. Failed audio does not authorize moving accepted visual cuts; timeline changes require a controlled revision.

Synchronization verification

Identify corresponding events in the actual rendered audio. Requested timestamps are not measurement evidence.

For each visual cut, measure:

offset = actual_audio_transition_time − cut_frame / fps

Require an identifiable intended transition with absolute offset ≤100 ms. Verify the remaining planned musical events and tempo progression to detect drift, including when the video has no cuts.

Conform working audio to round(T_effective × sample_rate) samples. The 0.1-second duration tolerance applies only to encoded playback verification, not to avoidable working-track mismatch.

## Final Output

Mux

Combine accepted visual and audio tracks into MP4, H.264 + AAC, or the specified output format.

Inspect the encoded result: assembly checks must still pass, playback must be intact, audio must start at its planned offset, duration mismatch must be ≤0.1 seconds, and cut alignment must remain ≤100 ms.

Deliverables

Deliver the final video and a generation log containing:

- Source, user constraints, assumptions, output specification, requested and effective duration.
- Active perception, temporal, and shot-plan versions; overrides and revisions.
- Tools/model versions where known; submitted calls, attempts, rejections, and cited rules.
- Segment intervals, shot types, reference lineage, actual cuts, and conformance operations.
- Audio method, measured event offsets, and final verification results.
- Elapsed time, known cost, manual interventions, unavailable measurements, and remaining limitations.

Report only performed checks and known values.

Completion criteria

| State | Definition |
|---|---|
| **COMPLETE** | Full target coverage; required visual, audio, synchronization, and encoding checks pass; final video and log delivered. |
| **PARTIAL** | COMPLETE is unmet, but accepted footage or a verified silent track is available for delivery. Identify missing intervals, failed stages, and unmet requirements. |
| **FAILED** | No accepted footage is available for delivery. Provide the failure log. |
| **IDEAL** | Optional distinction within COMPLETE: one continuous shot, no shot changes or conformance deviations. Not required. |

iLang IML-VEM v1.2.2 — perception-first, structure-before-sound, bounded recovery.
