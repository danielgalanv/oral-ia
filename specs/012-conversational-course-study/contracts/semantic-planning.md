# Semantic planning — explicit versions of the existing interpreter

## independent-proposition-verification — design only, unavailable

Feature 012 keeps its full conversational scope. A future independent
verifier must assess three separately recorded obligations: (1) requested
propositions/act/referents in the actual turn and context versus selected
goal(s); (2) each atomic output claim versus authorized original page/version
and explicit example assumptions; (3) coverage of every asked proposition
by an answer clause and pertinence of any emitted question. Exact offsets,
source hashes and registered IDs prove structure only. The planner's own
labels, free explanation, a second uncalibrated LLM vote, embedding score or
two agreeing labels cannot self-certify semantic entailment.

Candidate input: actual turn/state version, candidate plan, chosen unit
clauses, original source witnesses and proposed proposition/claim edges.
Candidate output: one of `supported`, `rejected`, `unknown` for each of the
three obligations, independent reviewer identity/evidence, bounded timing and
trace; no authority field for publication. `unknown` and `rejected` must
preserve state and produce a specific clarification or source-limit response,
not silence or another lesson. Normal T090/T150, access, consent and teacher
review remain separate downstream gates. No implementation currently emits
`supported`: [design and frozen controls](../evidence/propositional-verification-design.md).

## input-v10

Explicit experimental version10 selects interpreter8.3.0. It retains the v9
pending-question gate. When the first focus decision proposes a registered
two-goal relation, a bounded local-model check sees the actual turn/context
and both goals' titles, scopes and definitions. It selects whether the
relation is needed, only its primary or secondary goal suffices, or the
referent requires clarification. A single-goal proposal bypasses this check.
This can use up to five calls including correction binding under the existing
30s total budget. Syntax, registered references and canonical IDs are
validated after inference. The check does not validate the truth of a claim,
choose a teaching unit or authorize publication. Earlier versions and the
normal participant runtime remain unchanged.

## input-v9

Explicit experimental version9 selects interpreter8.2.0. It retains v8 focus
selection. Only when the actual context has a pending question and its text,
an additional bounded model selection classifies the new utterance against
that question as an answer attempt, a new request or an unclear referent.
`respond` is offered only for an answer attempt; a new request is routed through
the ordinary act selection, and an unclear referent yields clarification.
The gate does not determine whether an answer is true, choose a source or unit,
assign mastery, or authorize publication. It may use up to four model calls
including a correction contrast within the existing 30s total budget. An
unavailable pending-question text fails explicitly. Earlier versions and the
default interpreter keep their existing behavior.

## input-v8

Explicit experimental version8 selects interpreter8.1.0. It projects the same
readable references as v7, then uses the registered catalog selection path in
two stages: current focus (one goal, one registered relation, or a control) and
act. A correction may need the existing third call to choose a goal-scoped
contrast. The instructions distinguish a comparison already contained within
one goal from a requested cross-goal relation; a relation may be requested
implicitly through an unambiguous reference to previous concepts. Context is
evidence, not authority to retain a pair: when v8 explicitly selects one goal,
binding does not restore the previous pair for rephrase/example/ask. Earlier
versions retain their behavior. Canonical IDs and source/unit/question bindings
are restored and validated as in v7. V8 is an experiment on synthetic draft
previews, not teacher approval or participant publication.

## input-v7

Explicit version7 selects interpreter8.0.0. It projects goal reference labels from
the already existing technical goal titles, then invokes the joint proposal path.
For example an abstract internal goal key can be represented by its specific
title. This is a generic ASCII/underscore normalization of metadata, not a
dictionary of student questions or a change to the teaching content. Empty,
oversized, colliding labels and foreign context goals fail before inference.

The recorded inverse map restores canonical goal references after validation.
Actual input, source IDs, unit IDs, pending question IDs and exact claim binding
are unchanged. Model requests/raw outcomes retain the readable references;
canonical result mapping is explicit in the trace. No response is substituted,
no source permission is added and no teacher/semantic approval is inferred.
The same two-call maximum and30s budget apply. Earlier versions/defaults remain.

## input-v6

Explicit version6 selects existing interpreter7.0.1. One joint intent proposal
uses the existing SemanticIntentPlanV2 field names and actual text/context/goals/
registered relations. The host compiles at most256admissible reference-only JSON
tuples, never teaching answers: registered single goals or pairs, allowed acts,
actual greeting prefix, same-target rephrasing and an actual pending-question
precondition for respond. The owned decoder constrains syntax to those tuples;
post-validation independently checks membership before shared contrast/question
binding. No arbitrary source ID, teacher flag, grade or publication field exists.

`x-oralia-finite-outputs` is an internal syntax annotation, not an authorization
slot. It is carried to the worker separately and removed from the model-visible
schema to avoid expanding the prompt by all alternatives. The general schema is
still shown. Invalid/oversized explicit alternatives fail; they are not ignored.
Finite worker bounds are256object strings of at most512characters each.

A second call is needed only for a single-goal correction contrast. All calls
share30000ms; existing agent wall timeout remains32000ms. Earlier versions stay
explicit and their failures are preserved. Joint syntax is not an independent
semantic verifier, teacher review, public participant integration or G2.

Patch7.0.1 clarifies goal granularity: a single goal may already contain a
comparison, and confusion/practice requests do not themselves introduce another
goal. New requests do not become pending-question answers merely because a
question exists. These instructions are fallible semantic guidance, not a new
verifier. The7.0.0 capture remains unchanged. Posthoc observer revision3 separately
rejects unsolicited secondary goals and referent-pair drift; it is not provided
to the generator and does not confer acceptance.

## input-v5

Explicit version5 selects interpreter6.0.0. The target/action decision has the
same bounded catalog and30s total budget as version4, but outputs semantic
references directly: target_ref is a current goal ID, registered relation ID
prefixed relation:, or an explicit control reference; act is a permitted literal
act name. No numeric ordinal translation is required. Exact key/type/membership
checks precede the shared binding and preview renderer. Unknown references or
extra authority fields fail with no fallback.

After a content target is resolved, terminal clarification/finish controls are
not offered again at the action stage: they belong to target selection. respond
requires the actual pending question/current goal; rephrase requires the same
actual target pair as the previous state. These are state preconditions, not
content oracles. Existing greeting-prefix recognition is separate. Single-goal
correct can still use a third scoped contrast selection. Sources, current-unit
authorization and publication gates are unchanged; this remains preview only.

## input-v4

Explicit `semantic_planning_version=4` / constructor4 selects existing-agent
contract5.1.0. This experimental successor selects a target directly from the
current seven goals and three declared relations, plus clarify/outside/finish;
it does not first impose the failed English artifact taxonomy. The model emits
only target_index. A second finite action_index selects one of nine acts, excluding
respond when no actual pending question exists for the selected current goal.
Greeting uses the existing continuity GREETING prefix rule on actual normalized
input, separately from target/action classification. No domain phrase dictionary
is introduced. Indices are type/range/field checked before resolution;
no undeclared pair can be constructed. The second call receives the selected
target and actual context, without observer expectations.

Existing binding checks are shared: actual pending-question reference for respond,
actual whole input and a goal-scoped third contrast selection for single-goal
correct, registered relation binding for paired correct. The renderer and source
authorization are unchanged. At most three calls share30000ms; first target
selection is capped at12000ms, later stages use only measured remaining time.
No automatic retry, fallback, publication or claim of semantic correctness.
Earlier versions/defaults and their first failures remain separately reproducible.

The first5.0.0 capture used18act/greeting combinations and proposed respond after
the question had been cleared; the independent binding gate rejected it. The
unmodified transfer-direct-catalog-exposed capture preserves that failure and
incorrect software-topic substitutions. State admissibility is a precondition,
not an oracle identifying the correct teaching action.

## input-v1

Input: semantic_planning_version1, actual text/state and bounded goal IDs/descriptions. Output: SemanticStudyPlan (act,goal_ref,greet), no teaching text, score, mastery or permission. Semantic port is explicit constructor dependency; legacy constructors/contracts unchanged. Deadline32s only this opt-in contract. Cancellation does not advance state.

## input-v3

Explicit `semantic_planning_version=3` and constructor `semantic_version=3` select the experimental interpreter contract4.0.0. Defaults and earlier contracts remain unchanged. A first closed local-model call proposes the artifact scope: requirements_document, software_product, mixed or outside_catalog. It receives actual input/context and available goals, without evaluation oracles. Goal scope is derived from current source IDs (procedure/requirements versus testing), not a dictionary of student phrases. Missing or unknown source metadata fails before inference.

The first call has at most8000ms. Existing v2 intent/contrast selection then receives only in-scope goals, registered relations whose two goals remain available, and matching contrast options. Actual context is preserved. All calls share at most30000ms measured total budget, at most three calls; no retry, fallback or timeout increase. A proposed goal outside the scoped set fails. Scope selection is a fallible model proposal, never source authorization, semantic acceptance or teacher review.

Output retains v2 with optional `scope_limit=false`. A true limit is allowed only with clarify and no goal. The inspection renderer states the catalog limitation, emits no lesson and preserves state. Participant publication remains denied. Real-model diagnostic captures must be assessed separately from synthetic protocol tests.

Finite local decoding refinement: a closed object with exactly one required enum
field (1–32 string/integer alternatives) can be sent as explicit JSON alternatives
to the owned CUDA worker. A token-prefix constraint permits only those alternatives
and an end token after a complete alternative. Scope and contrast selection can use
this syntax constraint; the full intent schema still uses a schema hint and strict
post-validation. Ready metadata distinguishes finite-enum support from general
structured decoding; each actual outcome records `finite_decoder`. A partial
deadline output remains rejected. This does not establish that the chosen scope or
contrast is semantically correct, grant permission, or replace independent oracles.

Model proposes interpretation; independent renderer checks goal/reference/action and constructs only registered current unit content. The preview uses explicitly unreviewed technical drafts and refuses participant output. Normal T090 and teaching-unit publication reviewed=True remain mandatory for any future participant binding; no conversion of model prose to trusted data. G2 free-generative gate stays closed. Draft previews and raw generative probes are separate surfaces and separate evidence.

## input-v2

Opt-in `semantic_planning_version=2`, constructor `semantic_version=2`, contract3.1.3. Legacy1.0.0/2.1.2 and candidate3.0.0 remain distinct. The input includes actual current text, context, goal scopes and bounded contrast options from the pending curriculum. No participant route enables this contract yet.

The first call proposes only act/goal/greeting through the v1 closed schema. For a correction, a second call receives only contrasts of that goal and proposes an integer index. The program resolves it to the current option ID. Negative, out-of-range, boolean, string or additional-field selections are rejected. Unknown options never become trusted references.

At most two calls share a total30000ms budget; stage2 uses only the measured remainder and is not started below1000ms. Agent timeout32000ms is unchanged. No generation fallback. Every actual request/raw outcome and index→ID resolution is recorded separately when synthetic capture is explicitly enabled. A deadline/length/error does not advance preview state.

## output-v2

`SemanticStudyPlanV2`: schema_version2, act/goal_ref/greet plus correction_ref, claim_quote and optional reply_to_question_id. For correction, the program binds the exact whole current input as context (maximum4000characters); this does not attribute a belief or certify the selected contrast. It never asks the model to invent or paraphrase the student's claim. Other acts cannot carry a correction binding. A question reference, if supplied, must match the actual pending question; it does not grade or confirm comprehension.

The renderer independently rejects a correction reference outside the proposed goal or outside comparison/correction roles. It emits the selected contrast rather than a fixed correction for the goal, preserves not_assessed and denies participant publication. Exact input binding is traceability, not an independent semantic verdict. Appropriateness still needs negative-capable oracles and independent review.

Earlier3.1.0/3.1.1/3.1.2 captures remain in their immutable experiment folders: full-model quote/plan, staged full binding and staged UUID selection respectively. Their timeouts are not rewritten as success. Current schema/metadata are not evidence that those prior outputs used the new protocol.

## Receiving an answer —3.2.0

The v2 first-stage closed intent schema adds `respond`; legacy v1 remains unchanged. This means the input is proposed as a response to the actual pending question, never a correct answer or demonstration of understanding. The program binds the current question reference; missing references or another goal are rejected independently by the renderer.

The renderer acknowledges receipt and presents the goal's controlled contrast. It records last_response_question_id, removes the pending question and preserves assessment=not_assessed. It neither grades, paraphrases a student's belief nor infers mastery. The state remains a proposed inspection state in RAM, not participant persistence or T090/CAS. Current-source authorization and atomic normal-session binding remain mandatory work in T021.

The change follows the actual failure captured in interactive-index-real: a relevant answer to the question just emitted was treated as a new request for the initial explanation. The successor capture interactive-response-real must be assessed on its actual outputs; tests of the closed schema alone cannot close this gap.
