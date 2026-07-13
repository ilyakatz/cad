# Codex ↔ Claude rules porter

`port_agent_rules.py` copies the portable Markdown instruction layer between:

- Codex: `AGENTS.md` and `AGENTS.override.md`
- Claude Code: `CLAUDE.md`

It walks the repository, so nested instruction files retain their directory scope.

```bash
# Preview Codex -> Claude
python3 tools/port_agent_rules.py to-claude --dry-run

# Write Codex -> Claude
python3 tools/port_agent_rules.py to-claude

# Write Claude -> Codex
python3 tools/port_agent_rules.py to-codex
```

Generated files contain a marker and can be refreshed safely. The script refuses
to overwrite a hand-maintained destination unless `--force` is supplied.

## Deliberate limits

The script does not translate `.claude/settings.json`, `.codex/config.toml`, hooks,
permissions, or tool allow/deny policies. Their capabilities and security models
are not equivalent. It also warns instead of flattening `.claude/rules/*.md`, since
Claude glob/path scoping has no exact Codex instruction-file equivalent.

Run the tests with:

```bash
python3 -m unittest discover -s tools -p 'test_port_agent_rules.py'
```
