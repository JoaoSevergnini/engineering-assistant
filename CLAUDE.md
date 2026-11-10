@AGENTS.md

## Notas específicas do Claude Code

Este projeto é usado tanto com o Claude Code quanto com o Codex. O `AGENTS.md`, importado acima, é a fonte única dos princípios. Não duplicar aqui o seu conteúdo; este arquivo contém apenas o que é específico do Claude Code.

- **Skills**: a fonte é `.agents/skills/`. A pasta `.claude/skills/` contém apenas ponteiros gerados por `tools/sync_claude_skills.py` e não deve ser editada à mão. Ao acionar uma skill, ler e seguir o `SKILL.md` original em `.agents/skills/<nome>/`.
- **Após criar, renomear ou remover uma skill, ou alterar seu `name`/`description`**, executar `python -B tools/sync_claude_skills.py`. Para apenas conferir: `python -B tools/sync_claude_skills.py --check`.
- **Skills previstas sem conteúdo** (`SKILL.md` vazio ou sem cabeçalho) são ignoradas pela sincronização até serem implementadas.
- **Conhecimento permanente** (preferências, procedimentos, regras, lições aprendidas) deve ser registrado no repositório (`AGENTS.md`, `profile/`, skills), e não apenas na memória do Claude, para que o Codex também tenha acesso.
