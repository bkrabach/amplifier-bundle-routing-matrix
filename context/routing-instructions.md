# Model Routing

This session uses the routing matrix system for model selection.

## For Agent Authors

Use `model_role` in agent frontmatter to declare what kind of model your agent needs:

```yaml
model_role: coding                          # simple
model_role: [coding-image, coding, general] # with fallback chain
model_role: fast                            # utility agent
```

## For Delegating Agents

When delegating to sub-agents, you can override the model role:

```json
{
  "agent": "foundation:explorer",
  "instruction": "Analyze these UI screenshots...",
  "model_role": "coding-image"
}
```

Available roles are listed in the system context at the start of each session.
