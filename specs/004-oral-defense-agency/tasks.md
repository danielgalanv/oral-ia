---

description: "Task list for Feature 004 — Agencia de defensa oral y voz opcional"
---

# Tasks: Agencia de defensa oral y voz opcional

**Input**: Design documents from `specs/004-oral-defense-agency/` (spec.md, plan.md,
research.md, data-model.md, contracts/, quickstart.md)

**Prerequisites**: Features 001, 002, 003 DONE — 608 deterministic tests and 1 real-Ollama
test passing as of 2026-10-16. This feature is incremental (FR-033): additive edits to
stable integration points (generation purposes, catalog/templates, router registration,
API client and web route) are permitted when their historical regression tests pass.

**Tests**: Included throughout — this project's established convention (Features 001–003)
and the feature's own risk profile (no-evaluation guarantee, modality/cognition
boundary) make test coverage load-bearing, not optional.

**Organization**: Tasks are grouped by user story (spec.md priorities P1/P2/P3) to enable
independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1–US7, mapping 1:1 to spec.md's User Stories
- Exact file paths are given in every task description

## Path Conventions

Single project, matching plan.md's Project Structure exactly:
`src/oralia/{domain,application,infrastructure,interfaces}/`, `apps/web/src/routes/`,
`tests/{contract,integration,failure,unit,speech}/`.

---

## Phase 1: Setup

**Purpose**: Project-level scaffolding needed before any feature code exists.

- [X] T001 Add the `speech` pytest marker to `pyproject.toml`
  (`[tool.pytest.ini_options].markers`, same pattern as the existing `ollama` marker) and
  add an optional dependency group
  `speech = ["faster-whisper>=1.2.1,<2", "piper-tts>=1.8,<2"]` under
  `[project.optional-dependencies]` — no core dependency added, nothing else in
  `pyproject.toml` changes.
- [X] T002 [P] Create the package skeleton `src/oralia/infrastructure/speech/__init__.py`.
- [X] T003 [P] Create the test package skeleton `tests/speech/__init__.py`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Persistence and activity-configuration plumbing that every user story below
needs. No user story work can begin until this phase is complete.

**⚠️ CRITICAL**: No table/column of Features 001–003 is altered — only 4 new classes are
appended to `models.py` and one migration adds them via `create_table` only.

- [X] T004 Extend `src/oralia/infrastructure/db/models.py` **additively, at the end of the
  file**: add the 4 new SQLAlchemy classes `DefenseActivityConfig`, `Transcript`,
  `TranscriptCorrection`, `ConsentRecord` exactly per data-model.md's field tables — no
  existing class in this file is touched.
- [X] T005 Create the Alembic migration
  `src/oralia/infrastructure/db/migrations/versions/t004_oral_defense_tables.py`
  containing only `create_table` for the 4 new tables (`defense_activity_config`,
  `transcript`, `transcript_correction`, `consent_record`) — no `alter_table` on any
  existing table.
- [X] T006 Implement `src/oralia/application/commands/configure_defense_activity.py`:
  create/update `DefenseActivityConfig` for a given `activity_configuration_id`
  (`mode="oral_defense"` is a plain string value on the already-generic
  `ActivityConfiguration.mode` column — no Feature 001/003 file needs to recognize it
  explicitly). Mirrors `configure_self_study_activity.py`'s pattern: `409` if
  `ActivityConfiguration.immutable_since` is not null; `422` (FR-002a) if
  `initial_questions` is empty **and** the activity has no authorized materials.
- [X] T007 Create `src/oralia/interfaces/api/routers/oral_defense.py` with
  `POST /api/v1/tecnica/activities/{activity_id}/defense-config` wired to T006, and
  register the new router additively in `src/oralia/interfaces/api/app.py` (a single
  `include_router(...)` call, same pattern as the existing `self_study.router`
  registration — no existing route in `app.py` is touched).
- [X] T008 [P] Contract test `tests/contract/test_defense_config.py`: `201`/`200` on a
  valid config, `409` when the activity is already immutable, `422` when
  `initial_questions` is empty and no authorized materials exist (FR-002a).

**Checkpoint**: activity configuration + schema exist — user story phases can begin.

---

## Phase 3: User Story 1 - Realizar una defensa completa por texto (Priority: P1) 🎯 MVP

**Goal**: A student can complete an entire oral-defense session by text alone — question →
answer → retrieval → repregunta/clarify/acknowledge_missing_info/finish → verifiers →
`CognitiveState` → trace → closure → descriptive summary — with zero dependency on
STT/TTS.

**Independent Test**: Configure a defense activity (initial question or materials),
complete a full session by text only, and verify grounded follow-up questions and a
descriptive summary are produced at close.

### Tests for User Story 1

- [X] T009 [P] [US1] Contract test for `FollowUpQuestionAgent` in
  `tests/contract/test_followup_question_agent.py`: validates the input/output schema
  (contracts/defense-agents.md), asserts `status="ok"` even when `referenced_concept`
  cannot be satisfied (the agent never returns `status="error"` for that reason).
- [X] T010 [P] [US1] Contract test for `POST /defense-turns` (text) in
  `tests/contract/test_defense_turns_endpoint.py`: response schema
  (`dialogue_action`/`dialogue_purpose`/`output_text`/`sources`/`state_version`), `404`
  for a missing/inactive session.
- [X] T011 [P] [US1] Integration test: a complete text-only defense session (initial
  question → several repreguntas → voluntary close → summary) in
  `tests/integration/test_defense_text_full_session.py` (US1 Independent Test).
- [X] T012 [P] [US1] Integration test: each repregunta references, verifiably via
  `defense-trace`, the student's answer, a treated concept, or an authorized material
  (`followup_question_generated.referenced_concept`) in
  `tests/integration/test_defense_text_full_session.py`.
- [X] T013 [P] [US1] Integration test: a repregunta on the same topic is returned as
  `dialogue_action="ask"` with `dialogue_purpose="deepen_current_topic"` in
  `tests/integration/test_defense_text_full_session.py`.
- [X] T014 [P] [US1] Integration test: a repregunta that moves to a different authorized
  topic is returned as `dialogue_action="ask"` with `dialogue_purpose="switch_topic"` and
  `followup_question_generated` records source/target concept + reason + evidence; a
  request for a topic outside the authorized scope is rejected/redirected (`409`) in
  `tests/integration/test_defense_dialogue_contract.py`.
- [X] T015 [P] [US1] Integration test: a clear, answerable student response produces a
  normal `dialogue_action="ask"` follow-up, never `clarify`, in
  `tests/integration/test_defense_text_full_session.py`.
- [X] T016 [P] [US1] Integration test (FR-018b): a semantically ambiguous **definitive**
  text response (empty `concepts_mentioned`, or `CoherenceVerifierAgent` detects
  contradiction against the student's own prior statement) produces
  `dialogue_action="clarify"`, requests only the minimal disambiguating information,
  carries no evaluative framing, has its decision and reason traced, and the agency
  re-decides normally after the clarification is received, in
  `tests/integration/test_defense_dialogue_contract.py`.
- [X] T017 [P] [US1] Failure test: a repregunta whose `referenced_concept` cannot be
  satisfied, or that `GroundingVerifierAgent` cannot fundament, resolves to
  `dialogue_action="acknowledge_missing_info"` — never `clarify`, never an agent
  `status="error"` — including the case where grounding and coherence verdicts disagree
  (degradation.md CHK007), in `tests/contract/test_defense_output_authorization_matrix.py`.
- [X] T018 [P] [US1] Failure test: `CoherenceVerifierAgent` detects literal repetition of
  the immediately preceding repregunta → one bounded regeneration attempt →
  `acknowledge_missing_info` if still repetitive, in
  `tests/integration/test_defense_dialogue_contract.py`.
- [X] T019 [P] [US1] Failure test (FR-037): the primary generation adapter fails or is
  unavailable while generating a question/repregunta → an authorized deterministic
  alternative is used, the session is not lost, the failure and the chosen recovery
  action are traced, in `tests/failure/test_defense_generation_degradation.py`.
- [X] T020 [P] [US1] Failure test (FR-037): all authorized generation alternatives are
  exhausted with no valid continuation → a safe, non-fabricating action is selected
  (`acknowledge_missing_info`, `ask` on another authorized topic, or `finish`), never an
  invented repregunta, failure + recovery action traced, in
  `tests/failure/test_defense_generation_degradation.py`.
- [X] T021 [P] [US1] Failure test (degradation.md CHK008): `FollowUpQuestionAgent` cannot
  produce any valid continuation (e.g. no pending concepts, no usable evidence) → the
  same safe, non-fabricating resolution as T020 applies, the session continues, in
  `tests/contract/test_defense_output_authorization_matrix.py`.
- [X] T022 [P] [US1] Unit test: the structural relevance check uses `referenced_concept` ∈
  `concepts_mentioned` ∪ evidence text as its criterion — asserts it is **not** a literal
  string-equality/inequality comparison, in
  `tests/unit/test_defense_relevance_structural.py`.
- [X] T023 [P] [US1] Integration test: across ≥3 turns on the same topic, no two
  repreguntas are literal duplicates and every one references the student's answer, a
  treated concept, or an authorized material via the trace (SC-005 precursor) in
  `tests/integration/test_defense_text_full_session.py`.
- [X] T024 [P] [US1] Integration test: reaching `max_turns`/`max_duration_seconds` closes
  the session automatically (`status="closed_limit_reached"`), produces a descriptive
  summary, and leaves a fully reconstructible trace, in
  `tests/integration/test_defense_text_full_session.py`.
- [X] T025 [P] [US1] Integration test: voluntary closure
  (`status="closed_voluntary"`) gives the same closure/summary/trace guarantees as
  automatic closure, in `tests/integration/test_defense_text_full_session.py`.

### Implementation for User Story 1

- [X] T026 [US1] Extend `GenerationPort.GenerationPurpose` in
  `src/oralia/infrastructure/generation/generation_port.py`: add **only** the value
  `"repregunta"` (additive `Literal` extension). `"pregunta_defensa_inicial"` is **not**
  added — `PracticeQuestionAgent` (Feature 003) is reused unmodified for the initial
  question and keeps using its own existing purpose value (research.md §1/§8). Re-run
  Feature 003's existing generation tests unmodified to confirm no regression.
- [X] T027 [US1] Add a `purpose="repregunta"` extraction branch to
  `src/oralia/infrastructure/generation/deterministic_adapter.py` (additive, same
  extractive pattern already used for `"pregunta_practica"`) — no existing branch is
  modified.
- [X] T028 [US1] Implement `src/oralia/domain/agents/followup_question_agent.py`
  (contracts/defense-agents.md): role `generator`, delegates to `GenerationPort` with
  `purpose="repregunta"`; `previous_question_text`/`student_answer_text` are passed as
  **data**, never interpolated into the fixed `system` instruction (same data/instruction
  boundary already required for materials text, FR-008b of Feature 003); never produces
  scoring/diagnosis/performance commentary; `purpose` is received as a parameter, never
  inferred by the agent.
- [X] T029 [US1] Implement `src/oralia/application/orchestration/defense_agency_composer.py`
  — the single `DefenseAgency` composition (mirrors `self_study_agency_composer.py`'s
  pattern; does **not** import it, per research.md §1): initial question (bank entry, or
  `PracticeQuestionAgent` when the bank is empty) → per-answer pipeline: extract
  `concepts_mentioned` via a **new, local, private** helper function analogous to
  `self_study_agency_composer.py`'s `_concept_label` (replicated, not imported) → FR-018b
  cognitive-clarify check (empty `concepts_mentioned`, or `CoherenceVerifierAgent` finds a
  contradiction against the student's own prior statement) → `MaterialRetrieverAgent` →
  `FollowUpQuestionAgent` → `GroundingVerifierAgent` + `CoherenceVerifierAgent` combination
  (contracts/defense-agents.md's verdict table) → puerta final T090 con snapshot confiable,
  plantilla catalogada y binding completo →
  `dialogue_action` resolution (`ask`/`clarify`/`acknowledge_missing_info`/`finish`) →
  `CognitiveState` update via the existing `StatePatch` mechanism (zero new fields,
  research.md §11) → `TraceEvent` recording (`agent_execution`, `generation_call`,
  `verification_combined`, `followup_question_generated`, `turn_completed`).
- [X] T030 [US1] Implement the FR-037 degradation branch inside
  `defense_agency_composer.py` (same file as T029): on generation failure/unavailability,
  try authorized alternatives (bank question / deterministic fallback) before falling
  back to a safe non-fabricating `dialogue_action`; reuses `execute_agency`/
  `run_with_deadline`/`SafeFallbackAgent` (Feature 001, unchanged) — no second fallback
  mechanism is introduced.
- [X] T031 [US1] Implement `src/oralia/application/commands/submit_defense_turn.py` (text
  turn command), wiring session/turn persistence to `defense_agency_composer.py`.
- [X] T032 [P] [US1] Implement
  `src/oralia/application/services/defense_session_summary_service.py`: deterministic,
  code-only construction of the descriptive summary from already-persisted facts
  (`turn_count`, `duration_seconds`, `questions_asked`, `topics_covered`/
  `concepts_mentioned`, `sources_consulted_fragment_ids`, `clarifications_count`,
  `incidents`) per FR-029/FR-029a — no generative call of any kind; own file, same
  pattern as `study_session_summary_service.py` (accepted technical debt, research.md
  §1 — not a shared module).
- [X] T033 [US1] Implement `src/oralia/application/commands/end_defense_session.py`
  (basic closure for this phase: calls `close_session_with_outcome`; only
  `transition_won=true` calls T032 and returns `defense_summary`; consent capture is added
  later in US7).
- [X] T034 [US1] Wire `POST /defense-sessions/{id}/defense-turns` (text),
  `POST /defense-sessions/{id}/defense-end` (basic), and
  `GET /tecnica/defense-sessions/{id}/defense-trace` (reusing
  `reconstruct_session_trace`, Feature 001, unchanged) into
  `src/oralia/interfaces/api/routers/oral_defense.py` (same file created in T007).
- [X] T035 [P] [US1] Create the minimal accessible UI shell
  `apps/web/src/routes/DefensaOral.tsx` for the text-only flow (question display, text
  input, pre-answer purpose/limits/audio/retention disclosure, transcript review,
  keyboard operability, pause/repeat-question/pace controls per FR-004/FR-020/FR-035) —
  same accessibility pattern as `Autoestudio.tsx`.

**Checkpoint**: User Story 1 (MVP) is fully functional and independently testable by text
alone.

---

## Phase 4: User Story 2 - Nunca recibir una evaluación académica (Priority: P1)

**Goal**: Confirm that the complete T090 final gate blocks evaluative content end-to-end
inside `DefenseAgency`, with a trusted snapshot and exact catalog binding.

**Independent Test**: Force a test proposal containing grade/pass-fail content through the
defense pipeline and verify it is never published; only one independently verified
operational fallback may replace it, otherwise the response has `output_text=null`.

- [X] T036 [P] [US2] Contract test in `tests/contract/test_defense_output_authorization_matrix.py`
  (Quickstart Escenario E): a fixture proposal containing `"nota: 8"`/`"has aprobado"`
  fed through `DefenseAgency` is blocked by the final gate, the prohibited candidate is
  absent from persistence/transport, and the fixture covers both an authorized single
  operational fallback and a blocked fallback ending with `output_text=null`.
- [X] T037 [P] [US2] Failure test in
  `tests/integration/test_defense_summary_authorization.py` (FR-029a): incidents,
  clarifications, and repreguntas in the closing summary are always described as
  observable system facts, never as characterization of comprehension, effort,
  performance, or capacity.
- [X] T038 [P] [US2] Negative-assertion suite in
  `tests/failure/test_defense_no_evaluation.py`: asserts the absence of
  grade/score/level/performance/capacity/competence content across turn responses and the
  summary, and that STT confidence is never usable as an academic signal (FR-027).

**Checkpoint**: US1 + US2 — text-only defense with the no-evaluation guarantee verified.

---

## Phase 5: User Story 3 - Responder por voz con transcripción local corregible (Priority: P2)

**Goal**: Voice input with local transcription, student-correctable before it reaches the
cognitive pipeline, plus optional literal voice output — audio never persisted, single
`DefenseAgency` shared with text.

**Independent Test**: With voice enabled, answer orally, correct the shown transcription,
and verify the next repregunta reflects the corrected version, not the original.

### Tests for User Story 3

- [X] T039 [P] [US3] Contract test for `TranscriptionPort` (using a deterministic fake
  adapter) in `tests/contract/test_defense_speech_ports.py`.
- [X] T040 [P] [US3] Contract test for `SpeechSynthesisPort` (using a deterministic fake
  adapter) in `tests/contract/test_defense_speech_ports.py`.
- [X] T041 [P] [US3] Contract test for `POST /defense-turns/voice` in
  `tests/contract/test_defense_speech_endpoint.py`: response shape (`transcript_id`,
  `segments`, `overall_confidence`, `low_confidence`), `409` when
  `voice_input_allowed=false`.
- [X] T042 [P] [US3] Contract test for `POST /defense-turns/voice/confirm` in
  `tests/contract/test_defense_speech_endpoint.py`.
- [X] T043 [P] [US3] Integration test: confirming without edits makes `Transcript.raw_text`
  the definitive version and creates **no** `TranscriptCorrection` row, in
  `tests/integration/test_defense_voice_lifecycle.py` (Quickstart Escenario B,
  situation B).
- [X] T044 [P] [US3] Integration test: confirming with `corrected_text` creates a
  `TranscriptCorrection`, preserves the original `Transcript.raw_text` unchanged, and the
  next repregunta is demonstrably built from the corrected text, in
  `tests/integration/test_defense_voice_lifecycle.py`.
- [X] T045 [P] [US3] Integration test: correcting a transcript after a repregunta was
  already generated from the original version does not retroactively rewrite the
  already-shown repregunta — the correction applies only from that point forward, in
  `tests/integration/test_defense_correction_not_retroactive.py` (Edge Cases).
- [X] T046 [P] [US3] Test asserting audio is never persisted — no table, column or trace
  references it and no multipart temp file remains after the request — by inspecting the
  `Transcript` schema, DB state and forced-spool lifecycle, in
  `tests/contract/test_defense_rolled_spool_lifecycle.py`.
- [X] T047 [P] [US3] Integration test: TTS synthesizes exactly the final, already-verified
  `output_text` — never a pre-verification `GeneratedProposal`, never reformulated,
  summarized, or modified, in `tests/contract/test_defense_speech_endpoint.py` (FR-023).
- [X] T048 [P] [US3] Integration test: the same student-answer content submitted once via
  text and once via voice (confirmed) produces the same `dialogue_action`/
  `referenced_concept` structure — asserts a single `DefenseAgency` code path, not two,
  in `tests/integration/test_defense_voice_lifecycle.py` (SC-001 applied here).
- [X] T049 [P] [US3] Real-model test (marker `speech`, skipped by default, requires
  `ORALIA_STT_MODEL`) transcribing a fixture `.wav` with actual `faster-whisper` in
  `tests/speech/test_faster_whisper_real.py`.
- [X] T050 [P] [US3] Real-model test (marker `speech`, skipped by default, requires
  `ORALIA_TTS_VOICE`) synthesizing a fixture string with actual Piper in
  `tests/speech/test_piper_real.py`.

### Implementation for User Story 3

- [X] T051 [P] [US3] Define the `TranscriptionPort` protocol and `TranscriptionOutcome`
  model in `src/oralia/infrastructure/speech/transcription_port.py`
  (contracts/defense-agents.md).
- [X] T052 [P] [US3] Define the `SpeechSynthesisPort` protocol and `SynthesisOutcome`
  model in `src/oralia/infrastructure/speech/synthesis_port.py`.
- [X] T053 [P] [US3] Create `src/oralia/infrastructure/speech/config.py`:
  `ORALIA_STT_MODEL`, `ORALIA_STT_DEVICE`, `ORALIA_STT_COMPUTE_TYPE`,
  `ORALIA_TTS_VOICE`, `ORALIA_STT_LOW_CONFIDENCE_THRESHOLD` (default `0.6`), worker
  capacity/deadlines and fixed input limits (10 MiB/300 s), mirroring
  `infrastructure/generation/config.py`'s strict parsing pattern.
- [X] T054 [US3] Implement `FasterWhisperTranscriptionAdapter` in
  `src/oralia/infrastructure/speech/faster_whisper_adapter.py` (local, optional
  dependency) — receives bounded content from the router, never creates a named file and
  never persists or references audio; any multipart spool is owned and closed by the router.
- [X] T055 [US3] Implement `PiperSpeechSynthesisAdapter` in
  `src/oralia/infrastructure/speech/piper_adapter.py` (local, optional dependency).
- [X] T056 [P] [US3] Implement deterministic `FakeTranscriptionAdapter`/
  `FakeSpeechSynthesisAdapter` test doubles in `tests/fixtures/speech_adapters.py`
  (research.md §18 — same role `DeterministicGenerationAdapter` plays in production,
  here as a test double so the mandatory suite never needs real models).
- [X] T057 [US3] Implement `src/oralia/application/commands/submit_defense_voice_turn.py`:
  receives audio, calls `TranscriptionPort.transcribe()`, persists the provisional
  `Transcript`, discards the in-memory audio reference immediately after the call
  (success or failure), records `TraceEvent transcription_recorded` — invokes **no**
  cognitive component.
- [X] T058 [US3] Implement
  `src/oralia/application/commands/confirm_defense_transcript.py`: resolves
  `corrected_text` (creates `TranscriptCorrection` if non-null) or reuses
  `Transcript.raw_text` as definitive, records `TraceEvent transcript_corrected` when
  applicable, then hands the definitive text to `defense_agency_composer.py`'s common
  pipeline (same code path as a text turn).
- [X] T059 [US3] Extend the turn response with a speech descriptor only after
  `output_text` is approved and persisted; TTS is requested later through the dedicated
  endpoint and MUST NOT run inside the cognitive composer.
- [X] T060 [US3] Wire `POST /defense-turns/voice`,
  `POST /defense-turns/voice/confirm` and
  `POST /defense-turns/{turn_id}/speech` into `oral_defense.py` (same file as T034),
  following contracts/api-oral-defense.md.
- [X] T061 [P] [US3] Extend `DefensaOral.tsx` (same file as T035) with voice capture UI
  (record/stop, transcription review/correction, switch-to-text control) — same
  accessibility pattern as the text shell.

**Checkpoint**: US1–US3 — voice input/output with correctable local transcription works,
audio is never persisted, cognitive equivalence with text is verified.

---

## Phase 6: User Story 4 - Continuar por texto cuando falla la voz (Priority: P2)

**Goal**: Every voice failure path (capture/transcription/synthesis) degrades to text
without losing session state.

**Independent Test**: Force a simulated capture/transcription failure mid voice-session
and verify the session continues by text without losing already-reached state.

- [X] T062 [P] [US4] Integration test: `TranscriptionPort.transcribe()` returns failure
  (`ok=false`) → the audio (already discarded) is not retried, `TraceEvent
  transcription_failed` is recorded, no cognitive component processes the failed attempt,
  session state stays intact, the student can resubmit via `/defense-turns` (text), in
  `tests/failure/test_defense_speech_exceptions.py` (Quickstart Escenario C;
  research.md §18 situation D).
- [X] T063 [P] [US4] Integration test: `SpeechSynthesisPort.synthesize()` fails or times
  out (`run_with_deadline`) → `output_text` remains available, `TraceEvent tts_failed`
  is recorded, `Turn.status` stays `"completed"` (never degraded) in
  `tests/failure/test_defense_speech_exceptions.py` (FR-024).
- [X] T064 [P] [US4] Integration test: a mid-session failure of a non-essential component
  (TTS) does not interrupt the rest of the session — subsequent turns proceed normally,
  in `tests/failure/test_defense_speech_exceptions.py` (Edge Cases).
- [X] T065 [US4] Add failure handling to `submit_defense_voice_turn.py` (T057): catch and
  represent `TranscriptionOutcome.ok=false`, record `transcription_failed`, return a
  response directing the client to the text endpoint — never retries the same audio.
- [X] T066 [US4] Add failure handling to the dedicated speech endpoint/service (T060):
  catch synthesis failure/timeout, record `tts_failed`, return `503`, and keep the
  approved `output_text` and `Turn.status="completed"` unchanged.

**Checkpoint**: US1–US4 — voice degrades gracefully to text at every failure point without
losing session state.

---

## Phase 7: User Story 5 - Pedir aclaración ante una transcripción ambigua (Priority: P2)

**Goal**: Enforce, and verify independently, that STT low-confidence handling is a
pre-cognitive modality incident (FR-022) that never overlaps with FR-018b's cognitive
`clarify`.

**Independent Test**: Feed a transcription flagged with low confidence on a critical term
and verify the system requests clarification before proposing any repregunta.

- [X] T067 [P] [US5] Integration test: `low_confidence=true` in the
  `/defense-turns/voice` response → **no** `dialogue_action` field is present, **no**
  `agent_execution`/`generation_call`/`verification_combined` `TraceEvent` is recorded for
  that turn, the turn stays `awaiting_confirmation`, in
  `tests/integration/test_defense_voice_lifecycle.py` (Quickstart
  Escenario D; research.md §18 situation A) — the key negative assertion distinguishing
  this from T016's `clarify` test.
- [X] T068 [P] [US5] Integration test: from `awaiting_confirmation`, the student corrects
  the text and confirms → `DefenseAgency` only starts after `POST /voice/confirm`, using
  the corrected text exactly as an ordinary text turn, in
  `tests/integration/test_defense_voice_lifecycle.py`.
- [X] T069 [P] [US5] Integration test: from `awaiting_confirmation`, the student abandons
  voice and answers directly via `/defense-turns` (text), with no new recording ever
  requested, in `tests/integration/test_defense_remaining_boundaries.py`.
- [X] T070 [P] [US5] Integration test (FR-022a): a short/underdeveloped **text** answer,
  with no transcription involved, does not trigger the low-confidence confirmation flow
  nor `clarify` by brevity alone — it is treated as a normal answer producing a regular
  follow-up, in `tests/integration/test_defense_remaining_boundaries.py`.
- [X] T071 [P] [US5] Integration test explicitly distinguishing the two mechanisms
  (research.md §18 situations A vs. C): a low-confidence voice transcription never
  reaches `DialogueAction.clarify`, while an equivalent-but-semantically-empty
  **definitive** text answer does, in
  `tests/integration/test_defense_remaining_boundaries.py` — the explicit
  "an STT incident does not activate `DialogueAction.clarify`" test.
- [X] T072 [US5] Implement the `awaiting_confirmation` gating in
  `submit_defense_voice_turn.py`/`confirm_defense_transcript.py` (T057/T058, same files):
  when `low_confidence=true`, surface the flagged dubious segments and gate any call into
  `defense_agency_composer.py` until confirmation/correction is received — enforced by
  construction (the composer is simply not invoked before that point), matching
  research.md §5's agent-exclusion list.
- [X] T073 [P] [US5] Extend `DefensaOral.tsx` (same file as T061) with dubious-segment
  highlighting and the confirm/correct/switch-to-text controls (FR-022).

**Checkpoint**: US1–US5 — the modality-vs-cognition boundary (FR-022 vs. FR-018b) is fully
enforced and independently verified.

---

## Phase 8: User Story 6 - Repreguntas relevantes y no repetitivas (Priority: P2)

**Goal**: Dedicated verification of SC-005 across richer multi-turn scenarios, on top of
the relevance/no-repetition mechanism already built in US1 (T022/T023/T029).

**Independent Test**: Complete several turns on the same topic and verify, via the trace,
that every repregunta references the prior answer or an authorized material, and none
repeats a previous one literally.

- [X] T074 [P] [US6] Integration test: across a session that includes a `switch_topic`
  transition, no repregunta anywhere in the session is a literal duplicate of any earlier
  one, in `tests/integration/test_defense_session_isolation.py`.
- [X] T075 [P] [US6] Integration test: a repregunta with no support in evidence/
  `concepts_mentioned`/materials is never shown to the student —
  `acknowledge_missing_info` is returned instead (SC-005), in
  `tests/integration/test_defense_remaining_boundaries.py`.

**Checkpoint**: US1–US6 — all P1/P2 stories complete; SC-005 fully covered.

---

## Phase 9: User Story 7 - Cerrar la sesión con consentimiento sobre la conservación (Priority: P3)

**Goal**: Consent-gated retention on top of the basic closure already built in US1
(T033) — unified closure rule, purge of expired retained data, no cross-session
aggregation.

**Independent Test**: Configure an activity that allows choosing retain/delete at close,
complete a short session, and verify the student's decision is executed and recorded
correctly.

### Tests for User Story 7

- [X] T076 [P] [US7] Contract test `POST /defense-end` with a `{retain, scope}` body in
  `tests/contract/test_defense_end_consent.py`.
- [X] T077 [P] [US7] Integration test: `transcript_retention_authorized=false` for the
  activity → no `ConsentRecord` is created (nothing to decide), `Transcript`/
  `TranscriptCorrection`/the summary `TraceEvent` are deleted immediately at closure, in
  `tests/integration/test_defense_retention_and_purge.py`.
- [X] T078 [P] [US7] Integration test: `transcript_retention_authorized=true`, participant
  chooses `retain=false` → same immediate deletion as T077, in
  `tests/integration/test_defense_retention_and_purge.py`.
- [X] T079 [P] [US7] Integration test: `transcript_retention_authorized=true`, participant
  chooses `retain=true` with `scope=["transcript"]` → `Transcript`/`TranscriptCorrection`
  survive closure, the summary `TraceEvent` does not (excluded by `scope`), and both
  become subject to `RetentionPolicy.retention_days`, in
  `tests/integration/test_defense_retention_and_purge.py`.
- [X] T080 [P] [US7] Contract test `POST /tecnica/defense/purge-expired` in
  `tests/integration/test_defense_remaining_boundaries.py`: `PurgeResult` counters, only affects
  expired defense sessions with `decision="retain"`.
- [X] T081 [P] [US7] Integration test: purge never touches rows belonging to Features 001/003 sessions nor
  non-expired defense sessions; defense-owned content projections in reused tables
  are erased under the same session retention scope, in
  `tests/integration/test_defense_retention_and_purge.py`.
- [X] T082 [P] [US7] Test: `ConsentRecord.scope` only ever accepts
  `"transcript"`/`"summary"` — audio is never a candidate value under any configuration,
  in `tests/contract/test_defense_end_consent.py`.
- [X] T083 [P] [US7] Failure test (FR-032): no aggregation/correlation of defense data
  across sessions of the same `participant_code` — `defense-trace` only accepts
  `session_id`, no cross-session query path exists, in
  `tests/integration/test_defense_session_isolation.py` (mirrors Feature
  003's equivalent test).
- [X] T084 [P] [US7] Integration test (FR-029 compliance): `DefenseSessionSummary`
  content is limited to FR-029's allowed fields, is reproducible from the same persisted
  structured facts (re-running the deterministic builder twice yields the same summary),
  and contains zero grade/score/level/performance/capacity/competence content, in
  `tests/integration/test_defense_remaining_boundaries.py` — verifies FR-029's
  deterministic, non-generative construction requirement.

### Implementation for User Story 7

- [X] T085 [US7] Extend `end_defense_session.py` (T033, same file) to accept the optional
  `{retain, scope}` request body, create a `ConsentRecord` only when
  `transcript_retention_authorized=true` and `retain=true`, and apply the unified closure
  rule (delete immediately otherwise) per research.md §15, only when
  `close_session_with_outcome.transition_won=true`.
- [X] T086 [US7] Implement
  `src/oralia/application/commands/purge_expired_defense_data.py` (own file, mirrors
  `purge_expired_self_study_data.py`'s pattern, does not modify or import it — accepted
  technical debt, research.md §1): deletes `Transcript`/`TranscriptCorrection`/defense
  `TraceEvent` content past `RetentionPolicy.retention_days`, preserving structural
  audit metadata without session content.
- [X] T087 [US7] Wire `POST /tecnica/defense/purge-expired` into `oral_defense.py` (same
  file as T034/T060).
- [X] T088 [P] [US7] Extend `DefensaOral.tsx` (same file as T061/T073) with the closure
  screen: transcript review + retain/delete choice, shown only when
  `transcript_retention_authorized=true`.

**Checkpoint**: All 7 user stories are independently functional and tested.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final gate before this feature can be declared implemented.

- [X] T089 Run the full deterministic suite
  (`uv run pytest tests/ -q -m "not ollama and not speech"`) and confirm the 608
  pre-existing Feature 001–003 tests plus every new Feature 004 test pass with zero
  regressions.
- [X] T090 [P] Run `ruff` and `black` on every file modified/created by this feature (see
  plan.md's Project Structure) and fix any violation.
- [X] T091 Execute `quickstart.md` end-to-end (Escenarios A–F, trazabilidad, purga),
  confirming every documented "Esperado" assertion holds.
- [X] T092 Run a constitutional conformance review (11 principles) against `DefenseAgency`,
  same PASS/gap-per-principle format used for Feature 003's convergence review.
- [X] T093 Review every additive edit to a Feature 001/002/003 integration point
  (generation purpose/adapter, catalog/templates, router registration and shared API
  contracts) and prove with its existing regression tests that no prior behavior was
  weakened; report the exact changed files instead of requiring the impossible condition
  that historical files remain untouched.
- [ ] T094 (optional, marker `speech`) Run `uv run pytest tests/ -q -m speech` with
  `ORALIA_STT_MODEL`/`ORALIA_TTS_VOICE` configured and confirm T049/T050 pass — not
  required for the implementation-completion gate.

---

## Phase 11: W0 convergence — seguridad, concurrencia, voz efímera y cliente

**Purpose**: close the audited gaps found after Features 001–003 were completed. These
tasks are normative corrections and take precedence over any incompatible wording in
T001–T094. They preserve historical numbering and remain unchecked until implemented.

- [X] T095 [P] [US1] Add `tests/contract/test_defense_output_authorization_matrix.py`
  enumerating every visible candidate branch (initial bank/generated question,
  follow-up, cognitive clarify, missing evidence, generation degradation, limit/
  voluntary close and visible summary) and asserting exact catalog identity, full
  binding, trusted `AuthorizationSnapshot`, normal `attempt=0`, at most one operational
  `attempt=1`, and `output_text=None` after a second block (FR-026/FR-038/FR-039).
- [X] T096 [US1] Extend the activity-configuration path in
  `src/oralia/application/commands/configure_defense_activity.py` and the existing T090
  policy/catalog integration points with immutable defense policy and exact versioned
  template references for all T095 branches; historical configurations without a valid
  policy fail closed and receive no invented permission.
- [X] T097 [US1] Add the normal and operational defense entries required by T095 to the
  public `OutputTemplateCatalog`, preserving exact `(id, version, sha256)` resolution;
  add public-API unit tests proving no latest-version substitution and no uncatalogued
  literal can become a visible candidate.
- [X] T098 [US1] Integrate `final_output_gate` in
  `src/oralia/application/orchestration/defense_agency_composer.py` for every T095 branch.
  Build the snapshot from real `Session`/`ActivityConfiguration`/recipient and policy,
  create a new proposal/verdict after every transformation, permit one operational
  fallback only, and return a commit-free decision to the outer command.
- [X] T099 [US1] Update `src/oralia/application/commands/submit_defense_turn.py` so
  sanitized `GeneratedProposal`, final `VerificationResult`, `Turn`, state, trace and
  response are persisted by one outer transaction; rejected content is absent from
  `InternalMessage`, proposal, trace, authorization context, logs, errors and API.
  Add rollback/retry and blocked-null integration tests.
- [X] T100 [P] [US1] Update `tests/contract/test_defense_turns_endpoint.py` and API
  response schemas for `output_text: string|null`, `speech: descriptor|null`, blocked
  safe-close semantics and the absence of a content bubble when the value is null.
- [X] T101 [P] [US3] Add contract/integration tests in
  `tests/contract/test_defense_speech_endpoint.py` and
  `tests/contract/test_defense_voice_and_speech.py` for the dedicated POST speech endpoint:
  exact approved persisted text, WAV bytes, text SHA header, `no-store`, replay by
  regeneration, 404 for null/blocked output, 409 disabled and 503 without changing the
  completed text turn.
- [X] T102 [US3] Implement the dedicated speech endpoint in
  `src/oralia/interfaces/api/routers/oral_defense.py`; resolve the final approved
  `VerificationResult` before calling `SpeechSynthesisPort`, synthesize no other text and
  never persist audio.
- [X] T103 [P] [US3] Extend `apps/web/src/api/client.ts` with typed defense configuration,
  text turn, voice upload/confirm, close, trace and binary speech calls; model nullable
  output and create the speech `Blob` without base64 or hidden persistence.
- [X] T104 [P] [US1] Register `/defensa` explicitly in `apps/web/src/main.tsx` and add a
  route smoke test proving the feature is reachable without changing existing routes.
- [X] T105 [US3] Complete `apps/web/src/routes/DefensaOral.tsx`: text-first workflow,
  upload/review/correct voice, no bubble/audio request for `output_text:null`, WAV
  playback/replay, object-URL revocation, accessible controls and text continuity after
  STT/TTS failure. Add focused component tests.
- [X] T106 [P] [US3] Add `tests/unit/test_blocking_speech_worker.py` reproducing the
  T086/T100 guarantees: process-wide capacity across event loops, FIFO/backpressure,
  cancellation while waiting/running, submit failure permit release, singleton race and
  late-result discard.
- [X] T107 [US3] Implement
  `src/oralia/infrastructure/speech/blocking_speech_worker.py` as a dedicated
  process-wide bounded worker following Feature 002's proven contract; prohibit bare
  `asyncio.to_thread` and SQLAlchemy access in worker callables.
- [X] T108 [P] [US3] Add `tests/contract/test_defense_voice_upload_limits.py` covering
  10 MiB, 300 s, invalid/unknown formats, incremental over-limit input and forced
  `SpooledTemporaryFile` rollover; verify 413/422, zero STT calls and no open/recoverable
  temporary artifact on success, error, timeout and cancellation.
- [X] T109 [US3] Implement bounded multipart consumption and duration validation in
  `src/oralia/interfaces/api/routers/oral_defense.py`, with `await UploadFile.close()` in
  `finally`, and pass only accepted content to `submit_defense_voice_turn`.
- [X] T110 [US3] Update `FasterWhisperTranscriptionAdapter` to use the T107 worker,
  `faster-whisper>=1.2.1,<2`, a configured local model and no silent download; discard
  late results and keep all persistence on the owning coroutine.
- [X] T111 [US3] Update `PiperSpeechSynthesisAdapter` to use the T107 worker,
  `piper-tts>=1.8,<2` and a configured local `.onnx` voice; return bounded WAV data and
  discard late results without touching the approved turn.
- [X] T112 [P] [US4] Add failure tests spanning router/worker/adapters for wait timeout,
  execution timeout, cancellation and late completion; prove no transcript, correction,
  trace, audio reference or delayed HTTP result is written after the request ends.
- [X] T113 [P] [US7] Add
  `tests/integration/test_defense_close_transition_outcome.py` covering sequential and
  concurrent duplicate close plus injected rollback; exactly one winner performs
  summary, consent, retention/deletion, close event and lock release, while losers return
  persisted status with `defense_summary=null`.
- [X] T114 [US7] Refactor `src/oralia/application/commands/end_defense_session.py` to use
  `close_session_with_outcome`; gate every close side effect on `transition_won`, keep
  them in the winning outer transaction and make retry after rollback clean.
- [X] T115 [P] [US7] Align purge model/router/tests with Feature 003's current
  `sessions_matching_criteria` and `sessions_with_rows_deleted` counters and prove scope
  isolation plus immediate deletion when retention is not authorized or chosen.
- [X] T116 [P] Update `specs/004-oral-defense-agency/quickstart.md` with executable
  examples for blocked-null output, voice size/duration errors, TTS POST/replay, close
  idempotence and current deterministic/real-model commands; record actual evidence when
  run, never predicted counts.
- [X] T117 Run the complete deterministic regression
  `uv run --no-sync pytest tests/ -q -m "not ollama and not speech"`, the frontend
  TypeScript build/tests and Ruff only on Feature 004 changed files. Every failure must
  be assigned to an unchecked task; no inherited failure may be called expected without
  durable baseline evidence.
- [ ] T118 (optional, marker `speech`) Run the real Faster Whisper and Piper contract
  tests with configured local model/voice, recording exact dependency/model identifiers,
  command, pass/skip/fail counts and warnings separately from the deterministic gate.
- [X] T119 Re-run the seven specialized requirement checklists and constitutional review
  against implemented evidence. Mark only items supported by a file/test/command, keep
  unresolved historical items unchecked, and run `$speckit-analyze`; Feature 004 can
  close only with zero critical contradiction and complete buildable-requirement coverage.

**Checkpoint**: W0 gaps are implemented without weakening Features 001–003; T090 governs
all visible text, T150 governs closure, speech work is bounded, audio is verifiably
ephemeral, and `/defensa` handles nullable output and replay.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: depends on Setup — BLOCKS every user story.
- **US1 (Phase 3, P1, MVP)**: depends only on Foundational. No dependency on STT/TTS code
  at all (US3–US5's phases do not exist yet when US1 is built).
- **US2 (Phase 4, P1)**: depends only on Foundational + US1 (needs a working turn/summary
  pipeline to exercise `ConstitutionalControl` against) — no new production code of its
  own.
- **US3 (Phase 5, P2)**: depends on Foundational + US1 (extends the same
  `defense_agency_composer.py`/`oral_defense.py`/`DefensaOral.tsx` files with the voice
  branch).
- **US4 (Phase 6, P2)**: depends on US3 (there is no voice failure to degrade from before
  voice exists).
- **US5 (Phase 7, P2)**: depends on US3 (same reason).
- **US6 (Phase 8, P2)**: depends on US1 (adds tests only; the mechanism was already built
  there) — independent of US3/US4/US5.
- **US7 (Phase 9, P3)**: depends on US1 (extends `end_defense_session.py`, T033) —
  independent of US3/US4/US5/US6.
- **Polish (Phase 10)**: depends on every user story that was implemented.
- **W0 convergence (Phase 11)**: normative gate discovered after task generation.
  T095–T100 depend on Foundational + US1; T101–T112 depend on US3 and T098/T099;
  T113–T115 depend on US7 and Feature 001 T150; T116–T119 depend on all preceding W0
  tasks. Phase 10's final commands MUST be repeated through T117–T119 after convergence.

### W0 dependency graph

```text
T095 → T096–T097 → T098 → T099 → T100
T106 → T107 → T108–T112
T101 → T102 → T103–T105
T113 → T114 → T115
T100 + T102 + T105 + T112 + T115 → T116 → T117 → T119
T118 is optional and independent of the deterministic completion gate
```

### Within Each User Story

- Tests are written before the corresponding implementation task and MUST fail first.
- Contract tests → Integration/failure tests → Implementation, in the order listed.
- A story's checkpoint marks the point at which it is independently demonstrable end to
  end.

### Parallel Opportunities

- All Setup tasks marked `[P]` run in parallel.
- All Foundational tasks marked `[P]` run in parallel once T004–T007 complete.
- Once Foundational completes, US1 can start; once US1 completes, US2/US3/US6/US7 can
  proceed in parallel (they touch disjoint files except where noted as "same file as
  T0xx", which forces sequencing within that file).
- US4 and US5 can proceed in parallel with each other once US3 completes.
- All test tasks within a story marked `[P]` run in parallel (disjoint files).

---

## Parallel Example: User Story 1

```bash
# Launch all US1 tests together (disjoint files):
Task: "Contract test for FollowUpQuestionAgent in tests/contract/test_followup_question_agent.py"
Task: "Contract test for POST /defense-turns in tests/contract/test_defense_turns_endpoint.py"
Task: "Integration test full text session in tests/integration/test_defense_text_full_session.py"
Task: "Integration test clarify (FR-018b) in tests/integration/test_defense_dialogue_contract.py"
Task: "Failure test FR-037 primary generation fails in tests/failure/test_defense_generation_degradation.py"

# Sequential once tests exist (shared files, ordered dependency):
# T026 (generation_port.py) → T027 (deterministic_adapter.py) → T028 (followup_question_agent.py)
#   → T029/T030 (defense_agency_composer.py) → T031 (submit_defense_turn.py) → T033 (end_defense_session.py)
#   → T034 (oral_defense.py)
# T032 (defense_session_summary_service.py) and T035 (DefensaOral.tsx) run in parallel with the chain above.
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (CRITICAL — blocks every story).
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE**: run US1's tests, execute Quickstart Escenario A.
5. Demo the text-only MVP — this alone satisfies FR-003 ("100% del flujo por texto").

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. US1 → test independently → demo (MVP, text-only).
3. US2 → test independently (no new production code; verification only).
4. US3 → test independently → demo (voice added).
5. US4, US5 → test independently (voice degradation and modality/cognition boundary).
6. US6 → test independently (SC-005 deepened).
7. US7 → test independently → demo (consent-gated retention).
8. Phase 11 W0 convergence → implement the corrected security/concurrency/UI contracts.
9. Repeat Phase 10 gates through T116–T119 → feature gate.

### Notes

- `[P]` tasks touch different files with no completed-task dependency between them.
- `[Story]` labels map every phase-3+ task to its spec.md user story for traceability.
- Record evidence after each task or logical group without commits; validate each story
  independently.
- STT/TTS never become cognitive agents — `TranscriptionPort`/`SpeechSynthesisPort`
  remain plain interface adapters throughout (T051/T052), never registered in an
  `AgencyDefinition`.
- `FollowUpQuestionAgent` (T028) is the only genuinely new cognitive agent in this
  feature — everything else in Features 001–003 is reused through stable contracts or
  extended additively at the integration points inventoried by T093/T096/T097.

## Reconciliación de archivos de prueba (2026-10-17)

Las matrices históricas se agruparon por archivos compartidos, conforme a la instrucción de implementación. Las referencias de tareas apuntan a esos archivos reales; la tabla T001–T119 de `implementation-evidence.md` enlaza evidencia complementaria. Se conservan IDs, requisitos y escenarios. No se crearon wrappers ni archivos vacíos para simular cobertura. La instrucción de no realizar commits prevalece sobre la plantilla genérica.

## Revalidación del cierre tras auditoría independiente (2026-10-17)

Se reabrieron las tareas del flujo de cierre y sus puertas al detectar que la selección
de conservación del cliente no alcanzaba los cierres por límite. La corrección pasa
`closure_consent` en texto y voz confirmada hasta T150, valida el scope y plazo antes
del turno, y escribe consentimiento solo en el cierre ganador. Se añadió revisión
completa desde persistencia y confirmación explícita del cierre voluntario.

`test_defense_automatic_close_consent.py`: 16 combinaciones HTTP aprobadas. Playwright
incluye cierre voluntario, límite exacto de turnos y duración, selección previa,
conservación selectiva, revisión, cierre duplicado y purga. Puerta final completa:
766 deterministas y 9 Playwright aprobados; build/lint/Black PASS, Ruff 0 nuevos.
Las tareas se vuelven a marcar solo tras estas regresiones. T094/T118 no cambian.
