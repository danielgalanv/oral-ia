// CPU only: fake-clock UI policy and SSR of the actual React components. No server/browser/GPU.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import test from 'node:test';

const requireWeb = createRequire(new URL('../../apps/web/package.json', import.meta.url));
const ts = requireWeb('typescript');
const React = requireWeb('react');
const { renderToStaticMarkup } = requireWeb('react-dom/server');
const compile = path => ts.transpileModule(readFileSync(new URL(path, import.meta.url), 'utf8'), {
  compilerOptions: { module: ts.ModuleKind.ESNext, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022 },
}).outputText;
const dataURL = code => 'data:text/javascript;base64,' + Buffer.from(code).toString('base64');
const helperURL = dataURL(compile('../../apps/web/src/components/studyRuntime.ts'));
const policy = await import(helperURL);
let webCode = compile('../../apps/web/src/components/WebInspection.tsx');
for (const name of ['react/jsx-runtime', 'react']) {
  webCode = webCode.replaceAll(`from "${name}"`, `from ${JSON.stringify(pathToFileURL(requireWeb.resolve(name)).href)}`);
}
const webURL = dataURL(webCode);
const { default: WebInspection, WebEvidenceView } = await import(webURL);
let componentCode = compile('../../apps/web/src/components/DiagnosticStudy.tsx');
for (const name of ['react/jsx-runtime', 'react']) {
  componentCode = componentCode.replaceAll(`from "${name}"`, `from ${JSON.stringify(pathToFileURL(requireWeb.resolve(name)).href)}`);
}
componentCode = componentCode.replaceAll('from "./studyRuntime"', `from ${JSON.stringify(helperURL)}`);
componentCode = componentCode.replaceAll('from "./WebInspection"', `from ${JSON.stringify(webURL)}`);
const { default: DiagnosticStudy, RuntimeNotice, QuestionForm, api, groupStudySources } = await import(dataURL(componentCode));
const clock = { status: { expires_at_unix_ms: 100000, remaining_seconds: 60, expired: false, renewable: false }, sampledAt: 1000 };
const html = (component, props) => renderToStaticMarkup(React.createElement(component, props));

test('web is offline by default and opt-in displays notice before acquisition controls', () => {
  assert.match(html(WebInspection, { state: null, localReceipt: null, busy: false }), /offline/);
  const text = html(WebInspection, { state: { enabled: true, concepts: ['software requirements'], policy_version: 1 }, localReceipt: null, busy: false });
  assert.match(text, /Voy a consultar información de Internet/);
  assert.match(text, /no se envían preguntas/);
  assert.match(text, /ranking o la ausencia de pasajes no bastan/);
  assert.match(text, /button disabled/);
});

test('external attribution is separate, linked, unapproved and rendered as inert text', () => {
  const text = html(WebEvidenceView, { receipt: { status: 'acquired_unreviewed', errors: [], documents: [{ title: 'Original', entity: 'Author', url: 'https://original.example/', captured_at: '2026-10-30', edition: null, approval: 'quarantined', duplicate_of: 'hash', fragments: ['<script>steal()</script>'] }] } });
  assert.match(text, /Información de Internet/);
  assert.match(text, /href="https:\/\/original.example\//);
  assert.match(text, /compatibilidad docente inciertos/);
  assert.match(text, /no cuenta como corroboración/);
  assert.match(text, /&lt;script&gt;/);
  assert.doesNotMatch(text, /<script>/);
});

test('local countdown expires without heartbeat and blocks send/late response', () => {
  assert.equal(policy.remainingRuntime(clock, 31000), 30);
  assert.equal(policy.canSend(true, true, true, false, 'draft', clock, 60999), true);
  assert.equal(policy.canSend(true, true, true, false, 'draft', clock, 61000), false);
  assert.equal(policy.acceptResponse(7, 7, clock, 61000), false);
  assert.equal(policy.acceptResponse(7, 8, clock, 2000), false);
  assert.equal(clock.status.remaining_seconds, 60); // ticks cannot renew the server sample
});
test('connection loss, stopped model and closed inspection each block submission', () => {
  for (const flags of [[true, false, true], [true, true, false], [false, true, true]]) {
    assert.equal(policy.canSend(...flags, false, 'pending', clock, 2000), false);
  }
  assert.equal(policy.remainingRuntime(null, 100000), null); // fixtures have no invented runtime
});
test('network failure preserves uncertainty; known expiry and lease have distinct explanations', () => {
  const network = new policy.StudyApiError('', 'network');
  assert.match(policy.failureMessage(network, clock, 2000), /No se puede confirmar si recibió/);
  assert.match(policy.failureMessage(network, clock, 2000), /no se reenviará automáticamente/);
  assert.match(policy.failureMessage(network, clock, 61000), /runtime global ha caducado/);
  assert.match(policy.failureMessage(new policy.StudyApiError('', 'lease_expired'), clock, 2000), /inspección se ha cerrado/);
  assert.match(policy.generationMessage('provider_error'), /error de generación/);
  assert.doesNotMatch(policy.generationMessage('provider_error'), /conexión/);
});
test('actual runtime notice renders deadline, interruption warning and expired state', () => {
  assert.match(html(RuntimeNotice, { clock, now: 31000, deadlineSeconds: 50 }), /puede interrumpirse/);
  assert.match(html(RuntimeNotice, { clock, now: 61000, deadlineSeconds: 50 }), /0:00 restantes/);
  assert.match(html(RuntimeNotice, { clock, now: 61000, deadlineSeconds: 50 }), /envío deshabilitado/);
  assert.equal(html(RuntimeNotice, { clock: null, now: 0, deadlineSeconds: 50 }), '');
});
test('actual draft form keeps text editable while disconnected and does not imply receipt', () => {
  const markup = html(QuestionForm, { question: '¿Mi pregunta <sin enviar>?', busy: false, focusChange: false,
    enabled: false, deadlineSeconds: 50, onSubmit() {}, onQuestion() {}, onFocus() {}, onCancel() {} });
  assert.match(markup, /¿Mi pregunta &lt;sin enviar&gt;\?/);
  assert.doesNotMatch(markup, /<textarea[^>]*disabled/);
  assert.match(markup, /<button type="submit" disabled="">/);
  assert.doesNotMatch(markup, /Pregunta recibida|Candidata diagnóstica/);
});
test('expired initial runtime disables opening before any fetch', () => {
  const markup = html(DiagnosticStudy, { provider: 'REAL_TEST_NO_GPU', initialRuntime: { ...clock.status, expired: true, remaining_seconds: 0 } });
  assert.match(markup, /Plazo agotado/);
  assert.match(markup, /<button disabled="">Entrar en inspección temporal/);
});
test('actual transport translates Failed to fetch without retry or invented receipt', async () => {
  const previous = globalThis.fetch;
  let calls = 0;
  globalThis.fetch = async () => { calls++; throw new TypeError('Failed to fetch'); };
  try {
    await assert.rejects(api('turn', { question: 'synthetic' }), error => error instanceof policy.StudyApiError && error.code === 'network');
    assert.equal(calls, 1);
  } finally { globalThis.fetch = previous; }
});
test('body disconnection and HTTP runtime expiry remain distinct typed failures', async () => {
  const previous = globalThis.fetch;
  try {
    globalThis.fetch = async () => ({ ok: true, json: async () => { throw new TypeError('body interrupted'); } });
    await assert.rejects(api('state'), error => error.code === 'network');
    globalThis.fetch = async () => ({ ok: false, status: 410, json: async () => ({ detail: { code: 'runtime_expired', message: 'expired' } }) });
    await assert.rejects(api('state'), error => error.code === 'runtime_expired' && error.status === 410);
  } finally { globalThis.fetch = previous; }
});
test('explicit abort stays an abort, not a false network/model error', async () => {
  const previous = globalThis.fetch;
  const controller = new AbortController(); controller.abort();
  const aborted = new Error('synthetic abort');
  globalThis.fetch = async () => { throw aborted; };
  try { await assert.rejects(api('turn', {}, controller.signal), error => error === aborted); }
  finally { globalThis.fetch = previous; }
});
test('quota prevents submit independently of runtime, focus and provider readiness', () => {
  const quota = { used: 6, maximum: 6, remaining: 0, exhausted: true };
  assert.equal(policy.canSend(true, true, true, false, 'new topic', clock, 2000, quota), false);
  assert.equal(policy.canSend(true, true, true, false, 'draft', clock, 2000, { ...quota, used: 5, remaining: 1, exhausted: false }), true);
  assert.match(policy.generationMessage('invalidated', 'budget_exhausted'), /Cupo de llamadas agotado/);
  assert.match(policy.generationMessage('invalidated', 'model_unavailable'), /modelo está detenido/);
  assert.match(policy.generationMessage('invalidated', 'context_invalid'), /contrato técnico/);
  assert.match(policy.generationMessage('invalidated'), /no facilita una causa específica/);
  assert.doesNotMatch(policy.generationMessage('invalidated'), /presupuesto agotado|cupo agotado/i);
});
test('expanded study profile is announced explicitly in the actual UI', () => {
  const markup = html(DiagnosticStudy, { provider: 'TEST_CPU', deadlineSeconds: 180 });
  assert.match(markup, /Perfil de estudio ampliado optativo/);
  assert.match(markup, /2048 tokens, 180 segundos/);
  assert.match(markup, /16000 caracteres/);
});

test('recoverable search limits explain how to continue without implying exclusion or model failure', () => {
  assert.match(policy.generationMessage('invalidated', 'question_too_long'), /más breve|dividir/i);
  assert.match(policy.generationMessage('invalidated', 'search_context_too_long'), /Cambiar de tema/);
  for (const code of ['question_too_long', 'search_context_too_long', 'no_passages']) {
    assert.match(policy.generationMessage('no_passages', code), /conversación se conserva/i);
    assert.match(policy.generationMessage('no_passages', code), /no se ha consumido/i);
  }
  assert.match(policy.generationMessage('no_passages', 'no_passages'), /no significa que.*fuera/i);
  assert.equal(policy.canSend(true, true, true, false, 'reformulación', clock, 2000), true);
});


test('student view has basic controls and no manual topic or diagnostic controls', () => {
  const form = html(QuestionForm, { studentView: true, question: 'Pregunta', busy: false, focusChange: false, enabled: true, deadlineSeconds: 600, onSubmit() {}, onQuestion() {}, onFocus() {}, onCancel() {} });
  assert.match(form, /Tu pregunta/); assert.match(form, />Enviar</);
  assert.doesNotMatch(form, /checkbox|Cambiar de tema|laboratorio|segundos/);
  const screen = html(DiagnosticStudy, { studentView: true, provider: 'REAL_REVIEWED' });
  assert.match(screen, /Comenzar/);
  assert.doesNotMatch(screen, /Texto bruto|Runtime global|Presupuesto|not_assessed|unverified|publicación/);
});

test('response waiting reports elapsed time without invented stages or repeated live announcements', () => {
  const props = { studentView: true, question: 'Pregunta', busy: true, focusChange: false, enabled: false,
    deadlineSeconds: 600, onSubmit() {}, onQuestion() {}, onFocus() {}, onCancel() {} };
  const response = html(QuestionForm, { ...props, waitingSince: performance.now() });
  assert.match(response, /Preparando la respuesta/);
  assert.match(response, /role="timer" aria-live="off" aria-label="Tiempo de espera"/);
  assert.match(response, />Cancelar</);
  assert.doesNotMatch(response, /Revisando|Generando|aria-busy="true"/);
  const connection = html(QuestionForm, props);
  assert.match(connection, /Conectando/);
  assert.doesNotMatch(connection, /role="timer"|Preparando la respuesta/);
});

test('normal study is uncapped while an explicit experimental quota still blocks', () => {
  assert.equal(policy.canSend(true,true,true,false,'pregunta',null,0,{used:200,maximum:null,remaining:null,exhausted:false}),true);
  assert.equal(policy.canSend(true,true,true,false,'pregunta',null,0,{used:12,maximum:12,remaining:0,exhausted:true}),false);
});

test('sources group by document URL, retain pages and do not merge homonymous documents', () => {
  const p={filename:'Documento.pdf',page:4,original_url:'/doc/one#page=4'};
  const groups=groupStudySources([p,p,{...p,page:5,original_url:'/doc/one#page=5'},{...p,original_url:'/doc/two#page=4'}]);
  assert.equal(groups.length,2);
  assert.deepEqual(groups[0][1].map(p=>p.page),[4,5]);
  assert.equal(groups[1][1].length,1);
});
