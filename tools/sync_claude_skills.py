"""Gera em .claude/skills/ ponteiros para as skills mantidas em .agents/skills/.

O Codex lê as skills de .agents/skills/ e o Claude Code de .claude/skills/.
Como o projeto fica em unidade de rede (links simbólicos/junções indisponíveis),
cada skill do Claude é um SKILL.md mínimo que copia o cabeçalho (name/description)
da skill original e instrui a leitura do SKILL.md original.

Uso:
    python -B tools/sync_claude_skills.py          # gera/atualiza/remove ponteiros
    python -B tools/sync_claude_skills.py --check  # só confere; código 1 se desatualizado

Regras:
- Skills sem cabeçalho YAML (ex.: SKILL.md vazio, skill apenas prevista) são ignoradas.
- Só são removidos ponteiros que contêm o marcador de arquivo gerado; pastas criadas
  à mão em .claude/skills/ nunca são apagadas.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / ".agents" / "skills"
TARGET_DIR = ROOT / ".claude" / "skills"
# Mensagens de console em ASCII: o terminal pode nao usar UTF-8.
MARKER = "<!-- GERADO por tools/sync_claude_skills.py - nao editar a mao. -->"

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
NAME_RE = re.compile(r"^name:[ \t]*['\"]?([^'\"\r\n]+?)['\"]?[ \t]*$", re.MULTILINE)


def read_frontmatter(skill_md: Path) -> str | None:
    text = skill_md.read_text(encoding="utf-8-sig")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    return match.group(1).replace("\r\n", "\n").strip("\n")


def build_stub(folder: str, frontmatter: str) -> str:
    source = f".agents/skills/{folder}"
    return (
        f"---\n{frontmatter}\n---\n"
        f"{MARKER}\n"
        f"\n"
        f"# Ponteiro para `{source}/SKILL.md`\n"
        f"\n"
        f"Esta skill é mantida em `{source}/` e compartilhada com o Codex.\n"
        f"\n"
        f"Antes de qualquer ação, leia integralmente `{source}/SKILL.md` "
        f"(caminho relativo à raiz do projeto) e siga-o como a definição da skill.\n"
        f"Referências, scripts e links relativos citados nele devem ser resolvidos "
        f"a partir de `{source}/`, não desta pasta.\n"
    )


def expected_stubs() -> tuple[dict[str, str], list[str], list[str]]:
    stubs: dict[str, str] = {}
    skipped: list[str] = []
    problems: list[str] = []
    for skill_md in sorted(SOURCE_DIR.glob("*/SKILL.md")):
        folder = skill_md.parent.name
        frontmatter = read_frontmatter(skill_md)
        if frontmatter is None:
            skipped.append(folder)
            continue
        name = NAME_RE.search(frontmatter)
        if not name or not re.search(r"^description:", frontmatter, re.MULTILINE):
            problems.append(f"{folder}: cabecalho sem 'name' ou 'description'")
            continue
        if name.group(1).strip() != folder:
            problems.append(f"{folder}: 'name' ({name.group(1).strip()}) difere do nome da pasta")
        stubs[folder] = build_stub(folder, frontmatter)
    return stubs, skipped, problems


def is_generated(skill_md: Path) -> bool:
    return skill_md.is_file() and MARKER in skill_md.read_text(encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="apenas conferir, sem escrever")
    args = parser.parse_args()

    stubs, skipped, problems = expected_stubs()
    pending: list[str] = []

    for folder, content in stubs.items():
        target = TARGET_DIR / folder / "SKILL.md"
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current == content:
            continue
        if current is not None and MARKER not in current:
            problems.append(f"{folder}: .claude/skills/{folder}/SKILL.md existe e nao foi gerado; nao sobrescrito")
            continue
        pending.append(f"{'criar' if current is None else 'atualizar'} {folder}")
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")

    if TARGET_DIR.is_dir():
        for folder_path in sorted(p for p in TARGET_DIR.iterdir() if p.is_dir()):
            if folder_path.name in stubs or not is_generated(folder_path / "SKILL.md"):
                continue
            pending.append(f"remover {folder_path.name} (skill de origem ausente ou sem cabecalho)")
            if not args.check:
                shutil.rmtree(folder_path)

    verb = "Pendente" if args.check else "Feito"
    for item in pending:
        print(f"{verb}: {item}")
    for folder in skipped:
        print(f"Ignorada (sem cabecalho, prevista): {folder}")
    for problem in problems:
        print(f"ATENCAO: {problem}")
    if not pending:
        print(f"Ponteiros em dia: {len(stubs)} skill(s).")

    if args.check and pending:
        return 1
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
