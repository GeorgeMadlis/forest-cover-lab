# Publications Scoring Rubric

Each paper is scored from 0 to 3 on five dimensions.

## 1. Scientific relevance

- **0**: not relevant to forest cover, disturbance, or EO time series
- **1**: tangentially relevant
- **2**: relevant but not closely aligned
- **3**: directly relevant to core repo goals (forest baseline, monthly estimation, or weak supervision)

## 2. Label match

- **0**: label structure is incompatible with the repo problem
- **1**: weak relationship to forest-cover estimation
- **2**: partially aligned (e.g., annual labels only; no temporal disaggregation)
- **3**: strongly aligned with baseline, monthly estimation, or weak supervision goals

## 3. Codeability

- **0**: cannot be implemented from paper details alone
- **1**: major gaps in reproducibility; requires significant inference
- **2**: implementable with some inference
- **3**: clear enough to implement directly; algorithm, data, and evaluation are described

## 4. Reproducibility

- **0**: no code, unclear data, missing detail
- **1**: limited reproducibility
- **2**: moderate reproducibility (methods clear; data may require effort)
- **3**: strong reproducibility — accessible code and/or data, clear methods

## 5. Operational usefulness

- **0**: not useful for the repo roadmap
- **1**: mostly conceptual; unlikely to seed implementation
- **2**: useful with adaptation
- **3**: directly useful for v1, v2, or v3 implementation

## Total score

```
total_score = scientific_relevance + label_match + codeability + reproducibility + operational_usefulness
```

## Suggested interpretation

| Range | Action |
|---|---|
| 12–15 | Shortlist candidate |
| 8–11 | Keep under review |
| 0–7 | Reject or archive |

## Roadmap fit assignment

After scoring, assign one of:

- `v1` — grounding or baseline methodology
- `v2` — monthly confirmation or Sentinel time-series
- `v3` — weak supervision, latent models, or temporal disaggregation
- `reject` — not relevant or not reproducible enough
