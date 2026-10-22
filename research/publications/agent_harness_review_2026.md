# Agent harness evidence assessment

Consulted 2026-10-22; search scope **SS-0003**; source entries **PUB-0013–PUB-0018**
in [the inventory](publications_inventory.csv). Status: candidate interpretation,
human review pending. This targeted review concerns research governance supporting
forest-cover work across v1/v2/v3, not EO methods or forest-map performance.

## Scope and actual search history

Primary documentation was consulted during the preceding recommendation exchange.
SS-0003 was recorded before inventory insertion during implementation; it was not
registered before that earlier consultation. No earlier declaration is claimed.
Queries included `site.developers.openai.com codex multi agents subagents`,
`site.anthropic.com engineering harness agents multi agent`, and
`site.anthropic.com/engineering harness evals multi agent`. Matching official pages
were opened. Secondary search hits and papers not assessed in full are excluded from
this batch. Stop condition: primary coverage of delegation, permissions, handoffs and
evaluation, with transfer limits stated. This is not a systematic or exhaustive review.

## Source assessments

- **PUB-0013**, OpenAI [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents):
  living official documentation, publication date unspecified. Describes separate
  subagent contexts, custom agents, inherited sandbox/approval controls and host-specific
  behavior. Implication: role instructions cannot establish isolation; record the actual
  client, effective permissions and context inheritance. Documentation does not prove
  access or execution in a Lab round.
- **PUB-0014**, OpenAI [Responses multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent):
  living beta API documentation, publication date unspecified. Recommends independent,
  bounded tasks and identifies shared-state contention and token overhead. Implication:
  preserve delegation scope and resource limits; do not infer a universal concurrency
  default or deterministic execution graph. API-specific facilities are not automatically
  available in every Codex client.
- **PUB-0015**, Anthropic [Create custom subagents](https://code.claude.com/docs/en/sub-agents):
  living product documentation, publication date unspecified. Defines specialized
  assistants with separate contexts and configurable access. Implication: host adapters
  need their own observed runtime descriptions. Claude Code and Codex configurations are
  not interchangeable, and no adapter was exercised here.
- **PUB-0016**, Anthropic [Harness design](https://www.anthropic.com/research/harness-design-long-running-apps),
  2026-03-24: engineering case study separating planner, generator and evaluator with
  concrete acceptance criteria and structured communication. Context reset choices changed
  with the model. Implication: version handoff artifacts and evaluate alternative harness
  configurations. An evaluator can criticize outputs without granting scientific approval.
- **PUB-0017**, Anthropic [Agent evaluations](https://www.anthropic.com/research/demystifying-evals-for-ai-agents),
  2026-01-09: distinguishes tasks, repeated trials, graders, traces and final environmental
  outcomes; evaluates the model and harness together. Implication: test observable outcomes
  and provenance rather than trusting a completion narrative. Behavioral evaluation is
  distinct from forest-map accuracy and human scientific review.
- **PUB-0018**, Anthropic [Long-running harnesses](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents),
  2025-11-26: describes incremental work and durable handoffs across limited contexts.
  Implication: preserve state and unresolved work in explicit artifacts. This example does
  not establish that every host/model requires context resets.

Living-document inventory years denote consultation year, not a verified publication
year. All six entries use procedural scores 1/0/2/2/2 (total 7): indirect scientific
relevance, no forest-label match, described implementable patterns, inspectable guidance
without local replication, and potential operational usefulness. These candidate scores
do not measure scientific quality or benchmark performance. Reviewer/date fields remain
empty until an attributable review occurs.

## Proposed incorporation and limits

The [proposed graph ADR](../../docs/adr/0008-agent-governance-graph.md) adds reusable
role/harness/skill contracts, supporting hosts/capabilities, two validation contracts and
explicit non-claims. Every new concept and relation remains candidate. Sources and role
files remain authority; graph records are discoverable summaries. Skills cite the actual
Sentinel checkout's full commit, not a floating branch.

The [evaluation contract](../../validate/agent_harness_evaluation.md) defines a future
comparison. No agents were delegated, model inference benchmarked or behavioral trials
performed in this integration. Separate contexts or model providers do not establish
independent evidence. Execution metadata stays in round manifests. Disturbance candidates
are not legal deforestation, confirmed forest state or causal loss labels; Hansen annual
loss is not monthly ground truth; sensor agreement does not establish cause.
