# Notebooks

This directory is for **exploratory analysis only**.

Exploration here should support governance, evidence review, or contract design. Product
notebooks for a specific implementation repo belong with that downstream repo.

## Rules

- Notebooks may support exploration and QA but must not be the sole implementation path for core processing logic.
- Clear all outputs before committing (`nbstripout` is configured in pre-commit).
- Any logic that becomes part of a shared contract test may move to `fetch/`, `process/`,
  `validate/`, or `report/`.
- Any logic that becomes part of a narrow product pipeline should move to the relevant
  downstream repo.
