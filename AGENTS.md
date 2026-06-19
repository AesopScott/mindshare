# MAPS Agent Instructions

## Always-On MAPS Rules

When working in this repository or editing any MAPS skill:

- Ask exactly one question at a time. Do not present multi-question forms or checklists for the user to fill out.
- Treat `project-foundation.md` as the project control artifact when it exists.
- Use the project's persistent memory contract before running a MAPS skill: notes roots, source roots, memory roots, RAG/read-write rules, and mirrors.
- When a MAPS skill creates or updates durable knowledge, run the shared MAPS memory helper when available and update that skill's named note.
- Every MAPS skill run must end with an explicit completion report: status, outcome, key decisions, memory update, and next skill.
- Every MAPS skill must maintain an in-body version and changelog. Do not add nonstandard version fields to YAML frontmatter.
- Before publishing MAPS skill changes, run `python scripts/validate_maps_skills.py`.
- Role artifacts must define explicit authority boundaries and a learning/growth loop before recommending expanded responsibilities or capabilities.
