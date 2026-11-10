# Explicit scope-control transport v1

The local cached provider accepts `message_profile="academic/v1"` by default and an explicit opt-in `message_profile="scope-control/v1"`. The default constructs the same academic messages as before, preserving EvidenceItems, the grounding instruction, general-knowledge policy and ordinary conversation history behavior. No participant default is changed.

The opt-in family requires a typed `ScopeControlRequest`, not a generic academic GenerationRequest with an arbitrary JSON payload. It validates the fixed control instruction, typed step, exact data shape, absent academic evidence/history/concepts and `general_knowledge_allowed=false`. A typed control request accidentally sent through the academic default is rejected before serialization. An ordinary academic request or a control-shaped request with a teaching instruction cannot use the control port to bypass its evidence.

Effective wire profiles:

- `scope-control-finite/v1`: target or referent, compiled finite alternatives mandatory, no fallback.
- `scope-control-literal/v1`: exact-text witness extraction, finite alternatives absent. This is not advertised as constrained decoding or semantic verification.

Control frames contain exactly system + user; user wraps the unchanged JSON payload in `<scope_control_data>`. They do not invoke the academic `_build_user_content` rule requiring nonexistent EvidenceItems. The model still receives policy and question as data, with no permission to answer academically or publish.

`scope_message_profiles.py` contains only pure protocol logic and is shared by package imports and the standalone GPU worker. Before tokenizing, the worker validates envelope, role order, fixed instruction, step/profile consistency and finite/open mode; it reports `message_profile` in its response. The adapter records requested/effective/confirmed profiles and raw response. Missing or mismatched control confirmation rejects the result, invalidates the adapter and terminates only its owned worker. The finite classifier independently requires the expected effective profile in each step receipt, in addition to finite flags/membership for selection steps.

`cached_provider` advertises the profile explicitly in construction and checks worker capability metadata for both control profiles. An older worker cannot silently serve this opt-in mode. Academic compatibility does not require profile confirmation from older academic-only frames; new workers report the academic profile as well. Default academic message content is unchanged.

Example of the connected opt-in path (not executed with weights in this delivery):

```python
async with cached_provider(output, source=CACHED_MODEL_7B, quantization="nf4",
                           message_profile="scope-control/v1") as provider:
    result = await classify_finite_scope(question, shown_history, provider=provider,
        binding=binding, db=db, metadata=pinned_metadata, receipt_sink=persist_receipts)
```

Binding/source/metadata revalidation, four-call/512-token/30-second shared budget, literal uncertainty and publication=false remain in the classifier. Profile correctness does not imply scope correctness, claim support, coverage or acceptance. Historical failures stay failures and frozen packages retain original source snapshots. Old manifests intentionally reject a replay with this changed live transport; any future capacity measurement needs an explicit new snapshot and budget, not mutation of the old package.
