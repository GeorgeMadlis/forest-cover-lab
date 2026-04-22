# ADR 0004: Monthly Target Definition

- **Status:** Proposed
- **Date:** 2026-04-22
- **Deciders:** Forest Cover Lab maintainers
- **Technical area:** algorithm
- **Supersedes:** None
- **Superseded by:** None

## Context

The repository roadmap includes monthly forest-cover estimation.

However, annual forest-loss products and monthly forest-state estimates are not the same target.

The project needs a precise statement of what monthly outputs mean, what supervisory signals are valid for training, and what cannot be claimed scientifically.

## Decision

The repository will distinguish between three distinct concepts:

### 1. Monthly forest coverage estimate
Estimated forest area (hectares) for a calendar month, derived from monthly Sentinel composites under v2 or v3.

### 2. Monthly disturbance probability
Estimated probability of a disturbance event occurring in a calendar month, derived from time-series modeling.

### 3. Annual forest-loss supervision
The Hansen `lossyear` product and similar annual products are **weak supervisory signals only**.

If annual labels are used to train monthly models, they must be treated as weak supervision for a latent monthly process. They must **not** be treated as literal monthly ground truth.

### Binding constraint

> Hansen annual loss ≠ monthly ground truth.
> Monthly forest cover must not be claimed as verified when it is derived from annual weak labels.

This constraint must appear in README.md, every monthly report template, and every v3 run manifest.

## Rationale

This decision prevents:

- target leakage (training and evaluating on the same annual label)
- overclaiming monthly correctness from annual consistency
- incorrect interpretation of annual products as monthly labels

It also clarifies the difference between operational monitoring (v2) and latent inference research (v3).

## Alternatives considered

### Treat annual loss as monthly labels
Rejected because the semantics do not match. Annual loss is a composite signal; it cannot be reliably disaggregated to a single month without additional evidence.

### Avoid monthly targets entirely
Rejected because monthly estimation is a core project objective.

### Use only monthly forest state, no disturbance target
Deferred; both targets remain valid research options for v3.

## Consequences

### Positive
- Clearer scientific claims
- Better method selection in v2 and v3
- Cleaner validation design

### Negative
- More complexity in specs and reports
- More care required in communications and PR review

### Neutral / follow-up
- Exact monthly target family may differ between v2 (confirmation) and v3 (latent inference)
- External triangulation is required for credibility in v3

## Acceptance criteria

- v2 spec defines monthly targets using Sentinel composites only
- v3 spec explicitly labels annual Hansen signal as weak supervision
- reports distinguish estimated monthly outputs from supervisory labels
- validation plan includes temporal plausibility review design

## Risks and limitations

- Monthly latent inference may remain underdetermined without dense time series
- External triangulation is required for v3 claims
- Annual consistency with Hansen does not prove monthly correctness

## References

- `specs/v2_monthly_confirmation.md`
- `specs/v3_weak_supervision_monthly.md`
- `validate/validation_plan.md`
- `report/reporting_contract.md`
