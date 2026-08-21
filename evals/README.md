# Routing Evaluation Fixtures

`routing-cases.json` defines positive, negative, compatibility, and safety cases for the Skill router. It is intentionally model-agnostic: a harness may present each `prompt` to an Agent, observe activated Skills and execution mode, then compare them with the expected contract.

Static validation checks IDs, referenced Skill names, contradictory expectations, and coverage. A future LLM evaluation should also score whether the answer states the version gate, chooses the correct file/Editor/MCP mode, and performs the expected safety behavior.

These fixtures contain no Unreal assets or restricted source and may be extended with project-specific cases.
