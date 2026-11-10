# Revisión humana de continuidad natural — pendiente

Datos y participantes sintéticos. Estas pruebas no validan utilidad con personas ni voz real.

La evaluación negativa histórica de D01 continúa en sus actas originales. Esta revisión sucesora no la reemplaza ni presupone aprobación.


## Bloque 1: development-v7-first/development-agua-docx-oral_defense

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Hola, quiero empezar la defensa.

Respuesta íntegra:

Hola. ¿Cómo explicarías que una tela se seque sin que el agua hierva?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Hola, quiero empezar la defensa.",
  "http_status": 200,
  "response": {
    "turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "Hola. ¿Cómo explicarías que una tela se seque sin que el agua hierva?",
    "state_version": 3,
    "sources": [
      {
        "document_id": "98eed3e5-77bd-4b51-817e-2aacb4ed8010",
        "document_version": 1,
        "location_ref": "Evaporación",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "greeting",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": {
        "turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [
        "4498652c-1f4a-4200-9c76-a4dc2db7d336"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Hola, quiero empezar la defensa.",
    "pending_question_turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
    "pending_question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
    "claim_followup": null,
    "last_approved_unit_ids": [
      "4498652c-1f4a-4200-9c76-a4dc2db7d336"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "greeting",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "e1d5e2762f66ca3845d665d761504bf08e5330a35cefd631fbf1a0f83ce7cfe5",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "53a2b111-ee93-4429-a596-7b8ecd371f8f",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "b5a45213-ccf6-4a6f-9dcc-98624c6a90b6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: El agua desaparece cuando llega a cien grados.

Respuesta íntegra:

¿Estás explicando un cambio de estado o una transformación de la sustancia? ¿Qué distingue ambas ideas en tu razonamiento?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "El agua desaparece cuando llega a cien grados.",
  "http_status": 200,
  "response": {
    "turn_id": "8b9dafb8-58db-4cd5-9111-858e4f443966",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Estás explicando un cambio de estado o una transformación de la sustancia? ¿Qué distingue ambas ideas en tu razonamiento?",
    "state_version": 6,
    "sources": [
      {
        "document_id": "12706820-4a00-4c6d-a65d-591d1f5b3052",
        "document_version": 1,
        "location_ref": "Seguimiento de evaporacion, 1",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "8b9dafb8-58db-4cd5-9111-858e4f443966",
        "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
        "followup_unit_id": "55cad3a4-d029-4efd-bd56-cd58ae8b7c30",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "2fedbeb2-0fe5-4a08-ad46-0c4c9a72b385"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [
        "55cad3a4-d029-4efd-bd56-cd58ae8b7c30"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "El agua desaparece cuando llega a cien grados.",
    "pending_question_turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
    "pending_question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
    "claim_followup": {
      "participant_turn_id": "8b9dafb8-58db-4cd5-9111-858e4f443966",
      "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
      "followup_unit_id": "55cad3a4-d029-4efd-bd56-cd58ae8b7c30",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "2fedbeb2-0fe5-4a08-ad46-0c4c9a72b385"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "55cad3a4-d029-4efd-bd56-cd58ae8b7c30"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "8b9dafb8-58db-4cd5-9111-858e4f443966",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "0aa56d1c71c055444c8c8e50612ed20e8d5cd06a7d7ac473ee55f90aff77e388",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "d006bdeb-3544-4ae3-a3ce-9a4d6451c788",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "b5a45213-ccf6-4a6f-9dcc-98624c6a90b6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
    "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?",
    "strategy_role": 0
  }
}
```


### Paso 3

Participante ficticio: Me rectifico: sale por la superficie sin necesitar hervir.

Respuesta íntegra:

¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Me rectifico: sale por la superficie sin necesitar hervir.",
  "http_status": 200,
  "response": {
    "turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?",
    "state_version": 9,
    "sources": [
      {
        "document_id": "12706820-4a00-4c6d-a65d-591d1f5b3052",
        "document_version": 1,
        "location_ref": "Seguimiento de evaporacion, 2",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
        "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
        "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [
        "f0b4629e-f1eb-482a-a774-358f1fa83a02"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Me rectifico: sale por la superficie sin necesitar hervir.",
    "pending_question_turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
    "pending_question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
    "claim_followup": {
      "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
      "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
      "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "f0b4629e-f1eb-482a-a774-358f1fa83a02"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "4d5382e4fcc1eaf5c8186c978b19a027b70fa78f9baaf0a1eb7f9c421035eeec",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "f15a0236-db9a-49df-b580-619399f6d641",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "b5a45213-ccf6-4a6f-9dcc-98624c6a90b6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "55cad3a4-d029-4efd-bd56-cd58ae8b7c30",
    "text": "¿Estás explicando un cambio de estado o una transformación de la sustancia? ¿Qué distingue ambas ideas en tu razonamiento?",
    "strategy_role": 1
  }
}
```


### Paso 4

Participante ficticio: Necesito una pista para justificarlo.

Respuesta íntegra:

Identifica qué observas antes y después.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Necesito una pista para justificarlo.",
  "http_status": 200,
  "response": {
    "turn_id": "28ed7c49-d8a8-4af3-8a76-0f88210be20c",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "Identifica qué observas antes y después.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "98eed3e5-77bd-4b51-817e-2aacb4ed8010",
        "document_version": 1,
        "location_ref": "Evaporación",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "help",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
        "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
        "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [
        "c1c8c405-2108-41d5-a363-cf5cf8419d50"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Me rectifico: sale por la superficie sin necesitar hervir.",
    "pending_question_turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
    "pending_question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
    "claim_followup": {
      "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
      "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
      "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "c1c8c405-2108-41d5-a363-cf5cf8419d50"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "28ed7c49-d8a8-4af3-8a76-0f88210be20c",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "help",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 1,
    "stalled_signature": "bef1d090db65d6e60cdfe7aa10d68bd370498b24862fd42fefdb0baa1fd9e3a5",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "a593fba0-4bbb-4aee-a653-7d32adb5c6b1",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "b5a45213-ccf6-4a6f-9dcc-98624c6a90b6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
    "text": "¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?",
    "strategy_role": 2
  }
}
```


### Paso 5

Participante ficticio: ¿De dónde procede esa pregunta?

Respuesta íntegra:

La procedencia vigente es agua preguntas, sección Evaporación. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa pregunta?",
  "http_status": 200,
  "response": {
    "turn_id": "a2b35c2b-dd2b-4591-81d1-6277c42f63d3",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "La procedencia vigente es agua preguntas, sección Evaporación. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 15,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
        "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
        "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "approved",
      "latency_ms": 282,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Me rectifico: sale por la superficie sin necesitar hervir.",
    "pending_question_turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
    "pending_question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
    "claim_followup": {
      "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
      "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
      "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "c1c8c405-2108-41d5-a363-cf5cf8419d50"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "28ed7c49-d8a8-4af3-8a76-0f88210be20c",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 1,
    "stalled_signature": "f0cc3843fd95072d920744d42bbd0a74e7ef42cdb62a685b6a41b13a8cee0b11",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "20355090-9c2a-4a66-b71e-ce2a9f6c0768",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "b5a45213-ccf6-4a6f-9dcc-98624c6a90b6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: Termina sin conservar resumen ni transcripción.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Termina sin conservar resumen ni transcripción.",
  "http_status": 200,
  "response": {
    "turn_id": "b7a8d9d9-9ba6-4561-889b-ba7ec6f7d8dc",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
        "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
        "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 282,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Me rectifico: sale por la superficie sin necesitar hervir.",
    "pending_question_turn_id": "6dc93509-dcda-4be3-b104-501a018b11cf",
    "pending_question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
    "claim_followup": {
      "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
      "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
      "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "c1c8c405-2108-41d5-a363-cf5cf8419d50"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "28ed7c49-d8a8-4af3-8a76-0f88210be20c",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 1,
    "stalled_signature": "37a0377c7bd9ab6177bc0683cacae37d845ffc2984a95009b484c3c5adfcaf76",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "88d5cc4e-68d3-4084-a3a3-e23e54aef5d4",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "b5a45213-ccf6-4a6f-9dcc-98624c6a90b6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Lo confirmo.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Lo confirmo.",
  "http_status": 200,
  "response": {
    "turn_id": "2687dd11-0e48-4531-9e71-b312efdf399a",
    "dialogue_action": "finish",
    "dialogue_purpose": null,
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": {
      "turn_count": 7,
      "duration_seconds": 1,
      "questions_asked": [
        "Hola. ¿Cómo explicarías que una tela se seque sin que el agua hierva?",
        "¿Estás explicando un cambio de estado o una transformación de la sustancia? ¿Qué distingue ambas ideas en tu razonamiento?",
        "¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?"
      ],
      "topics_covered": [
        "evaporacion"
      ],
      "concepts_mentioned": [
        "evaporacion"
      ],
      "sources_consulted_fragment_ids": [
        "2fedbeb2-0fe5-4a08-ad46-0c4c9a72b385",
        "4b149aeb-f351-40d2-b079-2e2087cd365a",
        "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
      ],
      "clarifications_count": 0,
      "incidents": [],
      "close_reason": "closed_voluntary"
    },
    "session_status": "closed_voluntary",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "372a671c-994f-40fe-b6ec-de57eabada84",
        "question_unit_id": "4498652c-1f4a-4200-9c76-a4dc2db7d336",
        "followup_unit_id": "f0b4629e-f1eb-482a-a774-358f1fa83a02",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "c9e63a21-32ca-4e90-921e-ebd08b9e86e7"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 281,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {},
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "e9c7aa34-60ad-4402-a7b6-c39c0b3fc298",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "b5a45213-ccf6-4a6f-9dcc-98624c6a90b6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 2: development-v7-first/development-agua-docx-self_study

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Hola, ¿por qué una tela mojada pierde líquido?

Respuesta íntegra:

Hola. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Hola, ¿por qué una tela mojada pierde líquido?",
  "http_status": 200,
  "response": {
    "turn_id": "aa73199c-c0f6-47c9-bc14-de9fa2476650",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Hola. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "9af9f7f5-c5af-485d-bd61-97c9f85a8cb1",
        "document_version": 1,
        "location_ref": "párrafo 6 (Evaporación)",
        "fragment_text": "Por qué. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "faa6fb30-28d4-486b-930d-547ef4f082a2"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 187,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Hola, ¿por qué una tela mojada pierde líquido?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "faa6fb30-28d4-486b-930d-547ef4f082a2"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "aa73199c-c0f6-47c9-bc14-de9fa2476650",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "735b31a0143711e2e5e05ec834a7b2f4db98087d2fd671e391f09fc25c261800",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "ef05a54c-7737-414a-b2f7-2b5544019359",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "d7ef8c96-9a74-44cd-9a27-1c56134dc746",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: Entonces, ¿evaporarse es desaparecer?

Respuesta íntegra:

Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Entonces, ¿evaporarse es desaparecer?",
  "http_status": 200,
  "response": {
    "turn_id": "a22c97d4-2190-4989-b167-1a10c4d561ca",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.",
    "state_version": 6,
    "sources": [
      {
        "document_id": "9af9f7f5-c5af-485d-bd61-97c9f85a8cb1",
        "document_version": 1,
        "location_ref": "párrafo 8 (Evaporación)",
        "fragment_text": "Otra explicación. Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "0b3a7fcb-0037-4678-a999-b1db9f026e0b"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Entonces, ¿evaporarse es desaparecer?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "0b3a7fcb-0037-4678-a999-b1db9f026e0b"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "a22c97d4-2190-4989-b167-1a10c4d561ca",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "c60ced83dea7d6208059197f2ec73a1038e1e0dd27f7482a2c8aaf3f92753de5",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "08844f5c-eba6-4ebd-9779-6e8c10562d23",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "d7ef8c96-9a74-44cd-9a27-1c56134dc746",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 3

Participante ficticio: ¿Qué hacen las moléculas para salir del líquido?

Respuesta íntegra:

Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Qué hacen las moléculas para salir del líquido?",
  "http_status": 200,
  "response": {
    "turn_id": "e869c023-19f0-406b-b8e9-5747469b45ad",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
    "state_version": 9,
    "sources": [
      {
        "document_id": "9af9f7f5-c5af-485d-bd61-97c9f85a8cb1",
        "document_version": 1,
        "location_ref": "párrafo 6 (Evaporación)",
        "fragment_text": "Por qué. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "faa6fb30-28d4-486b-930d-547ef4f082a2"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "¿Qué hacen las moléculas para salir del líquido?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "faa6fb30-28d4-486b-930d-547ef4f082a2"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "e869c023-19f0-406b-b8e9-5747469b45ad",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "abd4d49f003c18205e32100423f2a0bb755446f203ea91b91b771cd5509d7ae6",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "8e0cbba2-a84d-4444-848c-a57442103295",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "d7ef8c96-9a74-44cd-9a27-1c56134dc746",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 4

Participante ficticio: ¿Y cómo pasa, en orden?

Respuesta íntegra:

Primero, identifica vapor de agua en el aire exterior. Después, el contacto con una superficie fría enfría el aire cercano y puede permitir la condensación. Por último, el agua líquida se reúne en gotas visibles. Describe origen, intercambio de energía y resultado en ese orden.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Y cómo pasa, en orden?",
  "http_status": 200,
  "response": {
    "turn_id": "b04873d9-e1a0-4b02-ab12-d4dbf7d7ffef",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Primero, identifica vapor de agua en el aire exterior. Después, el contacto con una superficie fría enfría el aire cercano y puede permitir la condensación. Por último, el agua líquida se reúne en gotas visibles. Describe origen, intercambio de energía y resultado en ese orden.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "9af9f7f5-c5af-485d-bd61-97c9f85a8cb1",
        "document_version": 1,
        "location_ref": "párrafo 33 (Condensación)",
        "fragment_text": "Cómo sucede. Primero, identifica vapor de agua en el aire exterior. Después, el contacto con una superficie fría enfría el aire cercano y puede permitir la condensación. Por último, el agua líquida se reúne en gotas visibles. Describe origen, intercambio de energía y resultado en ese orden.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "c7998f0a-df15-4423-b67e-3e56e6c230a8"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "condensacion",
    "content_query": "¿Y cómo pasa, en orden?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "c7998f0a-df15-4423-b67e-3e56e6c230a8"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "b04873d9-e1a0-4b02-ab12-d4dbf7d7ffef",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "condensacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "condensacion",
    "relevant_concepts": [
      "condensacion"
    ],
    "support_step": 0,
    "stalled_signature": "c1e414ca5ff227f0fef6d39f2f8d3f2087346714f11e36ecb5b6528919ac03ef",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "4b0b1fd1-2cb7-4310-9964-28acb530097f",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "d7ef8c96-9a74-44cd-9a27-1c56134dc746",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 5

Participante ficticio: Sigo sin verlo. Explícamelo de otra manera.

Respuesta íntegra:

Imagina dos reservas diferentes: agua dentro del vaso y vapor fuera. Sigue solo la reserva exterior. Al cambiar de estado junto al vaso, ese vapor da lugar a gotas. Así puedes explicar humedad fuera sin proponer una fuga del recipiente.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Sigo sin verlo. Explícamelo de otra manera.",
  "http_status": 200,
  "response": {
    "turn_id": "b0470a56-1df8-4ea5-8fce-0aa5f046a3bc",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Imagina dos reservas diferentes: agua dentro del vaso y vapor fuera. Sigue solo la reserva exterior. Al cambiar de estado junto al vaso, ese vapor da lugar a gotas. Así puedes explicar humedad fuera sin proponer una fuga del recipiente.",
    "state_version": 15,
    "sources": [
      {
        "document_id": "9af9f7f5-c5af-485d-bd61-97c9f85a8cb1",
        "document_version": 1,
        "location_ref": "párrafo 34 (Condensación)",
        "fragment_text": "Otra explicación. Imagina dos reservas diferentes: agua dentro del vaso y vapor fuera. Sigue solo la reserva exterior. Al cambiar de estado junto al vaso, ese vapor da lugar a gotas. Así puedes explicar humedad fuera sin proponer una fuga del recipiente.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "rephrase",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "f1b5261e-0de5-4319-80c1-8253de1e2274"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 187,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "condensacion",
    "content_query": "¿Y cómo pasa, en orden?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "f1b5261e-0de5-4319-80c1-8253de1e2274"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "b0470a56-1df8-4ea5-8fce-0aa5f046a3bc",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "condensacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "rephrase",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "condensacion",
    "relevant_concepts": [
      "condensacion"
    ],
    "support_step": 1,
    "stalled_signature": "a7d73776223ecaaca19ae8deacd6c866366e7b299054372d2481427dcb1538b3",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "04021ba6-63a9-4fd0-bccf-98731f76a57d",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "d7ef8c96-9a74-44cd-9a27-1c56134dc746",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: ¿De dónde procede esa explicación?

Respuesta íntegra:

La procedencia vigente es 01 agua dossier, sección párrafo 34 (Condensación). Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa explicación?",
  "http_status": 200,
  "response": {
    "turn_id": "b1c3be4d-5b0f-48e7-a199-24f947776846",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La procedencia vigente es 01 agua dossier, sección párrafo 34 (Condensación). Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 391,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "condensacion",
    "content_query": "¿Y cómo pasa, en orden?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "f1b5261e-0de5-4319-80c1-8253de1e2274"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "b0470a56-1df8-4ea5-8fce-0aa5f046a3bc",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "condensacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "condensacion",
    "relevant_concepts": [
      "condensacion"
    ],
    "support_step": 1,
    "stalled_signature": "664766e512786c45cfb9a579dfd633d0c9d7274f64fafa77c79b180e668e9a8c",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "2fb4b506-997b-4895-a2de-fe6b2c1f1a36",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "d7ef8c96-9a74-44cd-9a27-1c56134dc746",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Termina sin conservar resumen ni transcripción.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Termina sin conservar resumen ni transcripción.",
  "http_status": 200,
  "response": {
    "turn_id": "0a660a9b-003c-47f6-a7fc-4d0339f4529b",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 375,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "condensacion",
    "content_query": "¿Y cómo pasa, en orden?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "f1b5261e-0de5-4319-80c1-8253de1e2274"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "b0470a56-1df8-4ea5-8fce-0aa5f046a3bc",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "condensacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "condensacion",
    "relevant_concepts": [
      "condensacion"
    ],
    "support_step": 1,
    "stalled_signature": "bc3b6a3fd73e16d8ddefb9f5c5dcd88731d2d2fd3c3b33e1fb59e2b0a47ce8c7",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "d0701419-39ac-41f0-a5f7-97f0347236ed",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "d7ef8c96-9a74-44cd-9a27-1c56134dc746",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 8

Participante ficticio: Lo confirmo.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Lo confirmo.",
  "http_status": 200,
  "response": {
    "turn_id": "83e1a4c2-37b7-4103-a426-845f32454c13",
    "mode": "doubt_resolution",
    "dialogue_action": "finish",
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 24,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 375,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    },
    "session_closed": true,
    "session_status": "closed_voluntary",
    "study_summary": {
      "turn_count": 8,
      "duration_seconds": 2,
      "modes_used": [
        "doubt_resolution"
      ],
      "concepts_addressed": [
        "evaporacion",
        "condensacion"
      ],
      "practice_questions_count": 0,
      "practice_question_types": [],
      "sources_consulted_fragment_ids": [
        "104a9adc-d63c-41a4-af6a-6358b3bb9d0b",
        "2e07e17d-da46-4e6f-b0fe-2281cd91513b",
        "89c65b8c-9f74-4ee0-bb4f-55386c24c414",
        "dce4762b-1434-4694-9d47-41624e90463a"
      ],
      "incidents": []
    }
  },
  "context": null,
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "6e4fb6ff-6830-4f35-8ad0-4dcacf452692",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "d7ef8c96-9a74-44cd-9a27-1c56134dc746",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 3: development-v7-first/development-datos-pdf-oral_defense

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Hola, quiero empezar la defensa.

Respuesta íntegra:

Hola. ¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Hola, quiero empezar la defensa.",
  "http_status": 200,
  "response": {
    "turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "Hola. ¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?",
    "state_version": 3,
    "sources": [
      {
        "document_id": "ffcfbb86-cbee-4820-8dc8-fb8fed25bff6",
        "document_version": 1,
        "location_ref": "Media aritmética",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "greeting",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": {
        "turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [
        "858e8220-c9ef-41ec-9005-7e173a5d4391"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Hola, quiero empezar la defensa.",
    "pending_question_turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
    "pending_question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
    "claim_followup": null,
    "last_approved_unit_ids": [
      "858e8220-c9ef-41ec-9005-7e173a5d4391"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "greeting",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "f602dd3289ffa7b76e579c1eeb252fbfe371a1f862dc113c584b10e58931b04b",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "b42a39f2-fffe-49c9-8bf5-a3662b107038",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "6c9b90fa-885f-40a3-b955-49f7226f71c5",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: Treinta entre seis intentos da una media de cinco.

Respuesta íntegra:

¿Cómo distingues los intentos realizados de las observaciones disponibles al justificar el divisor?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Treinta entre seis intentos da una media de cinco.",
  "http_status": 200,
  "response": {
    "turn_id": "57ba9081-0b85-4f9f-ba32-d349b6b5b20c",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Cómo distingues los intentos realizados de las observaciones disponibles al justificar el divisor?",
    "state_version": 6,
    "sources": [
      {
        "document_id": "d3001cca-0f4d-4727-8366-90ea0055e8fe",
        "document_version": 1,
        "location_ref": "Seguimiento de media, 1",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "57ba9081-0b85-4f9f-ba32-d349b6b5b20c",
        "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
        "followup_unit_id": "fb871f54-bf5e-4719-83ff-2ed9ece282b3",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "f365bda7-867c-4d09-837e-24aec9fd5657"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [
        "fb871f54-bf5e-4719-83ff-2ed9ece282b3"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 359,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Treinta entre seis intentos da una media de cinco.",
    "pending_question_turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
    "pending_question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
    "claim_followup": {
      "participant_turn_id": "57ba9081-0b85-4f9f-ba32-d349b6b5b20c",
      "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
      "followup_unit_id": "fb871f54-bf5e-4719-83ff-2ed9ece282b3",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "f365bda7-867c-4d09-837e-24aec9fd5657"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "fb871f54-bf5e-4719-83ff-2ed9ece282b3"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "57ba9081-0b85-4f9f-ba32-d349b6b5b20c",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "9a7dee64426afeb61bc0e0411611f0a0d9a6747c5c9a0bb216f1796acf3d555c",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "9a78c644-6b39-4fab-b903-a3624bbc207a",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "6c9b90fa-885f-40a3-b955-49f7226f71c5",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
    "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?",
    "strategy_role": 0
  }
}
```


### Paso 3

Participante ficticio: Rectifico: solo tengo cinco duraciones; el intento sin medida no es cero.

Respuesta íntegra:

¿Qué representa el total y qué representa cada término del reparto que propones?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Rectifico: solo tengo cinco duraciones; el intento sin medida no es cero.",
  "http_status": 200,
  "response": {
    "turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Qué representa el total y qué representa cada término del reparto que propones?",
    "state_version": 9,
    "sources": [
      {
        "document_id": "d3001cca-0f4d-4727-8366-90ea0055e8fe",
        "document_version": 1,
        "location_ref": "Seguimiento de media, 2",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
        "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
        "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "66bf2d3e-5552-4efa-a031-1e1677efdb48"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [
        "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 155,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Rectifico: solo tengo cinco duraciones; el intento sin medida no es cero.",
    "pending_question_turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
    "pending_question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
    "claim_followup": {
      "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
      "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
      "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "66bf2d3e-5552-4efa-a031-1e1677efdb48"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "9d36f2e5bec85db53d348ae949c9c8cfba2e6392952bb0cc2d82a7d844d57c58",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "132180dd-5529-4c62-ac31-c5bd1402a335",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "6c9b90fa-885f-40a3-b955-49f7226f71c5",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "fb871f54-bf5e-4719-83ff-2ed9ece282b3",
    "text": "¿Cómo distingues los intentos realizados de las observaciones disponibles al justificar el divisor?",
    "strategy_role": 1
  }
}
```


### Paso 4

Participante ficticio: Necesito una pista para justificarlo.

Respuesta íntegra:

Comprueba la unidad de los valores.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Necesito una pista para justificarlo.",
  "http_status": 200,
  "response": {
    "turn_id": "9dc4a5be-4a46-43fc-9fc0-1b408708e59e",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "Comprueba la unidad de los valores.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "ffcfbb86-cbee-4820-8dc8-fb8fed25bff6",
        "document_version": 1,
        "location_ref": "Media aritmética",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "help",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
        "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
        "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "66bf2d3e-5552-4efa-a031-1e1677efdb48"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [
        "cbed55c8-6d58-45f0-b57f-f4abd6a186d9"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Rectifico: solo tengo cinco duraciones; el intento sin medida no es cero.",
    "pending_question_turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
    "pending_question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
    "claim_followup": {
      "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
      "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
      "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "66bf2d3e-5552-4efa-a031-1e1677efdb48"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "cbed55c8-6d58-45f0-b57f-f4abd6a186d9"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "9dc4a5be-4a46-43fc-9fc0-1b408708e59e",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "help",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 1,
    "stalled_signature": "7e420583a26e8e0197959abec48b19ea69a11cee98f1b80f549fc80f2dea3326",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "e7580b83-b845-4764-a991-50816ed55b3e",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "6c9b90fa-885f-40a3-b955-49f7226f71c5",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
    "text": "¿Qué representa el total y qué representa cada término del reparto que propones?",
    "strategy_role": 2
  }
}
```


### Paso 5

Participante ficticio: ¿De dónde procede esa pregunta?

Respuesta íntegra:

La procedencia vigente es datos preguntas, sección Media aritmética. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa pregunta?",
  "http_status": 200,
  "response": {
    "turn_id": "c01efa30-5f23-41e9-97ff-cd706355f055",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "La procedencia vigente es datos preguntas, sección Media aritmética. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 15,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
        "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
        "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "66bf2d3e-5552-4efa-a031-1e1677efdb48"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "approved",
      "latency_ms": 297,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Rectifico: solo tengo cinco duraciones; el intento sin medida no es cero.",
    "pending_question_turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
    "pending_question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
    "claim_followup": {
      "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
      "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
      "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "66bf2d3e-5552-4efa-a031-1e1677efdb48"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "cbed55c8-6d58-45f0-b57f-f4abd6a186d9"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "9dc4a5be-4a46-43fc-9fc0-1b408708e59e",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 1,
    "stalled_signature": "00881b3f61f441af0eaf425b5432e1bd349424d592fcc0582fdeca8d0384f4a5",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "e124e388-d2d5-4407-b9b2-76deaac44e28",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "6c9b90fa-885f-40a3-b955-49f7226f71c5",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: Termina sin conservar resumen ni transcripción.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Termina sin conservar resumen ni transcripción.",
  "http_status": 200,
  "response": {
    "turn_id": "fb02bb29-36a7-4268-8bf2-af5906d5bc28",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
        "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
        "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "66bf2d3e-5552-4efa-a031-1e1677efdb48"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 281,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Rectifico: solo tengo cinco duraciones; el intento sin medida no es cero.",
    "pending_question_turn_id": "c2c22629-9088-4c82-a87a-6d43b0fd400f",
    "pending_question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
    "claim_followup": {
      "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
      "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
      "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "66bf2d3e-5552-4efa-a031-1e1677efdb48"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "cbed55c8-6d58-45f0-b57f-f4abd6a186d9"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "9dc4a5be-4a46-43fc-9fc0-1b408708e59e",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 1,
    "stalled_signature": "8aed3cbd490ee7f606966c87b8fc7847dbf180903a89dc814389a6484b794c67",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "c12a4e60-88d3-4a18-85c7-d5a34a652932",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "6c9b90fa-885f-40a3-b955-49f7226f71c5",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Lo confirmo.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Lo confirmo.",
  "http_status": 200,
  "response": {
    "turn_id": "119ad673-9e08-4e3e-ad10-1804a8add669",
    "dialogue_action": "finish",
    "dialogue_purpose": null,
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": {
      "turn_count": 7,
      "duration_seconds": 2,
      "questions_asked": [
        "Hola. ¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?",
        "¿Cómo distingues los intentos realizados de las observaciones disponibles al justificar el divisor?",
        "¿Qué representa el total y qué representa cada término del reparto que propones?"
      ],
      "topics_covered": [
        "media"
      ],
      "concepts_mentioned": [
        "media"
      ],
      "sources_consulted_fragment_ids": [
        "66bf2d3e-5552-4efa-a031-1e1677efdb48",
        "d448b7b2-a07a-41c1-936a-aa8fabbf0e3e",
        "f365bda7-867c-4d09-837e-24aec9fd5657"
      ],
      "clarifications_count": 0,
      "incidents": [],
      "close_reason": "closed_voluntary"
    },
    "session_status": "closed_voluntary",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "638ad313-f4b5-4b1e-9db3-b17f7c391d39",
        "question_unit_id": "858e8220-c9ef-41ec-9005-7e173a5d4391",
        "followup_unit_id": "e4f40a9f-b4ca-48c2-9c0d-54d82a077a89",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "66bf2d3e-5552-4efa-a031-1e1677efdb48"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 295,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {},
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "7c5b7a0a-9a28-48b8-86a3-8762e90f78c1",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "6c9b90fa-885f-40a3-b955-49f7226f71c5",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 4: development-v7-first/development-datos-pdf-self_study

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Hola, antes de calcular léeme los datos de la serie A.

Respuesta íntegra:

Hola. En esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos, tres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el número de observaciones válidas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Hola, antes de calcular léeme los datos de la serie A.",
  "http_status": 200,
  "response": {
    "turn_id": "de675626-8cc5-43a9-b139-0daa946bad08",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Hola. En esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos, tres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el número de observaciones válidas.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "10e18bd1-5c9e-4ab6-b15e-e68ce041a03e",
        "document_version": 1,
        "location_ref": "página 2",
        "fragment_text": "Media aritmética\nEn esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos,\ntres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el\nnúmero de observaciones válidas. Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres,\ncuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta\nentre cinco: la media es seis segundos. Al dividir la suma entre el número de datos, se obtiene un reparto uniforme del total. Un valor\ngrande puede aumentar la media aunque la mayoría de las observaciones sean pequeñas. La suma expresa tiempo acumulado; la media expresa el total por observación. Confundirlas\ncambia tanto el número como la interpretación.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "e5805b75-b5be-4c07-ac67-6f17012fa335"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Hola, antes de calcular léeme los datos de la serie A.",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "e5805b75-b5be-4c07-ac67-6f17012fa335"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "de675626-8cc5-43a9-b139-0daa946bad08",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "307766780554268f3ef2590e9f810d601703b59ab654f0bd242d50d80a4d2877",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "2b0b8afe-5822-4d7e-b3b8-010938c6cbf3",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "ad597b84-b41d-4680-899c-a5f74f01d8f1",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: ¿Obtengo la media dividiendo treinta entre seis intentos?

Respuesta íntegra:

En esta práctica hay seis intentos y cinco duraciones medidas. El intento sin medida no aporta un cero ni otra duración conocida. El divisor de la media cuenta observaciones válidas, no intentos: en la serie A se divide el total de treinta segundos entre cinco valores medidos.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Obtengo la media dividiendo treinta entre seis intentos?",
  "http_status": 200,
  "response": {
    "turn_id": "8ebf97c1-d9ae-4bca-a994-2b06e627330d",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "En esta práctica hay seis intentos y cinco duraciones medidas. El intento sin medida no aporta un cero ni otra duración conocida. El divisor de la media cuenta observaciones válidas, no intentos: en la serie A se divide el total de treinta segundos entre cinco valores medidos.",
    "state_version": 6,
    "sources": [
      {
        "document_id": "5f8a3e2a-e563-40eb-b84c-e1e79dea0448",
        "document_version": 1,
        "location_ref": "Continuidad media, causal-count",
        "fragment_text": "En esta práctica hay seis intentos y cinco duraciones medidas. El intento sin medida no aporta un cero ni otra duración conocida. El divisor de la media cuenta observaciones válidas, no intentos: en la serie A se divide el total de treinta segundos entre cinco valores medidos.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "8e2f1c8b-5b9d-4580-bcfb-31bc741c62de"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "¿Obtengo la media dividiendo treinta entre seis intentos?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "8e2f1c8b-5b9d-4580-bcfb-31bc741c62de"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "8ebf97c1-d9ae-4bca-a994-2b06e627330d",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "a5eaffecea3a8c38b3a5b72c75a547bb284685a98b9c86a906c96b815a56c702",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "8ba8ab1d-02c5-4cf5-9b75-986e2ef8ec7e",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "ad597b84-b41d-4680-899c-a5f74f01d8f1",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 3

Participante ficticio: ¿Cuántas medidas válidas intervienen en el divisor?

Respuesta íntegra:

El divisor usa cinco observaciones válidas de la serie A. El sexto intento sigue sin una duración conocida y queda fuera del reparto. El número de intentos y el número de medidas disponibles son conceptos distintos.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Cuántas medidas válidas intervienen en el divisor?",
  "http_status": 200,
  "response": {
    "turn_id": "81e0b7fc-5409-40b1-9cc1-3a30c9393fc7",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "El divisor usa cinco observaciones válidas de la serie A. El sexto intento sigue sin una duración conocida y queda fuera del reparto. El número de intentos y el número de medidas disponibles son conceptos distintos.",
    "state_version": 9,
    "sources": [
      {
        "document_id": "5f8a3e2a-e563-40eb-b84c-e1e79dea0448",
        "document_version": 1,
        "location_ref": "Continuidad media, count-fact",
        "fragment_text": "El divisor usa cinco observaciones válidas de la serie A. El sexto intento sigue sin una duración conocida y queda fuera del reparto. El número de intentos y el número de medidas disponibles son conceptos distintos.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "0c87bb0d-cd55-4c77-af87-711a9afeffa8"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 187,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "¿Cuántas medidas válidas intervienen en el divisor?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "0c87bb0d-cd55-4c77-af87-711a9afeffa8"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "81e0b7fc-5409-40b1-9cc1-3a30c9393fc7",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "af7da0b51af18f831257da94109a42f8908dc236856e0278d58323d06b0aa07e",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "b56116d0-a70b-4868-bcbf-c9635f65e59c",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "ad597b84-b41d-4680-899c-a5f74f01d8f1",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 4

Participante ficticio: ¿Cómo se hace el cálculo paso a paso?

Respuesta íntegra:

Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres, cuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta entre cinco: la media es seis segundos.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Cómo se hace el cálculo paso a paso?",
  "http_status": 200,
  "response": {
    "turn_id": "f8dd1ccc-50ef-4bf6-ad0f-26feacdbc0e7",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres, cuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta entre cinco: la media es seis segundos.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "10e18bd1-5c9e-4ab6-b15e-e68ce041a03e",
        "document_version": 1,
        "location_ref": "página 2",
        "fragment_text": "Media aritmética\nEn esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos,\ntres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el\nnúmero de observaciones válidas. Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres,\ncuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta\nentre cinco: la media es seis segundos. Al dividir la suma entre el número de datos, se obtiene un reparto uniforme del total. Un valor\ngrande puede aumentar la media aunque la mayoría de las observaciones sean pequeñas. La suma expresa tiempo acumulado; la media expresa el total por observación. Confundirlas\ncambia tanto el número como la interpretación.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "806c9952-da47-4d6b-a4d2-2876fad35aaf"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "¿Cómo se hace el cálculo paso a paso?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "806c9952-da47-4d6b-a4d2-2876fad35aaf"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "f8dd1ccc-50ef-4bf6-ad0f-26feacdbc0e7",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "e198ea62d6292fd64818d36464628d2880d3bb9263e40e4e3c616380c77711f6",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "44da1ed8-3749-4537-ab89-30481a792ea1",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "ad597b84-b41d-4680-899c-a5f74f01d8f1",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 5

Participante ficticio: Para la mediana, ¿cómo empiezo?

Respuesta íntegra:

Primero, ordena las cinco duraciones de menor a mayor. Después, identifica la tercera, porque quedan dos a cada lado. Esa duración es tres segundos. Si hubiera un número par de valores, se usaría la media de los dos centrales.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Para la mediana, ¿cómo empiezo?",
  "http_status": 200,
  "response": {
    "turn_id": "aaa49a82-b5f2-4091-8b91-91fe9a9ccd06",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Primero, ordena las cinco duraciones de menor a mayor. Después, identifica la tercera, porque quedan dos a cada lado. Esa duración es tres segundos. Si hubiera un número par de valores, se usaría la media de los dos centrales.",
    "state_version": 15,
    "sources": [
      {
        "document_id": "10e18bd1-5c9e-4ab6-b15e-e68ce041a03e",
        "document_version": 1,
        "location_ref": "página 3",
        "fragment_text": "Mediana y posición\nLa mediana es el centro de los valores ordenados. Para la serie A ordenada, dos, tres, tres, cuatro y\ndieciocho, la posición central es la tercera y la mediana es tres segundos. Primero, ordena las cinco duraciones de menor a mayor. Después, identifica la tercera, porque\nquedan dos a cada lado. Esa duración es tres segundos. Si hubiera un número par de valores, se\nusaría la media de los dos centrales. La mediana se basa en posiciones del orden, por lo que un valor extremo puede cambiar mucho sin\ndesplazar el valor central en este ejemplo. La media usa la magnitud de todos los valores; la mediana identifica el centro del orden. En la serie\nA la duración dieciocho separa ambas descripciones. En una cantidad par de datos se necesita una media de dos posiciones centrales.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "c7af05b3-506a-45cd-a490-0671a52b0019"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "mediana",
    "content_query": "Para la mediana, ¿cómo empiezo?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "c7af05b3-506a-45cd-a490-0671a52b0019"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "aaa49a82-b5f2-4091-8b91-91fe9a9ccd06",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "mediana"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "mediana",
    "relevant_concepts": [
      "mediana"
    ],
    "support_step": 0,
    "stalled_signature": "ad78e501ed575121b9e87d88d66de07a123e72ba537c3d6752e23acae52b38a9",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "85ae23c4-571e-4e5c-8dd6-2ffb397e0167",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "ad597b84-b41d-4680-899c-a5f74f01d8f1",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: ¿De dónde procede esa explicación?

Respuesta íntegra:

La procedencia vigente es 04 datos practica, sección página 3. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa explicación?",
  "http_status": 200,
  "response": {
    "turn_id": "124281fa-21c0-43a2-83c5-bedcbdfed94a",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La procedencia vigente es 04 datos practica, sección página 3. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 390,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "mediana",
    "content_query": "Para la mediana, ¿cómo empiezo?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "c7af05b3-506a-45cd-a490-0671a52b0019"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "aaa49a82-b5f2-4091-8b91-91fe9a9ccd06",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "mediana"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "mediana",
    "relevant_concepts": [
      "mediana"
    ],
    "support_step": 0,
    "stalled_signature": "6cd067c8871c3ff86ecb35f4d65648808ac60664240a543c40c7063d07642da6",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "0df9106b-61ad-44e0-835e-a1c2c69b3ce3",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "ad597b84-b41d-4680-899c-a5f74f01d8f1",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Termina sin conservar resumen ni transcripción.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Termina sin conservar resumen ni transcripción.",
  "http_status": 200,
  "response": {
    "turn_id": "f65462f9-b44f-44cd-88bd-90d8fc9ae584",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 390,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "mediana",
    "content_query": "Para la mediana, ¿cómo empiezo?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "c7af05b3-506a-45cd-a490-0671a52b0019"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "aaa49a82-b5f2-4091-8b91-91fe9a9ccd06",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "mediana"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "mediana",
    "relevant_concepts": [
      "mediana"
    ],
    "support_step": 0,
    "stalled_signature": "fd8f5d95651eed7b203993319379dc18027f3435b4c06367354f0c66651f5489",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "29491758-1ffe-49b9-98d7-23346e57bee7",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "ad597b84-b41d-4680-899c-a5f74f01d8f1",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 8

Participante ficticio: Lo confirmo.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Lo confirmo.",
  "http_status": 200,
  "response": {
    "turn_id": "238cb0de-b56e-4258-8235-7a1d8559f4c4",
    "mode": "doubt_resolution",
    "dialogue_action": "finish",
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 24,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 391,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    },
    "session_closed": true,
    "session_status": "closed_voluntary",
    "study_summary": {
      "turn_count": 8,
      "duration_seconds": 2,
      "modes_used": [
        "doubt_resolution"
      ],
      "concepts_addressed": [
        "media",
        "mediana"
      ],
      "practice_questions_count": 0,
      "practice_question_types": [],
      "sources_consulted_fragment_ids": [
        "01924cd1-cc41-4508-ae4a-507a8060da13",
        "6e86596e-176a-494b-b0e8-f7d26f055228",
        "bd63a175-259a-408d-850e-ceb2ca9f362e",
        "c210a2a8-49cb-414d-beca-e3d996f949da"
      ],
      "incidents": []
    }
  },
  "context": null,
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "aa44ae72-c434-4166-8f87-9f840ec2704d",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "ad597b84-b41d-4680-899c-a5f74f01d8f1",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 5: development-v7-first/development-programa-docx-oral_defense

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Hola, quiero empezar la defensa.

Respuesta íntegra:

Hola. ¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Hola, quiero empezar la defensa.",
  "http_status": 200,
  "response": {
    "turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "Hola. ¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?",
    "state_version": 3,
    "sources": [
      {
        "document_id": "e2e44a3d-b386-41b8-a070-525ba491129b",
        "document_version": 1,
        "location_ref": "Reglas de validación",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "greeting",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": {
        "turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [
        "59eb3eb7-1250-46f0-a944-0ab5ac592627"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Hola, quiero empezar la defensa.",
    "pending_question_turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
    "pending_question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
    "claim_followup": null,
    "last_approved_unit_ids": [
      "59eb3eb7-1250-46f0-a944-0ab5ac592627"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "greeting",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "ba438c1e38882d541fea8221f44decde0685c9e6af6a5b09f9ac09d18453c1d9",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "4e418b00-096b-410a-8a78-174c6dbb5f31",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9216a46a-a18a-4858-b758-b904e2a63d6c",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: Mil es válido porque solo tiene dígitos.

Respuesta íntegra:

¿Cómo distingues comprobar el formato de comprobar la regla del caso al justificar tu respuesta?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Mil es válido porque solo tiene dígitos.",
  "http_status": 200,
  "response": {
    "turn_id": "030b6195-ba98-48b0-b1ee-599f0a82f1a9",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Cómo distingues comprobar el formato de comprobar la regla del caso al justificar tu respuesta?",
    "state_version": 6,
    "sources": [
      {
        "document_id": "865e35d3-5a8e-4440-86fa-04cf8251f9c2",
        "document_version": 1,
        "location_ref": "Seguimiento de validacion, 1",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "030b6195-ba98-48b0-b1ee-599f0a82f1a9",
        "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
        "followup_unit_id": "c18cadb7-e869-493d-b277-8f2863566498",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "19c2e586-34df-4cf3-b8d9-76dd6274a9d9"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [
        "c18cadb7-e869-493d-b277-8f2863566498"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Mil es válido porque solo tiene dígitos.",
    "pending_question_turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
    "pending_question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
    "claim_followup": {
      "participant_turn_id": "030b6195-ba98-48b0-b1ee-599f0a82f1a9",
      "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
      "followup_unit_id": "c18cadb7-e869-493d-b277-8f2863566498",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "19c2e586-34df-4cf3-b8d9-76dd6274a9d9"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "c18cadb7-e869-493d-b277-8f2863566498"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "030b6195-ba98-48b0-b1ee-599f0a82f1a9",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "08da46738fc89e62567448d3c375294d8027d08d5cb5c06339aac1fb896b4c6a",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "1beb397c-c229-496d-9894-3cac37879fa5",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9216a46a-a18a-4858-b758-b904e2a63d6c",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
    "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?",
    "strategy_role": 0
  }
}
```


### Paso 3

Participante ficticio: Rectifico: cumple formato, pero supera el rango permitido.

Respuesta íntegra:

¿Qué condición necesita cumplirse antes de solicitar la siguiente operación, y cómo la justificarías?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Rectifico: cumple formato, pero supera el rango permitido.",
  "http_status": 200,
  "response": {
    "turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Qué condición necesita cumplirse antes de solicitar la siguiente operación, y cómo la justificarías?",
    "state_version": 9,
    "sources": [
      {
        "document_id": "865e35d3-5a8e-4440-86fa-04cf8251f9c2",
        "document_version": 1,
        "location_ref": "Seguimiento de validacion, 2",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
        "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
        "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "ea271683-8fb8-4000-a983-2ee8fdeaeead"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [
        "5188c82e-14e7-4b90-8a67-cef0094b2954"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Rectifico: cumple formato, pero supera el rango permitido.",
    "pending_question_turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
    "pending_question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
    "claim_followup": {
      "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
      "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
      "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "ea271683-8fb8-4000-a983-2ee8fdeaeead"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "5188c82e-14e7-4b90-8a67-cef0094b2954"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "0320ce090fa7510aa13b1a970efeb9a9652db0defac183deb0b92dfb031ca2bc",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "f5a0a474-6637-450d-8772-53ff0228e675",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9216a46a-a18a-4858-b758-b904e2a63d6c",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "c18cadb7-e869-493d-b277-8f2863566498",
    "text": "¿Cómo distingues comprobar el formato de comprobar la regla del caso al justificar tu respuesta?",
    "strategy_role": 1
  }
}
```


### Paso 4

Participante ficticio: Necesito una pista para justificarlo.

Respuesta íntegra:

Recorre las reglas en su orden.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Necesito una pista para justificarlo.",
  "http_status": 200,
  "response": {
    "turn_id": "dda23b29-82bf-4a7c-a917-0f48793ca05a",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "Recorre las reglas en su orden.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "e2e44a3d-b386-41b8-a070-525ba491129b",
        "document_version": 1,
        "location_ref": "Reglas de validación",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "help",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
        "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
        "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "ea271683-8fb8-4000-a983-2ee8fdeaeead"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [
        "16444a79-2d11-422d-a2d6-a9600fa06433"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Rectifico: cumple formato, pero supera el rango permitido.",
    "pending_question_turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
    "pending_question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
    "claim_followup": {
      "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
      "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
      "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "ea271683-8fb8-4000-a983-2ee8fdeaeead"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "16444a79-2d11-422d-a2d6-a9600fa06433"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "dda23b29-82bf-4a7c-a917-0f48793ca05a",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "help",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 1,
    "stalled_signature": "00cf3df6ee08f4bf6be29a22a509650e35e2c4b67fefab531028f4414b79f7ee",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "12a3ea3f-c995-4abb-920a-8883c0892962",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9216a46a-a18a-4858-b758-b904e2a63d6c",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
    "text": "¿Qué condición necesita cumplirse antes de solicitar la siguiente operación, y cómo la justificarías?",
    "strategy_role": 2
  }
}
```


### Paso 5

Participante ficticio: ¿De dónde procede esa pregunta?

Respuesta íntegra:

La procedencia vigente es programa preguntas, sección Reglas de validación. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa pregunta?",
  "http_status": 200,
  "response": {
    "turn_id": "e23cf64c-1127-4f59-b51e-462e589a19ca",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "La procedencia vigente es programa preguntas, sección Reglas de validación. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 15,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
        "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
        "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "ea271683-8fb8-4000-a983-2ee8fdeaeead"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "approved",
      "latency_ms": 312,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Rectifico: cumple formato, pero supera el rango permitido.",
    "pending_question_turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
    "pending_question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
    "claim_followup": {
      "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
      "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
      "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "ea271683-8fb8-4000-a983-2ee8fdeaeead"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "16444a79-2d11-422d-a2d6-a9600fa06433"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "dda23b29-82bf-4a7c-a917-0f48793ca05a",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 1,
    "stalled_signature": "91eeb78132af6b5ad0f65b795c9318a2f549a01c29521ef478cb7036eecdfb57",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "19564ee3-bf37-4027-b6a5-2cc385f63595",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9216a46a-a18a-4858-b758-b904e2a63d6c",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: Termina sin conservar resumen ni transcripción.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Termina sin conservar resumen ni transcripción.",
  "http_status": 200,
  "response": {
    "turn_id": "eab2ed3c-e814-4326-8dbd-c3d77af6a92f",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
        "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
        "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "ea271683-8fb8-4000-a983-2ee8fdeaeead"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 282,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Rectifico: cumple formato, pero supera el rango permitido.",
    "pending_question_turn_id": "5e698c61-819d-41ad-a592-087f534c622e",
    "pending_question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
    "claim_followup": {
      "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
      "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
      "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "ea271683-8fb8-4000-a983-2ee8fdeaeead"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "16444a79-2d11-422d-a2d6-a9600fa06433"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "dda23b29-82bf-4a7c-a917-0f48793ca05a",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 1,
    "stalled_signature": "8779869651bfd23464920f478b5bc13d3e209a2f86e20e543585b3f782a52355",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "2edfbcb6-edfa-4406-a9c4-e05e7ea585d0",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9216a46a-a18a-4858-b758-b904e2a63d6c",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Lo confirmo.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Lo confirmo.",
  "http_status": 200,
  "response": {
    "turn_id": "58651008-2f76-4301-9999-1369e8e897d0",
    "dialogue_action": "finish",
    "dialogue_purpose": null,
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": {
      "turn_count": 7,
      "duration_seconds": 2,
      "questions_asked": [
        "Hola. ¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?",
        "¿Cómo distingues comprobar el formato de comprobar la regla del caso al justificar tu respuesta?",
        "¿Qué condición necesita cumplirse antes de solicitar la siguiente operación, y cómo la justificarías?"
      ],
      "topics_covered": [
        "validacion"
      ],
      "concepts_mentioned": [
        "validacion"
      ],
      "sources_consulted_fragment_ids": [
        "19c2e586-34df-4cf3-b8d9-76dd6274a9d9",
        "c1191d4e-2b24-4595-8681-5cbfaada728e",
        "ea271683-8fb8-4000-a983-2ee8fdeaeead"
      ],
      "clarifications_count": 0,
      "incidents": [],
      "close_reason": "closed_voluntary"
    },
    "session_status": "closed_voluntary",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "14f188e1-b98c-42c2-8cbc-669733d00817",
        "question_unit_id": "59eb3eb7-1250-46f0-a944-0ab5ac592627",
        "followup_unit_id": "5188c82e-14e7-4b90-8a67-cef0094b2954",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "ea271683-8fb8-4000-a983-2ee8fdeaeead"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 281,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {},
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "a680fc7b-84cd-42d8-b8f8-2d28fe8c286e",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9216a46a-a18a-4858-b758-b904e2a63d6c",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 6: development-v7-first/development-programa-docx-self_study

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Buenas, ¿qué es validar exactamente?

Respuesta íntegra:

Hola. Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Buenas, ¿qué es validar exactamente?",
  "http_status": 200,
  "response": {
    "turn_id": "d107b12c-c91a-4feb-a64b-debb9710e92e",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Hola. Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "738251aa-8437-45d1-96ab-8311cf1b986b",
        "document_version": 1,
        "location_ref": "Definición funcional propuesta, revisión humana pendiente",
        "fragment_text": "Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "19b747b2-9709-41fc-877a-52a8500a083b"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Buenas, ¿qué es validar exactamente?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "19b747b2-9709-41fc-877a-52a8500a083b"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "d107b12c-c91a-4feb-a64b-debb9710e92e",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "1228b354f3dcf2016d5e9b2848300d48600af6d353c82b22072277ae28068bc3",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "f05e75c2-a8d1-4247-b51a-8829f2077ce2",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9fb5b530-41d3-4b77-aec4-1997c518ac33",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: ¿Por qué no lo guardamos y luego vemos si está bien?

Respuesta íntegra:

Validar antes de pedir guardar evita que el programa persista una cantidad que incumple las reglas del caso. Primero se comprueban formato y rango. Solo cuando la validación acepta los datos se solicita guardarlos. Un fallo de escritura es otro problema: una cantidad puede ser válida aunque el archivo no pueda escribirse.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Por qué no lo guardamos y luego vemos si está bien?",
  "http_status": 200,
  "response": {
    "turn_id": "762cb81b-343e-4a42-81b5-30eb43d6ad46",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Validar antes de pedir guardar evita que el programa persista una cantidad que incumple las reglas del caso. Primero se comprueban formato y rango. Solo cuando la validación acepta los datos se solicita guardarlos. Un fallo de escritura es otro problema: una cantidad puede ser válida aunque el archivo no pueda escribirse.",
    "state_version": 6,
    "sources": [
      {
        "document_id": "738251aa-8437-45d1-96ab-8311cf1b986b",
        "document_version": 1,
        "location_ref": "Continuidad validacion, causal-order",
        "fragment_text": "Validar antes de pedir guardar evita que el programa persista una cantidad que incumple las reglas del caso. Primero se comprueban formato y rango. Solo cuando la validación acepta los datos se solicita guardarlos. Un fallo de escritura es otro problema: una cantidad puede ser válida aunque el archivo no pueda escribirse.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "73edc852-bdf9-4ee6-91f2-857c1d9619c8"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Por qué no lo guardamos y luego vemos si está bien?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "73edc852-bdf9-4ee6-91f2-857c1d9619c8"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "762cb81b-343e-4a42-81b5-30eb43d6ad46",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "65b6b2fb9e1fbe2236cd6d7e0e5fa4948c3df08636fd1bf7d5551d11aecbfbae",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "b7966d65-c554-4802-be57-cb094af04d50",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9fb5b530-41d3-4b77-aec4-1997c518ac33",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 3

Participante ficticio: ¿Y si escribo cero cero siete?

Respuesta íntegra:

Entrada cero cero siete: formato admitido, conversión a siete y rango válido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Y si escribo cero cero siete?",
  "http_status": 200,
  "response": {
    "turn_id": "85a2b43a-f986-4703-a0ac-c1c66f86b5a5",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Entrada cero cero siete: formato admitido, conversión a siete y rango válido.",
    "state_version": 9,
    "sources": [
      {
        "document_id": "5990ed35-2796-42e7-b0a7-7a71778fbe39",
        "document_version": 1,
        "location_ref": "párrafo 25 (Reglas de validación)",
        "fragment_text": "Ejemplo 1. Entrada cero cero siete: formato admitido, conversión a siete y rango válido.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "23cb4fb7-f934-45da-98e3-c4a01cabfa9a"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 155,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Y si escribo cero cero siete?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "23cb4fb7-f934-45da-98e3-c4a01cabfa9a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "85a2b43a-f986-4703-a0ac-c1c66f86b5a5",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "d33a49f5d8ba78dd4ae8403a04e5635ef10765d452e244b7c6967ea1486ef225",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "85277597-7134-4620-98d0-e70c5c53ea0d",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9fb5b530-41d3-4b77-aec4-1997c518ac33",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 4

Participante ficticio: ¿Qué ocurre si escribo mil?

Respuesta íntegra:

Entrada mil: dígitos admitidos, conversión posible y rechazo por rango; no se guarda.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Qué ocurre si escribo mil?",
  "http_status": 200,
  "response": {
    "turn_id": "72c408ae-205c-48f0-969e-18b7ccfd4d76",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Entrada mil: dígitos admitidos, conversión posible y rechazo por rango; no se guarda.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "5990ed35-2796-42e7-b0a7-7a71778fbe39",
        "document_version": 1,
        "location_ref": "párrafo 26 (Reglas de validación)",
        "fragment_text": "Ejemplo 2. Entrada mil: dígitos admitidos, conversión posible y rechazo por rango; no se guarda.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "fc8eed29-20a2-4b78-8e53-3cea49b63e70"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 156,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Qué ocurre si escribo mil?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "fc8eed29-20a2-4b78-8e53-3cea49b63e70"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "72c408ae-205c-48f0-969e-18b7ccfd4d76",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "101f4afed7dedfb349a5b69130da3b61b6c1802ea545b3bf52aa95fc781a0555",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "5fe57636-875d-4fb6-9ca1-1f9c85c3c7a0",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9fb5b530-41d3-4b77-aec4-1997c518ac33",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 5

Participante ficticio: ¿Y ese último número cumple el rango?

Respuesta íntegra:

Sí, cero es una cantidad válida. No, mil no es aceptable en este programa. Un número puede ser un entero correcto y aun así incumplir una regla de negocio.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Y ese último número cumple el rango?",
  "http_status": 200,
  "response": {
    "turn_id": "01206d99-f24c-448a-90d4-7ea7d595110a",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Sí, cero es una cantidad válida. No, mil no es aceptable en este programa. Un número puede ser un entero correcto y aun así incumplir una regla de negocio.",
    "state_version": 15,
    "sources": [
      {
        "document_id": "5990ed35-2796-42e7-b0a7-7a71778fbe39",
        "document_version": 1,
        "location_ref": "párrafo 22 (Reglas de validación)",
        "fragment_text": "Qué es posible. Sí, cero es una cantidad válida. No, mil no es aceptable en este programa. Un número puede ser un entero correcto y aun así incumplir una regla de negocio.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "b352ae3c-0215-4ad4-a488-cd33be4e9d26"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Y ese último número cumple el rango?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "b352ae3c-0215-4ad4-a488-cd33be4e9d26"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "01206d99-f24c-448a-90d4-7ea7d595110a",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "5f81d6d2b140f541b113dcb6a5f37450b30119a049be8115a93f73a0dca4699e",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "24aa614c-37f2-4d45-b1a5-0fade67d799e",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9fb5b530-41d3-4b77-aec4-1997c518ac33",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: ¿De dónde procede esa explicación?

Respuesta íntegra:

La procedencia vigente es 02 programa caso, sección párrafo 22 (Reglas de validación). Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa explicación?",
  "http_status": 200,
  "response": {
    "turn_id": "ba501404-b71c-4fde-8e7e-450b51b3f4a0",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La procedencia vigente es 02 programa caso, sección párrafo 22 (Reglas de validación). Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 390,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Y ese último número cumple el rango?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "b352ae3c-0215-4ad4-a488-cd33be4e9d26"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "01206d99-f24c-448a-90d4-7ea7d595110a",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "780d66f2d0bf6f7419d9d2f6aed461bc964a7b4c432e6c8582458edb73b50902",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "8138dab1-63db-4790-b43c-552dd5684d3c",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9fb5b530-41d3-4b77-aec4-1997c518ac33",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Termina sin conservar resumen ni transcripción.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Termina sin conservar resumen ni transcripción.",
  "http_status": 200,
  "response": {
    "turn_id": "6be1efd7-121b-4a69-9760-ec47a6578ab9",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 391,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Y ese último número cumple el rango?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "b352ae3c-0215-4ad4-a488-cd33be4e9d26"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "01206d99-f24c-448a-90d4-7ea7d595110a",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "8779869651bfd23464920f478b5bc13d3e209a2f86e20e543585b3f782a52355",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "f995f53c-2d35-4bbb-91b7-0d33ebe651f9",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9fb5b530-41d3-4b77-aec4-1997c518ac33",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 8

Participante ficticio: Lo confirmo.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Lo confirmo.",
  "http_status": 200,
  "response": {
    "turn_id": "003a49ba-c91f-4336-8502-4bf99ad8f393",
    "mode": "doubt_resolution",
    "dialogue_action": "finish",
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 24,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 390,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    },
    "session_closed": true,
    "session_status": "closed_voluntary",
    "study_summary": {
      "turn_count": 8,
      "duration_seconds": 2,
      "modes_used": [
        "doubt_resolution"
      ],
      "concepts_addressed": [
        "validacion"
      ],
      "practice_questions_count": 0,
      "practice_question_types": [],
      "sources_consulted_fragment_ids": [
        "03a8b689-7884-4aca-a212-e9e3968eb354",
        "2e2ad17c-bef7-4962-9be9-cf7c7fcb5e74",
        "873b86e8-dda4-4180-b8b8-f93d44855a8d",
        "c78393cd-230b-4cdd-888f-52396c7692a3",
        "d3459868-6124-4c7f-abf9-22417256b0ca"
      ],
      "incidents": []
    }
  },
  "context": null,
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "aa74ebc8-9ea9-4398-bd72-634c2c413e95",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "9fb5b530-41d3-4b77-aec4-1997c518ac33",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 7: reserved-v4-third-first/reserved_third-agua-docx-oral_defense

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Buenas tardes, quiero empezar con una pregunta de defensa.

Respuesta íntegra:

Hola. ¿Cómo explicarías que una tela se seque sin que el agua hierva?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Buenas tardes, quiero empezar con una pregunta de defensa.",
  "http_status": 200,
  "response": {
    "turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "Hola. ¿Cómo explicarías que una tela se seque sin que el agua hierva?",
    "state_version": 3,
    "sources": [
      {
        "document_id": "4878959f-6a3e-43e6-9190-fcb515ec3042",
        "document_version": 1,
        "location_ref": "Evaporación",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "greeting",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": {
        "turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [
        "dc6f90f4-2b77-4dd0-934e-7c9006846d8a"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Buenas tardes, quiero empezar con una pregunta de defensa.",
    "pending_question_turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
    "pending_question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
    "claim_followup": null,
    "last_approved_unit_ids": [
      "dc6f90f4-2b77-4dd0-934e-7c9006846d8a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "greeting",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "0a4ec0116444dc3a4420ea245c0148526591ff3e2dd7f3018ede97e82bf09dba",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "5d084b77-4e92-4b69-8308-19b3fdd64150",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "3ff92116-4126-44ec-a7d8-bb26f43cb4c6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: Estoy suponiendo que el vapor es otra sustancia.

Respuesta íntegra:

¿Estás explicando un cambio de estado o una transformación de la sustancia? ¿Qué distingue ambas ideas en tu razonamiento?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Estoy suponiendo que el vapor es otra sustancia.",
  "http_status": 200,
  "response": {
    "turn_id": "be7f8ef1-e2ac-4563-baa3-94a571a897c3",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Estás explicando un cambio de estado o una transformación de la sustancia? ¿Qué distingue ambas ideas en tu razonamiento?",
    "state_version": 6,
    "sources": [
      {
        "document_id": "791c41f3-6144-42ee-9b06-ef55bdf2eb7f",
        "document_version": 1,
        "location_ref": "Seguimiento de evaporacion, 1",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "be7f8ef1-e2ac-4563-baa3-94a571a897c3",
        "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
        "followup_unit_id": "553f5950-fccb-4b0b-bad6-9da5453b8b89",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "370b7609-b6de-4572-bc80-28facb2773af"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [
        "553f5950-fccb-4b0b-bad6-9da5453b8b89"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Estoy suponiendo que el vapor es otra sustancia.",
    "pending_question_turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
    "pending_question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
    "claim_followup": {
      "participant_turn_id": "be7f8ef1-e2ac-4563-baa3-94a571a897c3",
      "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
      "followup_unit_id": "553f5950-fccb-4b0b-bad6-9da5453b8b89",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "370b7609-b6de-4572-bc80-28facb2773af"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "553f5950-fccb-4b0b-bad6-9da5453b8b89"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "be7f8ef1-e2ac-4563-baa3-94a571a897c3",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "4028bed40b1819257cfcd50d839b4c886527f9f7f9a1a652cda88eae54aacc9e",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "177ec4a4-2ead-4acc-8c93-184c63c09638",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "3ff92116-4126-44ec-a7d8-bb26f43cb4c6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
    "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?",
    "strategy_role": 0
  }
}
```


### Paso 3

Participante ficticio: Ahora hablo del estado: el agua sigue siendo la misma sustancia.

Respuesta íntegra:

¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Ahora hablo del estado: el agua sigue siendo la misma sustancia.",
  "http_status": 200,
  "response": {
    "turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?",
    "state_version": 9,
    "sources": [
      {
        "document_id": "791c41f3-6144-42ee-9b06-ef55bdf2eb7f",
        "document_version": 1,
        "location_ref": "Seguimiento de evaporacion, 2",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
        "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
        "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "badb6187-33a5-4ec4-bc14-3c256dbe459c"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [
        "7ca9e50e-a280-41d0-b6c2-07a260ea42b1"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Ahora hablo del estado: el agua sigue siendo la misma sustancia.",
    "pending_question_turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
    "pending_question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
    "claim_followup": {
      "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
      "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
      "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "badb6187-33a5-4ec4-bc14-3c256dbe459c"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "7ca9e50e-a280-41d0-b6c2-07a260ea42b1"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "8f5282a0ca575e07d220144c291d5e01ab42a36b45b77964514c2af39c655f58",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "01be2cc8-d2d9-4f02-a530-f5a05a66c138",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "3ff92116-4126-44ec-a7d8-bb26f43cb4c6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "553f5950-fccb-4b0b-bad6-9da5453b8b89",
    "text": "¿Estás explicando un cambio de estado o una transformación de la sustancia? ¿Qué distingue ambas ideas en tu razonamiento?",
    "strategy_role": 1
  }
}
```


### Paso 4

Participante ficticio: Dame una pista para organizar la justificación.

Respuesta íntegra:

Identifica qué observas antes y después.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Dame una pista para organizar la justificación.",
  "http_status": 200,
  "response": {
    "turn_id": "08509f63-d257-4991-bf19-5dc512eed26c",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "Identifica qué observas antes y después.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "4878959f-6a3e-43e6-9190-fcb515ec3042",
        "document_version": 1,
        "location_ref": "Evaporación",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "help",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
        "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
        "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "badb6187-33a5-4ec4-bc14-3c256dbe459c"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [
        "7ab6a667-1dc3-43b9-905a-98b86944a9fe"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 188,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Ahora hablo del estado: el agua sigue siendo la misma sustancia.",
    "pending_question_turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
    "pending_question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
    "claim_followup": {
      "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
      "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
      "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "badb6187-33a5-4ec4-bc14-3c256dbe459c"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "7ab6a667-1dc3-43b9-905a-98b86944a9fe"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "08509f63-d257-4991-bf19-5dc512eed26c",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "help",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 1,
    "stalled_signature": "25985febfa379bed34f269e65b37a27a3a9d92f241935d0cb57506c9471a3d3c",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "034eba87-8fa1-4a18-9f56-4dbcdc48500d",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "3ff92116-4126-44ec-a7d8-bb26f43cb4c6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
    "text": "¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?",
    "strategy_role": 2
  }
}
```


### Paso 5

Participante ficticio: ¿De dónde procede esa pregunta?

Respuesta íntegra:

La procedencia vigente es agua preguntas, sección Evaporación. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa pregunta?",
  "http_status": 200,
  "response": {
    "turn_id": "a3b29897-40af-421e-9e05-59cbede18807",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "La procedencia vigente es agua preguntas, sección Evaporación. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 15,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
        "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
        "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "badb6187-33a5-4ec4-bc14-3c256dbe459c"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "approved",
      "latency_ms": 295,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Ahora hablo del estado: el agua sigue siendo la misma sustancia.",
    "pending_question_turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
    "pending_question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
    "claim_followup": {
      "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
      "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
      "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "badb6187-33a5-4ec4-bc14-3c256dbe459c"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "7ab6a667-1dc3-43b9-905a-98b86944a9fe"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "08509f63-d257-4991-bf19-5dc512eed26c",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 1,
    "stalled_signature": "f0cc3843fd95072d920744d42bbd0a74e7ef42cdb62a685b6a41b13a8cee0b11",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "67513d38-8617-4e8d-99d2-99626d5a3e63",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "3ff92116-4126-44ec-a7d8-bb26f43cb4c6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: Terminar la sesión sin guardar esta conversación.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Terminar la sesión sin guardar esta conversación.",
  "http_status": 200,
  "response": {
    "turn_id": "93b85f43-9f8f-4208-8291-7bfab6d36f94",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
        "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
        "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "badb6187-33a5-4ec4-bc14-3c256dbe459c"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
        "text": "¿Cómo explicarías que una tela se seque sin que el agua hierva?"
      },
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 281,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Ahora hablo del estado: el agua sigue siendo la misma sustancia.",
    "pending_question_turn_id": "88cb20c7-13dc-43fa-8046-89ba3eb7a2f9",
    "pending_question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
    "claim_followup": {
      "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
      "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
      "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
      "subgoal_ref": "evaporacion",
      "source_fragment_ids": [
        "badb6187-33a5-4ec4-bc14-3c256dbe459c"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "7ab6a667-1dc3-43b9-905a-98b86944a9fe"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "08509f63-d257-4991-bf19-5dc512eed26c",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 1,
    "stalled_signature": "37a0377c7bd9ab6177bc0683cacae37d845ffc2984a95009b484c3c5adfcaf76",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "0d782d0a-cdc6-48bb-a31d-879b267a2f1d",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "3ff92116-4126-44ec-a7d8-bb26f43cb4c6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Confirmo finalizar sin conservarlos.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Confirmo finalizar sin conservarlos.",
  "http_status": 200,
  "response": {
    "turn_id": "dbc34de5-fc22-4fce-ad70-3b323c298de6",
    "dialogue_action": "finish",
    "dialogue_purpose": null,
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": {
      "turn_count": 7,
      "duration_seconds": 1,
      "questions_asked": [
        "Hola. ¿Cómo explicarías que una tela se seque sin que el agua hierva?",
        "¿Estás explicando un cambio de estado o una transformación de la sustancia? ¿Qué distingue ambas ideas en tu razonamiento?",
        "¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?"
      ],
      "topics_covered": [
        "evaporacion"
      ],
      "concepts_mentioned": [
        "evaporacion"
      ],
      "sources_consulted_fragment_ids": [
        "0e6a660e-dc25-41e4-be33-a7928ebf2f65",
        "370b7609-b6de-4572-bc80-28facb2773af",
        "badb6187-33a5-4ec4-bc14-3c256dbe459c"
      ],
      "clarifications_count": 0,
      "incidents": [],
      "close_reason": "closed_voluntary"
    },
    "session_status": "closed_voluntary",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "06474425-2ef5-469e-bc0c-0a55278a5489",
        "question_unit_id": "dc6f90f4-2b77-4dd0-934e-7c9006846d8a",
        "followup_unit_id": "7ca9e50e-a280-41d0-b6c2-07a260ea42b1",
        "subgoal_ref": "evaporacion",
        "source_fragment_ids": [
          "badb6187-33a5-4ec4-bc14-3c256dbe459c"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 280,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {},
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "e6c9803f-eabc-4ad9-b64a-0409dc4580b8",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "3ff92116-4126-44ec-a7d8-bb26f43cb4c6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 8: reserved-v4-third-first/reserved_third-agua-docx-self_study

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Buenas tardes, ¿por qué sale agua de una tela mojada al aire?

Respuesta íntegra:

Hola. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Buenas tardes, ¿por qué sale agua de una tela mojada al aire?",
  "http_status": 200,
  "response": {
    "turn_id": "81198b39-6e0c-4567-8d01-f2b2bfbb0f38",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Hola. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "81ea13b5-72d3-475b-b764-cff616338976",
        "document_version": 1,
        "location_ref": "párrafo 6 (Evaporación)",
        "fragment_text": "Por qué. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "8ad3b834-0bc1-40af-8f05-ed060128ad3e"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 202,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "Buenas tardes, ¿por qué sale agua de una tela mojada al aire?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "8ad3b834-0bc1-40af-8f05-ed060128ad3e"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "81198b39-6e0c-4567-8d01-f2b2bfbb0f38",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "db22320917b14fa912329ef62d398c507917db9dfe273d8b5dbc96bd925d493a",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "d6afa8f5-52cf-4c89-bd6d-22b5abdd0d23",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "559de92f-cb3b-4235-adb9-e907e3b1bb08",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: ¿Eso implica que se separan el hidrógeno y el oxígeno?

Respuesta íntegra:

La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Eso implica que se separan el hidrógeno y el oxígeno?",
  "http_status": 200,
  "response": {
    "turn_id": "7918bf9b-fd6b-4af5-941a-d234307b8126",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
    "state_version": 6,
    "sources": [
      {
        "document_id": "81ea13b5-72d3-475b-b764-cff616338976",
        "document_version": 1,
        "location_ref": "párrafo 6 (Evaporación)",
        "fragment_text": "Por qué. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "cc280edc-a776-48e1-a9e9-9a07d847759a"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "¿Eso implica que se separan el hidrógeno y el oxígeno?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "cc280edc-a776-48e1-a9e9-9a07d847759a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "7918bf9b-fd6b-4af5-941a-d234307b8126",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "083fb6cd7b1e78051fe367c1788d8a4655b94d84c814d201093d50216ec6af2b",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "53ef7d39-4b7e-4613-ba82-8967f7117360",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "559de92f-cb3b-4235-adb9-e907e3b1bb08",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 3

Participante ficticio: Sigo sin verlo; dame otra forma de explicarlo.

Respuesta íntegra:

Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Sigo sin verlo; dame otra forma de explicarlo.",
  "http_status": 200,
  "response": {
    "turn_id": "2523d827-dfd8-4901-9249-ddf5a2430951",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.",
    "state_version": 9,
    "sources": [
      {
        "document_id": "81ea13b5-72d3-475b-b764-cff616338976",
        "document_version": 1,
        "location_ref": "párrafo 8 (Evaporación)",
        "fragment_text": "Otra explicación. Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "rephrase",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "b6bf0106-2e4b-4c55-a697-47e88314f71d"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "¿Eso implica que se separan el hidrógeno y el oxígeno?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "b6bf0106-2e4b-4c55-a697-47e88314f71d"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "2523d827-dfd8-4901-9249-ddf5a2430951",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "rephrase",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 1,
    "stalled_signature": "45db9614f578698c0db01e557e773edbdea41ad786d30b7321d79a5efca0c859",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "6225dbcc-c933-46de-81d7-e734a2c42e1c",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "559de92f-cb3b-4235-adb9-e907e3b1bb08",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 4

Participante ficticio: ¿Cómo sucede ese cambio paso a paso?

Respuesta íntegra:

Primero, sitúa una superficie de agua en contacto con el aire. Después, algunas moléculas salen del líquido y pasan al gas; otras pueden volver. Si salen más de las que regresan, disminuye el líquido. El proceso necesita energía, que puede proceder del agua y del entorno. Por eso un objeto mojado puede enfriarse mientras se seca.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Cómo sucede ese cambio paso a paso?",
  "http_status": 200,
  "response": {
    "turn_id": "46de0ffc-93ff-4973-9f1c-4d8be264cd7d",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Primero, sitúa una superficie de agua en contacto con el aire. Después, algunas moléculas salen del líquido y pasan al gas; otras pueden volver. Si salen más de las que regresan, disminuye el líquido. El proceso necesita energía, que puede proceder del agua y del entorno. Por eso un objeto mojado puede enfriarse mientras se seca.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "81ea13b5-72d3-475b-b764-cff616338976",
        "document_version": 1,
        "location_ref": "párrafo 7 (Evaporación)",
        "fragment_text": "Cómo sucede. Primero, sitúa una superficie de agua en contacto con el aire. Después, algunas moléculas salen del líquido y pasan al gas; otras pueden volver. Si salen más de las que regresan, disminuye el líquido. El proceso necesita energía, que puede proceder del agua y del entorno. Por eso un objeto mojado puede enfriarse mientras se seca.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "7a039eff-851e-4473-9eb3-6d6254462661"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "¿Cómo sucede ese cambio paso a paso?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "7a039eff-851e-4473-9eb3-6d6254462661"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "46de0ffc-93ff-4973-9f1c-4d8be264cd7d",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "5d58b2550773b3b1c360c1cd039c619092c5543bd1109ab05cf1189f1f8341a5",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "34f1552b-b3e4-4d53-ba1f-a58b5308b95a",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "559de92f-cb3b-4235-adb9-e907e3b1bb08",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 5

Participante ficticio: ¿Puede producirse vapor sin hervir?

Respuesta íntegra:

Sí, el agua líquida puede pasar a vapor sin hervir mediante evaporación. También puede producir vapor por ebullición bajo las condiciones adecuadas. Que un ejemplo muestre una vía no excluye la otra.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Puede producirse vapor sin hervir?",
  "http_status": 200,
  "response": {
    "turn_id": "82662924-4be3-4d6e-905f-027e2a68de9e",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Sí, el agua líquida puede pasar a vapor sin hervir mediante evaporación. También puede producir vapor por ebullición bajo las condiciones adecuadas. Que un ejemplo muestre una vía no excluye la otra.",
    "state_version": 15,
    "sources": [
      {
        "document_id": "81ea13b5-72d3-475b-b764-cff616338976",
        "document_version": 1,
        "location_ref": "párrafo 9 (Evaporación)",
        "fragment_text": "Qué es posible. Sí, el agua líquida puede pasar a vapor sin hervir mediante evaporación. También puede producir vapor por ebullición bajo las condiciones adecuadas. Que un ejemplo muestre una vía no excluye la otra.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "c6f83db6-7ef8-444a-b5f9-3be7b13a0440"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 156,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "¿Puede producirse vapor sin hervir?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "c6f83db6-7ef8-444a-b5f9-3be7b13a0440"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "82662924-4be3-4d6e-905f-027e2a68de9e",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "c1645282cc0d253c2da9119c28e33b25691306d9bf744b08aaa72ddcb9c39a24",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "509f5fef-0468-417e-8b7b-8bee28818781",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "559de92f-cb3b-4235-adb9-e907e3b1bb08",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: ¿De dónde procede esa explicación?

Respuesta íntegra:

La procedencia vigente es 01 agua dossier, sección párrafo 9 (Evaporación). Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa explicación?",
  "http_status": 200,
  "response": {
    "turn_id": "c00f211d-5c72-4236-be2c-6352b9870bf0",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La procedencia vigente es 01 agua dossier, sección párrafo 9 (Evaporación). Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 375,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "¿Puede producirse vapor sin hervir?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "c6f83db6-7ef8-444a-b5f9-3be7b13a0440"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "82662924-4be3-4d6e-905f-027e2a68de9e",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "913e2752312dcb976bf735ce40f4e264568a248a6ce0143d889a5c8bf0bfebec",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "864d42a0-bd98-4e1e-a818-5e8994ab2769",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "559de92f-cb3b-4235-adb9-e907e3b1bb08",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Terminar la sesión sin guardar esta conversación.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Terminar la sesión sin guardar esta conversación.",
  "http_status": 200,
  "response": {
    "turn_id": "44decb65-2a4f-4b7d-973d-965b5c9821e6",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 375,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "evaporacion",
    "content_query": "¿Puede producirse vapor sin hervir?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "c6f83db6-7ef8-444a-b5f9-3be7b13a0440"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "82662924-4be3-4d6e-905f-027e2a68de9e",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "evaporacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "evaporacion",
    "relevant_concepts": [
      "evaporacion"
    ],
    "support_step": 0,
    "stalled_signature": "37a0377c7bd9ab6177bc0683cacae37d845ffc2984a95009b484c3c5adfcaf76",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "460585d3-e533-4011-8cfc-6887028f690a",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "559de92f-cb3b-4235-adb9-e907e3b1bb08",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 8

Participante ficticio: Confirmo finalizar sin conservarlos.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Confirmo finalizar sin conservarlos.",
  "http_status": 200,
  "response": {
    "turn_id": "9b6278ea-6642-468d-b56d-6fe1926cd4b9",
    "mode": "doubt_resolution",
    "dialogue_action": "finish",
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 24,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 375,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    },
    "session_closed": true,
    "session_status": "closed_voluntary",
    "study_summary": {
      "turn_count": 8,
      "duration_seconds": 2,
      "modes_used": [
        "doubt_resolution"
      ],
      "concepts_addressed": [
        "evaporacion"
      ],
      "practice_questions_count": 0,
      "practice_question_types": [],
      "sources_consulted_fragment_ids": [
        "53c569d8-832c-4966-a486-ccca8d87bb9c",
        "6404826c-ef08-4415-ac4e-529d385de231",
        "edaca198-32f8-49a8-8d75-313de73b98c3",
        "fc78b8ab-d508-4ee7-b42a-1f0807a0b0b5"
      ],
      "incidents": []
    }
  },
  "context": null,
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "71f13d96-a9da-4876-a934-b6e96ae8fb5e",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "559de92f-cb3b-4235-adb9-e907e3b1bb08",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 9: reserved-v4-third-first/reserved_third-datos-pdf-oral_defense

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Buenas tardes, quiero empezar con una pregunta de defensa.

Respuesta íntegra:

Hola. ¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Buenas tardes, quiero empezar con una pregunta de defensa.",
  "http_status": 200,
  "response": {
    "turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "Hola. ¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?",
    "state_version": 3,
    "sources": [
      {
        "document_id": "3e2bc6b7-5f11-4ab2-8aa4-d9c57f80d617",
        "document_version": 1,
        "location_ref": "Media aritmética",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "greeting",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": {
        "turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [
        "836433d1-2479-411a-b01f-89f4cfcf6afd"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 187,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Buenas tardes, quiero empezar con una pregunta de defensa.",
    "pending_question_turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
    "pending_question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
    "claim_followup": null,
    "last_approved_unit_ids": [
      "836433d1-2479-411a-b01f-89f4cfcf6afd"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "greeting",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "d32ed0483f4bc5451c2e1c8811a6d49d77ba49370bf512b018d8d7dbe2a152b4",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "d50bd185-ee04-4b14-9307-c2af83054f86",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "955861e8-7bc5-4a3d-86e6-035668ccf75b",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: Mi propuesta cuenta también el intento que no tiene una duración.

Respuesta íntegra:

¿Cómo distingues los intentos realizados de las observaciones disponibles al justificar el divisor?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Mi propuesta cuenta también el intento que no tiene una duración.",
  "http_status": 200,
  "response": {
    "turn_id": "036953d3-ff18-44a4-abe8-1597cfc27ff0",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Cómo distingues los intentos realizados de las observaciones disponibles al justificar el divisor?",
    "state_version": 6,
    "sources": [
      {
        "document_id": "55854de1-196e-4afc-9556-a2263f9bccf0",
        "document_version": 1,
        "location_ref": "Seguimiento de media, 1",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "036953d3-ff18-44a4-abe8-1597cfc27ff0",
        "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
        "followup_unit_id": "d0cedb59-5dd9-458f-a377-e2e04d3b92d0",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "b4b741e8-9123-4afc-832a-754713c8924d"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [
        "d0cedb59-5dd9-458f-a377-e2e04d3b92d0"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Mi propuesta cuenta también el intento que no tiene una duración.",
    "pending_question_turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
    "pending_question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
    "claim_followup": {
      "participant_turn_id": "036953d3-ff18-44a4-abe8-1597cfc27ff0",
      "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
      "followup_unit_id": "d0cedb59-5dd9-458f-a377-e2e04d3b92d0",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "b4b741e8-9123-4afc-832a-754713c8924d"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "d0cedb59-5dd9-458f-a377-e2e04d3b92d0"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "036953d3-ff18-44a4-abe8-1597cfc27ff0",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "84724f947d7dcadcab3f411851a3e7a891c0784335dbd6b4c2fc57ec39561f4d",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "478fd193-1aee-405c-9813-b40d7ac89caa",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "955861e8-7bc5-4a3d-86e6-035668ccf75b",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
    "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?",
    "strategy_role": 0
  }
}
```


### Paso 3

Participante ficticio: Quería distinguir los intentos de las cinco medidas disponibles.

Respuesta íntegra:

¿Qué representa el total y qué representa cada término del reparto que propones?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Quería distinguir los intentos de las cinco medidas disponibles.",
  "http_status": 200,
  "response": {
    "turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Qué representa el total y qué representa cada término del reparto que propones?",
    "state_version": 9,
    "sources": [
      {
        "document_id": "55854de1-196e-4afc-9556-a2263f9bccf0",
        "document_version": 1,
        "location_ref": "Seguimiento de media, 2",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
        "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
        "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "c9378085-67f1-4357-8ec0-74322fd80123"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [
        "b44176d9-8e73-441a-98bd-5a3382b2c71a"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Quería distinguir los intentos de las cinco medidas disponibles.",
    "pending_question_turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
    "pending_question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
    "claim_followup": {
      "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
      "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
      "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "c9378085-67f1-4357-8ec0-74322fd80123"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "b44176d9-8e73-441a-98bd-5a3382b2c71a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "8122286ca3d404fe7d72b975dbdd99d0137f1d97069a01e65fb9bd49853fb0b8",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "904f7706-bab1-4413-b306-d3740e748be1",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "955861e8-7bc5-4a3d-86e6-035668ccf75b",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "d0cedb59-5dd9-458f-a377-e2e04d3b92d0",
    "text": "¿Cómo distingues los intentos realizados de las observaciones disponibles al justificar el divisor?",
    "strategy_role": 1
  }
}
```


### Paso 4

Participante ficticio: Dame una pista para organizar la justificación.

Respuesta íntegra:

Comprueba la unidad de los valores.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Dame una pista para organizar la justificación.",
  "http_status": 200,
  "response": {
    "turn_id": "cd678e4f-574e-4f59-8a1c-84fdd6c3d8fa",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "Comprueba la unidad de los valores.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "3e2bc6b7-5f11-4ab2-8aa4-d9c57f80d617",
        "document_version": 1,
        "location_ref": "Media aritmética",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "help",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
        "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
        "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "c9378085-67f1-4357-8ec0-74322fd80123"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [
        "cb3e0953-586e-45f8-80b5-a88124896c8a"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 186,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Quería distinguir los intentos de las cinco medidas disponibles.",
    "pending_question_turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
    "pending_question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
    "claim_followup": {
      "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
      "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
      "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "c9378085-67f1-4357-8ec0-74322fd80123"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "cb3e0953-586e-45f8-80b5-a88124896c8a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "cd678e4f-574e-4f59-8a1c-84fdd6c3d8fa",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "help",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 1,
    "stalled_signature": "f9b87931916f82db25ce433fb6e113786e1e197c51631910a982b6f89d25a27e",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "11e7299f-a9e1-43ee-8abd-d9605620489f",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "955861e8-7bc5-4a3d-86e6-035668ccf75b",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
    "text": "¿Qué representa el total y qué representa cada término del reparto que propones?",
    "strategy_role": 2
  }
}
```


### Paso 5

Participante ficticio: ¿De dónde procede esa pregunta?

Respuesta íntegra:

La procedencia vigente es datos preguntas, sección Media aritmética. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa pregunta?",
  "http_status": 200,
  "response": {
    "turn_id": "234e412b-88bf-4fd2-9892-93401803ef79",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "La procedencia vigente es datos preguntas, sección Media aritmética. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 15,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
        "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
        "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "c9378085-67f1-4357-8ec0-74322fd80123"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "approved",
      "latency_ms": 297,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Quería distinguir los intentos de las cinco medidas disponibles.",
    "pending_question_turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
    "pending_question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
    "claim_followup": {
      "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
      "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
      "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "c9378085-67f1-4357-8ec0-74322fd80123"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "cb3e0953-586e-45f8-80b5-a88124896c8a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "cd678e4f-574e-4f59-8a1c-84fdd6c3d8fa",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 1,
    "stalled_signature": "00881b3f61f441af0eaf425b5432e1bd349424d592fcc0582fdeca8d0384f4a5",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "7211a295-cf31-4e24-8293-f3758cd4ebc2",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "955861e8-7bc5-4a3d-86e6-035668ccf75b",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: Terminar la sesión sin guardar esta conversación.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Terminar la sesión sin guardar esta conversación.",
  "http_status": 200,
  "response": {
    "turn_id": "11878a38-da17-4269-b562-dc83bbe4faf5",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
        "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
        "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "c9378085-67f1-4357-8ec0-74322fd80123"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
        "text": "¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?"
      },
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 280,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Quería distinguir los intentos de las cinco medidas disponibles.",
    "pending_question_turn_id": "c95c3a1f-5feb-4e35-80d6-6d7dcbeb159d",
    "pending_question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
    "claim_followup": {
      "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
      "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
      "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
      "subgoal_ref": "media",
      "source_fragment_ids": [
        "c9378085-67f1-4357-8ec0-74322fd80123"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "cb3e0953-586e-45f8-80b5-a88124896c8a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "cd678e4f-574e-4f59-8a1c-84fdd6c3d8fa",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 1,
    "stalled_signature": "8aed3cbd490ee7f606966c87b8fc7847dbf180903a89dc814389a6484b794c67",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "acd892dd-48e8-425d-b005-5459a24fd3f6",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "955861e8-7bc5-4a3d-86e6-035668ccf75b",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Confirmo finalizar sin conservarlos.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Confirmo finalizar sin conservarlos.",
  "http_status": 200,
  "response": {
    "turn_id": "eb67f747-23db-41e0-a733-aa47098cff82",
    "dialogue_action": "finish",
    "dialogue_purpose": null,
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": {
      "turn_count": 7,
      "duration_seconds": 1,
      "questions_asked": [
        "Hola. ¿Cómo explicarías el cálculo de la media de la serie A sin limitarte a decir seis?",
        "¿Cómo distingues los intentos realizados de las observaciones disponibles al justificar el divisor?",
        "¿Qué representa el total y qué representa cada término del reparto que propones?"
      ],
      "topics_covered": [
        "media"
      ],
      "concepts_mentioned": [
        "media"
      ],
      "sources_consulted_fragment_ids": [
        "210c10b2-e60a-41f8-b9d0-01d500b9acaf",
        "b4b741e8-9123-4afc-832a-754713c8924d",
        "c9378085-67f1-4357-8ec0-74322fd80123"
      ],
      "clarifications_count": 0,
      "incidents": [],
      "close_reason": "closed_voluntary"
    },
    "session_status": "closed_voluntary",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "68c15492-aa4e-46d3-aafb-303e0680a296",
        "question_unit_id": "836433d1-2479-411a-b01f-89f4cfcf6afd",
        "followup_unit_id": "b44176d9-8e73-441a-98bd-5a3382b2c71a",
        "subgoal_ref": "media",
        "source_fragment_ids": [
          "c9378085-67f1-4357-8ec0-74322fd80123"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 297,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {},
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "596a7b0b-d977-4002-92ab-15255c402aef",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "955861e8-7bc5-4a3d-86e6-035668ccf75b",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 10: reserved-v4-third-first/reserved_third-datos-pdf-self_study

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Buenas tardes, lee los valores de la serie A.

Respuesta íntegra:

Hola. En esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos, tres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el número de observaciones válidas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Buenas tardes, lee los valores de la serie A.",
  "http_status": 200,
  "response": {
    "turn_id": "51a3c6ad-3d3e-4763-a9bf-c8ac94b08e7c",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Hola. En esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos, tres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el número de observaciones válidas.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "fbc0af04-d73e-4fc3-af89-caf7ba83144e",
        "document_version": 1,
        "location_ref": "página 2",
        "fragment_text": "Media aritmética\nEn esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos,\ntres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el\nnúmero de observaciones válidas. Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres,\ncuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta\nentre cinco: la media es seis segundos. Al dividir la suma entre el número de datos, se obtiene un reparto uniforme del total. Un valor\ngrande puede aumentar la media aunque la mayoría de las observaciones sean pequeñas. La suma expresa tiempo acumulado; la media expresa el total por observación. Confundirlas\ncambia tanto el número como la interpretación.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "b446ad40-3666-439c-9953-1ffed17758e6"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 187,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "Buenas tardes, lee los valores de la serie A.",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "b446ad40-3666-439c-9953-1ffed17758e6"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "51a3c6ad-3d3e-4763-a9bf-c8ac94b08e7c",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "d24a6fe972546a415a098177dd8bc3b92ffdb97f9b3d4d21f4c03417a2d16898",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "99a3e822-8792-4925-8da3-701e9c592708",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "416572d4-c772-4c92-9846-10a1dcad1c4d",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: ¿Para calcular la media dividimos treinta entre seis intentos?

Respuesta íntegra:

En esta práctica hay seis intentos y cinco duraciones medidas. El intento sin medida no aporta un cero ni otra duración conocida. El divisor de la media cuenta observaciones válidas, no intentos: en la serie A se divide el total de treinta segundos entre cinco valores medidos.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Para calcular la media dividimos treinta entre seis intentos?",
  "http_status": 200,
  "response": {
    "turn_id": "7bb159f1-8128-40b3-b9b5-8e4f77282345",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "En esta práctica hay seis intentos y cinco duraciones medidas. El intento sin medida no aporta un cero ni otra duración conocida. El divisor de la media cuenta observaciones válidas, no intentos: en la serie A se divide el total de treinta segundos entre cinco valores medidos.",
    "state_version": 6,
    "sources": [
      {
        "document_id": "bd87df84-17dd-4072-8e26-f5870ad91201",
        "document_version": 1,
        "location_ref": "Continuidad media, causal-count",
        "fragment_text": "En esta práctica hay seis intentos y cinco duraciones medidas. El intento sin medida no aporta un cero ni otra duración conocida. El divisor de la media cuenta observaciones válidas, no intentos: en la serie A se divide el total de treinta segundos entre cinco valores medidos.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "cced457d-62fd-442a-88a2-791d13ba7d4e"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 156,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "¿Para calcular la media dividimos treinta entre seis intentos?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "cced457d-62fd-442a-88a2-791d13ba7d4e"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "7bb159f1-8128-40b3-b9b5-8e4f77282345",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "72ceaac869452d5224c022460c10d497d29c2c73b392d1334ef79785dfce29b8",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "939220fa-deef-4251-91d7-4769b758e974",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "416572d4-c772-4c92-9846-10a1dcad1c4d",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 3

Participante ficticio: ¿Qué pasa con el intento sin una duración?

Respuesta íntegra:

El divisor usa cinco observaciones válidas de la serie A. El sexto intento sigue sin una duración conocida y queda fuera del reparto. El número de intentos y el número de medidas disponibles son conceptos distintos.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Qué pasa con el intento sin una duración?",
  "http_status": 200,
  "response": {
    "turn_id": "450a59ec-b521-47fe-9169-47366d6d0dee",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "El divisor usa cinco observaciones válidas de la serie A. El sexto intento sigue sin una duración conocida y queda fuera del reparto. El número de intentos y el número de medidas disponibles son conceptos distintos.",
    "state_version": 9,
    "sources": [
      {
        "document_id": "bd87df84-17dd-4072-8e26-f5870ad91201",
        "document_version": 1,
        "location_ref": "Continuidad media, count-fact",
        "fragment_text": "El divisor usa cinco observaciones válidas de la serie A. El sexto intento sigue sin una duración conocida y queda fuera del reparto. El número de intentos y el número de medidas disponibles son conceptos distintos.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "5d601d83-3a46-4da9-afbd-086037163560"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "¿Qué pasa con el intento sin una duración?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "5d601d83-3a46-4da9-afbd-086037163560"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "450a59ec-b521-47fe-9169-47366d6d0dee",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "5e5b20bc1ad2514f92e43cce036a8845ad78a0d53abe4fe64a29ce636f910e14",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "dbc9c009-80c9-4091-9b3e-203412e4dbc3",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "416572d4-c772-4c92-9846-10a1dcad1c4d",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 4

Participante ficticio: ¿Cómo se calcula la media paso a paso?

Respuesta íntegra:

Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres, cuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta entre cinco: la media es seis segundos.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Cómo se calcula la media paso a paso?",
  "http_status": 200,
  "response": {
    "turn_id": "5b86c613-19ae-4e68-8b39-88cb83b257e9",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres, cuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta entre cinco: la media es seis segundos.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "fbc0af04-d73e-4fc3-af89-caf7ba83144e",
        "document_version": 1,
        "location_ref": "página 2",
        "fragment_text": "Media aritmética\nEn esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos,\ntres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el\nnúmero de observaciones válidas. Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres,\ncuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta\nentre cinco: la media es seis segundos. Al dividir la suma entre el número de datos, se obtiene un reparto uniforme del total. Un valor\ngrande puede aumentar la media aunque la mayoría de las observaciones sean pequeñas. La suma expresa tiempo acumulado; la media expresa el total por observación. Confundirlas\ncambia tanto el número como la interpretación.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "8561bc14-b9f2-4761-9275-b8bb721d3651"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "media",
    "content_query": "¿Cómo se calcula la media paso a paso?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "8561bc14-b9f2-4761-9275-b8bb721d3651"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "5b86c613-19ae-4e68-8b39-88cb83b257e9",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "media"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "media",
    "relevant_concepts": [
      "media"
    ],
    "support_step": 0,
    "stalled_signature": "00e355458a073fad3b8ab6d0471c569c1247c27c7594d2aceebb16463bc71256",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "a36ca979-0425-45eb-a750-4c865f27a581",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "416572d4-c772-4c92-9846-10a1dcad1c4d",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 5

Participante ficticio: ¿Qué significa mediana?

Respuesta íntegra:

La mediana es el centro de los valores ordenados. Para la serie A ordenada, dos, tres, tres, cuatro y dieciocho, la posición central es la tercera y la mediana es tres segundos.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Qué significa mediana?",
  "http_status": 200,
  "response": {
    "turn_id": "a477451b-77a2-4f6f-a60c-4cb9a78b4a9b",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La mediana es el centro de los valores ordenados. Para la serie A ordenada, dos, tres, tres, cuatro y dieciocho, la posición central es la tercera y la mediana es tres segundos.",
    "state_version": 15,
    "sources": [
      {
        "document_id": "fbc0af04-d73e-4fc3-af89-caf7ba83144e",
        "document_version": 1,
        "location_ref": "página 3",
        "fragment_text": "Mediana y posición\nLa mediana es el centro de los valores ordenados. Para la serie A ordenada, dos, tres, tres, cuatro y\ndieciocho, la posición central es la tercera y la mediana es tres segundos. Primero, ordena las cinco duraciones de menor a mayor. Después, identifica la tercera, porque\nquedan dos a cada lado. Esa duración es tres segundos. Si hubiera un número par de valores, se\nusaría la media de los dos centrales. La mediana se basa en posiciones del orden, por lo que un valor extremo puede cambiar mucho sin\ndesplazar el valor central en este ejemplo. La media usa la magnitud de todos los valores; la mediana identifica el centro del orden. En la serie\nA la duración dieciocho separa ambas descripciones. En una cantidad par de datos se necesita una media de dos posiciones centrales.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "69740ccf-ab58-40d9-82a1-b9ead1ca593d"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "mediana",
    "content_query": "¿Qué significa mediana?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "69740ccf-ab58-40d9-82a1-b9ead1ca593d"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "a477451b-77a2-4f6f-a60c-4cb9a78b4a9b",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "mediana"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "mediana",
    "relevant_concepts": [
      "mediana"
    ],
    "support_step": 0,
    "stalled_signature": "f07e8824305fe0908cd672c165f6a822265620400890c39fe3257243cd94e884",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "2d3ee967-2fa8-42f1-807f-0d59d751d230",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "416572d4-c772-4c92-9846-10a1dcad1c4d",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: ¿De dónde procede esa explicación?

Respuesta íntegra:

La procedencia vigente es 04 datos practica, sección página 3. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa explicación?",
  "http_status": 200,
  "response": {
    "turn_id": "4da4a23b-9f00-4fd3-b2bc-96ff7b92ef5b",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La procedencia vigente es 04 datos practica, sección página 3. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 390,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "mediana",
    "content_query": "¿Qué significa mediana?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "69740ccf-ab58-40d9-82a1-b9ead1ca593d"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "a477451b-77a2-4f6f-a60c-4cb9a78b4a9b",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "mediana"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "mediana",
    "relevant_concepts": [
      "mediana"
    ],
    "support_step": 0,
    "stalled_signature": "6cd067c8871c3ff86ecb35f4d65648808ac60664240a543c40c7063d07642da6",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "0ca2bd43-c8cd-4345-b5dd-93e6a14e277d",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "416572d4-c772-4c92-9846-10a1dcad1c4d",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Terminar la sesión sin guardar esta conversación.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Terminar la sesión sin guardar esta conversación.",
  "http_status": 200,
  "response": {
    "turn_id": "1a4ba656-01dd-4d0a-8297-aeac3c2c1f1a",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 375,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "mediana",
    "content_query": "¿Qué significa mediana?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "69740ccf-ab58-40d9-82a1-b9ead1ca593d"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "a477451b-77a2-4f6f-a60c-4cb9a78b4a9b",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "mediana"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "mediana",
    "relevant_concepts": [
      "mediana"
    ],
    "support_step": 0,
    "stalled_signature": "fd8f5d95651eed7b203993319379dc18027f3435b4c06367354f0c66651f5489",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "0255f788-c8ce-4634-92b4-45791d3dbfb3",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "416572d4-c772-4c92-9846-10a1dcad1c4d",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 8

Participante ficticio: Confirmo finalizar sin conservarlos.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Confirmo finalizar sin conservarlos.",
  "http_status": 200,
  "response": {
    "turn_id": "b8ea205a-7597-4c93-917e-00ff82223175",
    "mode": "doubt_resolution",
    "dialogue_action": "finish",
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 24,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 391,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    },
    "session_closed": true,
    "session_status": "closed_voluntary",
    "study_summary": {
      "turn_count": 8,
      "duration_seconds": 2,
      "modes_used": [
        "doubt_resolution"
      ],
      "concepts_addressed": [
        "media",
        "mediana"
      ],
      "practice_questions_count": 0,
      "practice_question_types": [],
      "sources_consulted_fragment_ids": [
        "45952a81-17dd-4871-a354-cf3a79de2978",
        "6344fb01-8e38-47a1-9c79-5723f5150f6e",
        "bac58366-2405-41fe-9502-8ea44345cb45",
        "dc8cb9ad-566b-427d-8b4d-aa95e4a92804"
      ],
      "incidents": []
    }
  },
  "context": null,
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "2fc382ab-b31f-476a-93d0-d9d33222d382",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "416572d4-c772-4c92-9846-10a1dcad1c4d",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 11: reserved-v4-third-first/reserved_third-programa-docx-oral_defense

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Buenas tardes, quiero empezar con una pregunta de defensa.

Respuesta íntegra:

Hola. ¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Buenas tardes, quiero empezar con una pregunta de defensa.",
  "http_status": 200,
  "response": {
    "turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "Hola. ¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?",
    "state_version": 3,
    "sources": [
      {
        "document_id": "1f6fb858-d752-421b-b783-41b4958ed2b6",
        "document_version": 1,
        "location_ref": "Reglas de validación",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "greeting",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": {
        "turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [
        "2b819c2f-1cef-407c-a330-77eca0aa6ef2"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Buenas tardes, quiero empezar con una pregunta de defensa.",
    "pending_question_turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
    "pending_question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
    "claim_followup": null,
    "last_approved_unit_ids": [
      "2b819c2f-1cef-407c-a330-77eca0aa6ef2"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "greeting",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "a58dd480e5277a4233bb99239361560c92c5e4768a38244683a0087fce9e1039",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "b812a5f4-27c7-4f82-8a33-c3bdd76b0bc1",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "a87b6027-2b1a-4430-8e12-052b167d3865",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: Pienso que basta con convertir el texto para pedir que se guarde.

Respuesta íntegra:

¿Cómo distingues comprobar el formato de comprobar la regla del caso al justificar tu respuesta?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Pienso que basta con convertir el texto para pedir que se guarde.",
  "http_status": 200,
  "response": {
    "turn_id": "b6f1ea92-f82a-4456-896b-22410bbf3da6",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Cómo distingues comprobar el formato de comprobar la regla del caso al justificar tu respuesta?",
    "state_version": 6,
    "sources": [
      {
        "document_id": "2783ce96-1d00-4d7e-9a02-643d1973981a",
        "document_version": 1,
        "location_ref": "Seguimiento de validacion, 1",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "b6f1ea92-f82a-4456-896b-22410bbf3da6",
        "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
        "followup_unit_id": "271e21cb-8623-4f96-b329-bf0e65d0dcb6",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "516f2ca4-75ef-4879-8a7d-cdd39e238bbb"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [
        "271e21cb-8623-4f96-b329-bf0e65d0dcb6"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 155,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Pienso que basta con convertir el texto para pedir que se guarde.",
    "pending_question_turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
    "pending_question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
    "claim_followup": {
      "participant_turn_id": "b6f1ea92-f82a-4456-896b-22410bbf3da6",
      "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
      "followup_unit_id": "271e21cb-8623-4f96-b329-bf0e65d0dcb6",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "516f2ca4-75ef-4879-8a7d-cdd39e238bbb"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "271e21cb-8623-4f96-b329-bf0e65d0dcb6"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "b6f1ea92-f82a-4456-896b-22410bbf3da6",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "db2399f8a1da215b0fa7e2217a84b752a8594a0436fcfad4e25b633e4c7e8ba4",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "1ad54000-d4ff-433b-8f15-53081ce3b389",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "a87b6027-2b1a-4430-8e12-052b167d3865",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
    "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?",
    "strategy_role": 0
  }
}
```


### Paso 3

Participante ficticio: Mi rectificación distingue el formato de la condición del rango.

Respuesta íntegra:

¿Qué condición necesita cumplirse antes de solicitar la siguiente operación, y cómo la justificarías?

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Mi rectificación distingue el formato de la condición del rango.",
  "http_status": 200,
  "response": {
    "turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
    "dialogue_action": "ask",
    "dialogue_purpose": "deepen_current_topic",
    "output_text": "¿Qué condición necesita cumplirse antes de solicitar la siguiente operación, y cómo la justificarías?",
    "state_version": 9,
    "sources": [
      {
        "document_id": "2783ce96-1d00-4d7e-9a02-643d1973981a",
        "document_version": 1,
        "location_ref": "Seguimiento de validacion, 2",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_answer",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
        "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
        "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [
        "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Mi rectificación distingue el formato de la condición del rango.",
    "pending_question_turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
    "pending_question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
    "claim_followup": {
      "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
      "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
      "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_answer",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "3e4e041edca6ceaa2533e1ad71b3f9b351d1a5717ae20cdc0c2f98d7544f75d1",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "fa1287a4-fac5-4e8e-8320-c9a30f39d264",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "a87b6027-2b1a-4430-8e12-052b167d3865",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "271e21cb-8623-4f96-b329-bf0e65d0dcb6",
    "text": "¿Cómo distingues comprobar el formato de comprobar la regla del caso al justificar tu respuesta?",
    "strategy_role": 1
  }
}
```


### Paso 4

Participante ficticio: Dame una pista para organizar la justificación.

Respuesta íntegra:

Recorre las reglas en su orden.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Dame una pista para organizar la justificación.",
  "http_status": 200,
  "response": {
    "turn_id": "9000be01-6a60-48bd-b88e-59a97e2c5895",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "Recorre las reglas en su orden.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "1f6fb858-d752-421b-b783-41b4958ed2b6",
        "document_version": 1,
        "location_ref": "Reglas de validación",
        "fragment_text": "",
        "content_withheld": true
      }
    ],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "help",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
        "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
        "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [
        "3c89ec3d-215a-494e-9df0-af19051da903"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 157,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Mi rectificación distingue el formato de la condición del rango.",
    "pending_question_turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
    "pending_question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
    "claim_followup": {
      "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
      "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
      "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "3c89ec3d-215a-494e-9df0-af19051da903"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "9000be01-6a60-48bd-b88e-59a97e2c5895",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "help",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 1,
    "stalled_signature": "44652e4b13311687a6b4915fa2f7762eb62966b11c13c78355560906ef6b8d01",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "dda340f6-6126-43d9-abe8-dbf407b013e6",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "a87b6027-2b1a-4430-8e12-052b167d3865",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  },
  "response_to_actual_question": {
    "unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
    "text": "¿Qué condición necesita cumplirse antes de solicitar la siguiente operación, y cómo la justificarías?",
    "strategy_role": 2
  }
}
```


### Paso 5

Participante ficticio: ¿De dónde procede esa pregunta?

Respuesta íntegra:

La procedencia vigente es programa preguntas, sección Reglas de validación. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa pregunta?",
  "http_status": 200,
  "response": {
    "turn_id": "e42d35c6-2eb6-49a6-b057-73c9b4a0d800",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "La procedencia vigente es programa preguntas, sección Reglas de validación. Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 15,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
        "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
        "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "approved",
      "latency_ms": 297,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Mi rectificación distingue el formato de la condición del rango.",
    "pending_question_turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
    "pending_question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
    "claim_followup": {
      "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
      "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
      "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "3c89ec3d-215a-494e-9df0-af19051da903"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "9000be01-6a60-48bd-b88e-59a97e2c5895",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 1,
    "stalled_signature": "91eeb78132af6b5ad0f65b795c9318a2f549a01c29521ef478cb7036eecdfb57",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "aaf654a5-9263-4672-8584-483b36bece94",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "a87b6027-2b1a-4430-8e12-052b167d3865",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: Terminar la sesión sin guardar esta conversación.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Terminar la sesión sin guardar esta conversación.",
  "http_status": 200,
  "response": {
    "turn_id": "f96dee8f-068d-4adb-9d1e-6fd0073ca7a1",
    "dialogue_action": "clarify",
    "dialogue_purpose": null,
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": null,
    "session_status": "active",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
        "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
        "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": {
        "turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
        "text": "¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?"
      },
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 282,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Mi rectificación distingue el formato de la condición del rango.",
    "pending_question_turn_id": "7fe9cf64-4d33-45c1-b245-ea3a267df9fa",
    "pending_question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
    "claim_followup": {
      "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
      "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
      "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
      "subgoal_ref": "validacion",
      "source_fragment_ids": [
        "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
      ],
      "assessment": "not_assessed"
    },
    "last_approved_unit_ids": [
      "3c89ec3d-215a-494e-9df0-af19051da903"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "9000be01-6a60-48bd-b88e-59a97e2c5895",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 1,
    "stalled_signature": "8779869651bfd23464920f478b5bc13d3e209a2f86e20e543585b3f782a52355",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "49b1901c-2dfc-4fa7-a7a2-83c38ef2c41a",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "a87b6027-2b1a-4430-8e12-052b167d3865",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Confirmo finalizar sin conservarlos.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Confirmo finalizar sin conservarlos.",
  "http_status": 200,
  "response": {
    "turn_id": "c2996af4-3fdd-427f-8999-abd00b4fbd16",
    "dialogue_action": "finish",
    "dialogue_purpose": null,
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "blocked": false,
    "speech": null,
    "defense_summary": {
      "turn_count": 7,
      "duration_seconds": 1,
      "questions_asked": [
        "Hola. ¿Cómo validarías cero cero siete y mil usando el mismo procedimiento?",
        "¿Cómo distingues comprobar el formato de comprobar la regla del caso al justificar tu respuesta?",
        "¿Qué condición necesita cumplirse antes de solicitar la siguiente operación, y cómo la justificarías?"
      ],
      "topics_covered": [
        "validacion"
      ],
      "concepts_mentioned": [
        "validacion"
      ],
      "sources_consulted_fragment_ids": [
        "516f2ca4-75ef-4879-8a7d-cdd39e238bbb",
        "a317dd50-8de4-41e7-b4ab-5159ea2c37b5",
        "fef42dcc-3945-4f4b-b651-f35e499c0ddc"
      ],
      "clarifications_count": 0,
      "incidents": [],
      "close_reason": "closed_voluntary"
    },
    "session_status": "closed_voluntary",
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": {
        "participant_turn_id": "6be5fb77-b0ce-4bcc-92bc-c276225e1f94",
        "question_unit_id": "2b819c2f-1cef-407c-a330-77eca0aa6ef2",
        "followup_unit_id": "35e2ccf7-d1b3-46a2-9329-626e4e6c0f17",
        "subgoal_ref": "validacion",
        "source_fragment_ids": [
          "a317dd50-8de4-41e7-b4ab-5159ea2c37b5"
        ],
        "assessment": "not_assessed"
      },
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 297,
      "turn_budget_ms": 10000,
      "available_topics": [],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {},
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "0723c268-5d14-4c81-a8c1-8ba91a4a05cb",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "a87b6027-2b1a-4430-8e12-052b167d3865",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 12: reserved-v4-third-first/reserved_third-programa-docx-self_study

Evaluación humana: **pendiente**. Resultado técnico: `passed`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Hola, ¿qué significa validar en este programa?

Respuesta íntegra:

Hola. Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Hola, ¿qué significa validar en este programa?",
  "http_status": 200,
  "response": {
    "turn_id": "773172a3-576c-4554-a32f-9b573a425568",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Hola. Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "17276f30-d237-49c3-9e05-070cf09a8394",
        "document_version": 1,
        "location_ref": "Definición funcional propuesta, revisión humana pendiente",
        "fragment_text": "Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "d2565fc3-f2be-43a5-836e-336a121319c1"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Hola, ¿qué significa validar en este programa?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "d2565fc3-f2be-43a5-836e-336a121319c1"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "773172a3-576c-4554-a32f-9b573a425568",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "2b0053c8d3adde2901ff52bb7ba245b78e87f84e2ebf6da0211a98fe3bc16d87",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "71a3f155-3bd5-4969-bde2-1486df7db5f6",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "c2b48b55-ad2b-43a4-b0fc-79627f880bb6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "greeted-reviewed-response",
      "template_version": 1,
      "template_sha256": "8ab11feba8642faba2105aa9038607c070bb2d0572ff905c197e5c38397fdd71",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 2

Participante ficticio: ¿Para qué comprobar una cantidad antes de pedir guardarla?

Respuesta íntegra:

Validar antes de pedir guardar evita que el programa persista una cantidad que incumple las reglas del caso. Primero se comprueban formato y rango. Solo cuando la validación acepta los datos se solicita guardarlos. Un fallo de escritura es otro problema: una cantidad puede ser válida aunque el archivo no pueda escribirse.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Para qué comprobar una cantidad antes de pedir guardarla?",
  "http_status": 200,
  "response": {
    "turn_id": "e95e3a28-869f-466f-80de-9298a5e6f497",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Validar antes de pedir guardar evita que el programa persista una cantidad que incumple las reglas del caso. Primero se comprueban formato y rango. Solo cuando la validación acepta los datos se solicita guardarlos. Un fallo de escritura es otro problema: una cantidad puede ser válida aunque el archivo no pueda escribirse.",
    "state_version": 6,
    "sources": [
      {
        "document_id": "17276f30-d237-49c3-9e05-070cf09a8394",
        "document_version": 1,
        "location_ref": "Continuidad validacion, causal-order",
        "fragment_text": "Validar antes de pedir guardar evita que el programa persista una cantidad que incumple las reglas del caso. Primero se comprueban formato y rango. Solo cuando la validación acepta los datos se solicita guardarlos. Un fallo de escritura es otro problema: una cantidad puede ser válida aunque el archivo no pueda escribirse.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "1b2f6d53-5ea3-4ac0-b9f7-a2f4bf822d49"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 186,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Para qué comprobar una cantidad antes de pedir guardarla?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "1b2f6d53-5ea3-4ac0-b9f7-a2f4bf822d49"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "e95e3a28-869f-466f-80de-9298a5e6f497",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "23374ab4c3a515c290f130f37a07d18f4b0ede4b3a2e5c58bfb15a35470e0306",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "96ea09a1-3990-4310-8dbd-0aecbdd58ae5",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "c2b48b55-ad2b-43a4-b0fc-79627f880bb6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 3

Participante ficticio: Si introduzco 007, ¿qué se comprueba?

Respuesta íntegra:

Entrada cero cero siete: formato admitido, conversión a siete y rango válido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Si introduzco 007, ¿qué se comprueba?",
  "http_status": 200,
  "response": {
    "turn_id": "9d5f6ce7-4448-445a-b57f-9bcf52a58975",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Entrada cero cero siete: formato admitido, conversión a siete y rango válido.",
    "state_version": 9,
    "sources": [
      {
        "document_id": "fbc6d1db-8bec-4b25-bd86-4cd51a01505d",
        "document_version": 1,
        "location_ref": "párrafo 25 (Reglas de validación)",
        "fragment_text": "Ejemplo 1. Entrada cero cero siete: formato admitido, conversión a siete y rango válido.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "4156f8b4-e3ce-4cf4-931d-7a433724abbb"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "Si introduzco 007, ¿qué se comprueba?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "4156f8b4-e3ce-4cf4-931d-7a433724abbb"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "9d5f6ce7-4448-445a-b57f-9bcf52a58975",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "d71daa50af1511d994b713b794717c9c1de5daeb07a5ebe5560ded835cbf1ee8",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "57255e00-01cf-4369-833d-9d22a682e681",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "c2b48b55-ad2b-43a4-b0fc-79627f880bb6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 4

Participante ficticio: ¿Se admite el valor 1000?

Respuesta íntegra:

Entrada mil: dígitos admitidos, conversión posible y rechazo por rango; no se guarda.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Se admite el valor 1000?",
  "http_status": 200,
  "response": {
    "turn_id": "cb759b41-81d5-4679-adb2-a6bccb8d350f",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Entrada mil: dígitos admitidos, conversión posible y rechazo por rango; no se guarda.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "fbc6d1db-8bec-4b25-bd86-4cd51a01505d",
        "document_version": 1,
        "location_ref": "párrafo 26 (Reglas de validación)",
        "fragment_text": "Ejemplo 2. Entrada mil: dígitos admitidos, conversión posible y rechazo por rango; no se guarda.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "f51e4f62-2a52-4762-a552-29bf57e3ee5d"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 171,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Se admite el valor 1000?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "f51e4f62-2a52-4762-a552-29bf57e3ee5d"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "cb759b41-81d5-4679-adb2-a6bccb8d350f",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "6173150ad99a547f2a0df220369a64a0eece16883f5520857959383759d5f546",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "4f83cf16-8c25-44d5-928c-04571c1fb6b5",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "c2b48b55-ad2b-43a4-b0fc-79627f880bb6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 5

Participante ficticio: ¿Qué ocurre con ese último valor?

Respuesta íntegra:

Sí, cero es una cantidad válida. No, mil no es aceptable en este programa. Un número puede ser un entero correcto y aun así incumplir una regla de negocio.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Qué ocurre con ese último valor?",
  "http_status": 200,
  "response": {
    "turn_id": "215243a3-6ded-46d2-9a47-ef769a9218d8",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Sí, cero es una cantidad válida. No, mil no es aceptable en este programa. Un número puede ser un entero correcto y aun así incumplir una regla de negocio.",
    "state_version": 15,
    "sources": [
      {
        "document_id": "fbc6d1db-8bec-4b25-bd86-4cd51a01505d",
        "document_version": 1,
        "location_ref": "párrafo 22 (Reglas de validación)",
        "fragment_text": "Qué es posible. Sí, cero es una cantidad válida. No, mil no es aceptable en este programa. Un número puede ser un entero correcto y aun así incumplir una regla de negocio.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "70140653-ac32-43e8-8d83-c485cea3af4a"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Qué ocurre con ese último valor?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "70140653-ac32-43e8-8d83-c485cea3af4a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "215243a3-6ded-46d2-9a47-ef769a9218d8",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "7c5fbf214fe1d39711b8c42bd4886c0ea805c729730d2de2058704cf105c6443",
    "stalled_count": 0,
    "last_notice": null,
    "offered_actions": [],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "c313b24d-88e2-4867-9afe-a4191bfb474d",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "c2b48b55-ad2b-43a4-b0fc-79627f880bb6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "material-fragment-response",
      "template_version": 1,
      "template_sha256": "d5312ed1c947e130352c866a497299b681caa41d2db27359bc10bd790d8391a7",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 6

Participante ficticio: ¿De dónde procede esa explicación?

Respuesta íntegra:

La procedencia vigente es 02 programa caso, sección párrafo 22 (Reglas de validación). Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿De dónde procede esa explicación?",
  "http_status": 200,
  "response": {
    "turn_id": "0b549152-e0b5-4f1e-9f8f-a04a77b768bd",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La procedencia vigente es 02 programa caso, sección párrafo 22 (Reglas de validación). Identifico la procedencia, no leo fragmentos de la fuente. Para ampliar di más sobre la fuente; para seguir di ayuda o continúa.",
    "state_version": 18,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "sources",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 390,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Qué ocurre con ese último valor?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "70140653-ac32-43e8-8d83-c485cea3af4a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "215243a3-6ded-46d2-9a47-ef769a9218d8",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "content_question",
        "confidence_kind": "heuristic",
        "reason_code": "content_input"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "780d66f2d0bf6f7419d9d2f6aed461bc964a7b4c432e6c8582458edb73b50902",
    "stalled_count": 1,
    "last_notice": "sources",
    "offered_actions": [
      "rephrase",
      "topic_switch"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": false,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "e1383339-e344-473f-b6ca-521d10fea646",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "c2b48b55-ad2b-43a4-b0fc-79627f880bb6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-sources",
      "template_version": 1,
      "template_sha256": "f285cc0fefcf32de222f0315c5d60a32a98f5798aa9c31038b39454e750109b0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 7

Participante ficticio: Terminar la sesión sin guardar esta conversación.

Respuesta íntegra:

¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Terminar la sesión sin guardar esta conversación.",
  "http_status": 200,
  "response": {
    "turn_id": "969ca079-4460-4f28-b57e-debf9ecf09bf",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "¿Quieres cerrar esta sesión? Se conservará nada. Di confirmo cerrar para finalizar o continuar sesión para seguir. Para cambiar la conservación di qué conservarás antes de confirmar el cierre.",
    "state_version": 21,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "close_confirm",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 375,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    }
  },
  "context": {
    "schema_version": 2,
    "current_topic_ref": "validacion",
    "content_query": "¿Qué ocurre con ese último valor?",
    "pending_question_turn_id": null,
    "pending_question_unit_id": null,
    "claim_followup": null,
    "last_approved_unit_ids": [
      "70140653-ac32-43e8-8d83-c485cea3af4a"
    ],
    "pending_topic_ref": null,
    "last_approved_turn_id": "215243a3-6ded-46d2-9a47-ef769a9218d8",
    "candidate_referents": [
      {
        "kind": "topic",
        "ref": "validacion"
      }
    ],
    "selected_referent": null,
    "intent_hypotheses": [
      {
        "label": "finish",
        "confidence_kind": "heuristic",
        "reason_code": "explicit_control"
      }
    ],
    "current_subgoal_ref": "validacion",
    "relevant_concepts": [
      "validacion"
    ],
    "support_step": 0,
    "stalled_signature": "8779869651bfd23464920f478b5bc13d3e209a2f86e20e543585b3f782a52355",
    "stalled_count": 2,
    "last_notice": "close_confirm",
    "offered_actions": [
      "help",
      "topic_switch",
      "finish"
    ],
    "effective_profile": "guided_controlled",
    "navigation_page": 0,
    "pending_conservation": null,
    "close_confirmation_pending": true,
    "evidence_refs": []
  },
  "status": "active",
  "final_verification": {
    "proposal_id": "77155ee5-d314-4e87-9b32-82dd1e78f603",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "c2b48b55-ad2b-43a4-b0fc-79627f880bb6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-close-confirm",
      "template_version": 1,
      "template_sha256": "791247eb9606d23d7223e885b437a948623f8302f0fddd35d13aec626ed9aeb0",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


### Paso 8

Participante ficticio: Confirmo finalizar sin conservarlos.

Respuesta íntegra:

La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Confirmo finalizar sin conservarlos.",
  "http_status": 200,
  "response": {
    "turn_id": "d1645242-9950-4a97-8ba9-1983a4ad2433",
    "mode": "doubt_resolution",
    "dialogue_action": "finish",
    "output_text": "La sesión ha terminado. Se aplica la elección confirmada: nada. Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.",
    "state_version": 24,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "finish",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "finish",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 391,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": [
        "help",
        "topic_switch",
        "finish"
      ]
    },
    "session_closed": true,
    "session_status": "closed_voluntary",
    "study_summary": {
      "turn_count": 8,
      "duration_seconds": 2,
      "modes_used": [
        "doubt_resolution"
      ],
      "concepts_addressed": [
        "validacion"
      ],
      "practice_questions_count": 0,
      "practice_question_types": [],
      "sources_consulted_fragment_ids": [
        "09b71e46-6af4-4024-8c13-c18af67cd6c6",
        "0edbf2a8-0e33-4d95-b8f4-0ce6bd17c810",
        "0f79bd12-d508-432f-97ca-500a0e7e5180",
        "6e742bd9-2bfd-416a-9470-2528d67ea380",
        "962b637f-4348-4fe0-a65c-a08b09ebeaf8"
      ],
      "incidents": []
    }
  },
  "context": null,
  "status": "closed_voluntary",
  "final_verification": {
    "proposal_id": "52eccfd4-3e62-479a-9335-88176df50174",
    "verifier_agent_id": "constitutional-control",
    "verdict": "approved",
    "reasons": [],
    "authorization_context": {
      "activity_configuration_id": "c2b48b55-ad2b-43a4-b0fc-79627f880bb6",
      "activity_version": 1,
      "policy_id": "guided-screenless/v4",
      "policy_version": 1,
      "schema_version": 1,
      "policy_sha256": "997e24811125ebd65d197159802efce79e529dd69c0ecf70b0589b204666c23f",
      "template_id": "screenless-finish",
      "template_version": 1,
      "template_sha256": "85e8fba63f2cb86d3972c85be828a49602b59134e8357ccb53a55b8f43d23520",
      "message_type": "normal",
      "attempt": 0
    }
  }
}
```


## Bloque 13: audit-prefixes-v7-first/agua-docx

Evaluación humana: **pendiente**. Resultado técnico: `[]`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: ¿El agua puede pasar a vapor sin hervir?

Respuesta íntegra:

Sí, el agua líquida puede pasar a vapor sin hervir mediante evaporación. También puede producir vapor por ebullición bajo las condiciones adecuadas. Que un ejemplo muestre una vía no excluye la otra.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿El agua puede pasar a vapor sin hervir?",
  "http_status": 200,
  "response": {
    "turn_id": "89e75438-c24d-4c4a-8ef9-8b56ced58d04",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Sí, el agua líquida puede pasar a vapor sin hervir mediante evaporación. También puede producir vapor por ebullición bajo las condiciones adecuadas. Que un ejemplo muestre una vía no excluye la otra.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "f3e743f7-976e-4c2d-ab45-6e878dc0535b",
        "document_version": 1,
        "location_ref": "párrafo 9 (Evaporación)",
        "fragment_text": "Qué es posible. Sí, el agua líquida puede pasar a vapor sin hervir mediante evaporación. También puede producir vapor por ebullición bajo las condiciones adecuadas. Que un ejemplo muestre una vía no excluye la otra.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "ee0a1c58-ac22-4868-99e2-47f83c9a6737"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 250,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  }
}
```


### Paso 2

Participante ficticio: ¿Por qué sale del líquido?

Respuesta íntegra:

Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Por qué sale del líquido?",
  "http_status": 200,
  "response": {
    "turn_id": "1614a843-2253-4939-b562-3b263b3720d6",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
    "state_version": 6,
    "sources": [
      {
        "document_id": "f3e743f7-976e-4c2d-ab45-6e878dc0535b",
        "document_version": 1,
        "location_ref": "párrafo 6 (Evaporación)",
        "fragment_text": "Por qué. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "d51d007b-8f60-4c5a-a849-2a064547e43c"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  }
}
```


### Paso 3

Participante ficticio: No lo entiendo. ¿Se rompe el agua en hidrógeno y oxígeno?

Respuesta íntegra:

La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "No lo entiendo. ¿Se rompe el agua en hidrógeno y oxígeno?",
  "http_status": 200,
  "response": {
    "turn_id": "d781ec47-4b08-4d46-a12e-81d9778c6c8f",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
    "state_version": 9,
    "sources": [
      {
        "document_id": "f3e743f7-976e-4c2d-ab45-6e878dc0535b",
        "document_version": 1,
        "location_ref": "párrafo 6 (Evaporación)",
        "fragment_text": "Por qué. Las moléculas del líquido se mueven y no tienen todas la misma energía. Algunas próximas a la superficie pueden vencer las atracciones entre moléculas y escapar como vapor. La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "8511ad5a-ccfb-41ba-81b6-433c8b296a62"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  }
}
```


### Paso 4

Participante ficticio: Sigo sin verlo. Explícamelo de otra manera.

Respuesta íntegra:

Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Sigo sin verlo. Explícamelo de otra manera.",
  "http_status": 200,
  "response": {
    "turn_id": "7fcbbd66-db7a-41e0-8492-157c4612ed92",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.",
    "state_version": 12,
    "sources": [
      {
        "document_id": "f3e743f7-976e-4c2d-ab45-6e878dc0535b",
        "document_version": 1,
        "location_ref": "párrafo 8 (Evaporación)",
        "fragment_text": "Otra explicación. Piensa en una tela húmeda. El agua no desaparece: parte pasa al aire en forma gaseosa. Observamos menos líquido en la tela; el mecanismo consiste en la salida de moléculas por las superficies mojadas. Esta explicación cambia de escala, desde lo que vemos hasta lo que sucede entre moléculas.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "rephrase",
      "repeat_target": null,
      "support_step": 1,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "26757cb2-54ce-45e5-90d2-2aaa287d4a4e"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "condensacion",
        "congelacion",
        "ebullicion",
        "evaporacion",
        "presion"
      ],
      "offered_actions": []
    }
  }
}
```


## Bloque 14: audit-prefixes-v7-first/datos-pdf

Evaluación humana: **pendiente**. Resultado técnico: `[]`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: ¿Qué significa mediana?

Respuesta íntegra:

La mediana es el centro de los valores ordenados. Para la serie A ordenada, dos, tres, tres, cuatro y dieciocho, la posición central es la tercera y la mediana es tres segundos.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Qué significa mediana?",
  "http_status": 200,
  "response": {
    "turn_id": "a8c3e837-abd9-4271-ab9d-8dd4022bb00c",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "La mediana es el centro de los valores ordenados. Para la serie A ordenada, dos, tres, tres, cuatro y dieciocho, la posición central es la tercera y la mediana es tres segundos.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "1dedf0c0-51e5-4524-8383-7fdecd19d1c2",
        "document_version": 1,
        "location_ref": "página 3",
        "fragment_text": "Mediana y posición\nLa mediana es el centro de los valores ordenados. Para la serie A ordenada, dos, tres, tres, cuatro y\ndieciocho, la posición central es la tercera y la mediana es tres segundos. Primero, ordena las cinco duraciones de menor a mayor. Después, identifica la tercera, porque\nquedan dos a cada lado. Esa duración es tres segundos. Si hubiera un número par de valores, se\nusaría la media de los dos centrales. La mediana se basa en posiciones del orden, por lo que un valor extremo puede cambiar mucho sin\ndesplazar el valor central en este ejemplo. La media usa la magnitud de todos los valores; la mediana identifica el centro del orden. En la serie\nA la duración dieciocho separa ambas descripciones. En una cantidad par de datos se necesita una media de dos posiciones centrales.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "0bcad35f-5f82-4da6-91aa-a4ea3c971ef2"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  }
}
```


### Paso 2

Participante ficticio: ¿Y la otra?

Respuesta íntegra:

No puedo resolver esa referencia con seguridad. Temas disponibles: ausentes, dispersion, interpretacion. Di elijo y el nombre del tema, repetir opciones o terminar la sesión.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "¿Y la otra?",
  "http_status": 200,
  "response": {
    "turn_id": "ddff6d17-a82c-478e-8945-85a69f0a159e",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "No puedo resolver esa referencia con seguridad. Temas disponibles: ausentes, dispersion, interpretacion. Di elijo y el nombre del tema, repetir opciones o terminar la sesión.",
    "state_version": 6,
    "sources": [],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "fixed-dialogue-template/v1",
      "primary_act": "ambiguous",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [],
      "notice": "clarify",
      "grounding_verdict": "not_applicable",
      "coherence_verdict": "not_applicable",
      "non_disclosure_verdict": "not_applicable",
      "latency_ms": 390,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": [
        "rephrase",
        "topic_switch"
      ]
    }
  }
}
```


### Paso 3

Participante ficticio: La media

Respuesta íntegra:

En esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos, tres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el número de observaciones válidas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "La media",
  "http_status": 200,
  "response": {
    "turn_id": "ce5f941a-6c04-4406-a3c8-f2685466bb14",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "En esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos, tres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el número de observaciones válidas.",
    "state_version": 9,
    "sources": [
      {
        "document_id": "1dedf0c0-51e5-4524-8383-7fdecd19d1c2",
        "document_version": 1,
        "location_ref": "página 2",
        "fragment_text": "Media aritmética\nEn esta práctica ficticia se registran duraciones de un proceso, en segundos. La serie A es dos,\ntres, tres, cuatro y dieciocho. La media aritmética se obtiene sumando los valores y dividiendo por el\nnúmero de observaciones válidas. Primero, comprueba que todas las duraciones usan segundos. Después, suma dos, tres, tres,\ncuatro y dieciocho: treinta segundos. Cuenta cinco observaciones válidas. Por último, divide treinta\nentre cinco: la media es seis segundos. Al dividir la suma entre el número de datos, se obtiene un reparto uniforme del total. Un valor\ngrande puede aumentar la media aunque la mayoría de las observaciones sean pequeñas. La suma expresa tiempo acumulado; la media expresa el total por observación. Confundirlas\ncambia tanto el número como la interpretación.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "b83878ae-170a-4bb6-bd3e-dea7640cde47"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 155,
      "turn_budget_ms": 10000,
      "available_topics": [
        "ausentes",
        "dispersion",
        "interpretacion",
        "media",
        "mediana"
      ],
      "offered_actions": []
    }
  }
}
```


## Bloque 15: audit-prefixes-v7-first/programa-docx

Evaluación humana: **pendiente**. Resultado técnico: `[]`.

Criterio: intención/pertinencia, suficiencia, continuidad, fuente, no revelación y efecto de privacidad. Registrar aceptar/requiere corrección y justificación; ninguna casilla está aprobada por pruebas.


### Paso 1

Participante ficticio: Buenas, ¿qué es validar exactamente?

Respuesta íntegra:

Hola. Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.

Registro íntegro de HTTP, fuentes, estado, pregunta emitida y verificaciones:

```json
{
  "input": "Buenas, ¿qué es validar exactamente?",
  "http_status": 200,
  "response": {
    "turn_id": "3139c9af-5044-40e7-b19c-436562fe29bd",
    "mode": "doubt_resolution",
    "dialogue_action": "respond",
    "output_text": "Hola. Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.",
    "state_version": 3,
    "sources": [
      {
        "document_id": "99e1bb61-252e-4afd-bec5-e3f6fa7edfc1",
        "document_version": 1,
        "location_ref": "Definición funcional propuesta, revisión humana pendiente",
        "fragment_text": "Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. En Registro Local se comprueba el formato admitido y el rango de la cantidad. Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.",
        "content_withheld": false
      }
    ],
    "general_knowledge_used": false,
    "dialogue_status": {
      "screenless_text_ready": true,
      "conservation": {
        "retain": false,
        "scope": []
      },
      "available_modes": [
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review"
      ],
      "effective_profile": "guided_controlled",
      "provider": "reviewed-unit-renderer/v1",
      "primary_act": "content_question",
      "repeat_target": null,
      "support_step": 0,
      "pending_topic": null,
      "claim_followup": null,
      "pending_question": null,
      "rendered_unit_ids": [
        "12683411-aa28-4e17-a423-1f3f4d359511"
      ],
      "notice": null,
      "grounding_verdict": "fundamentada",
      "coherence_verdict": "approved",
      "non_disclosure_verdict": "approved",
      "latency_ms": 172,
      "turn_budget_ms": 10000,
      "available_topics": [
        "almacenamiento",
        "entrada",
        "responsabilidades",
        "salida",
        "validacion"
      ],
      "offered_actions": []
    }
  }
}
```
