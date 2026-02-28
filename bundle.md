---
bundle:
  name: routing-matrix
  version: 0.1.0

includes:
  - routing-matrix:behaviors/routing.yaml
---

# Routing Matrix

Curated model routing for Amplifier. Maps semantic roles (coding, planning, fast, etc.)
to ranked provider/model lists. Agents declare `model_role` and the system resolves
to the best available model from installed providers.
