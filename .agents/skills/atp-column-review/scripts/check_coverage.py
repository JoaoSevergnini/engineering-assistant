"""Valida cobertura documental; nunca calcula ou concede aprovação estrutural."""
import argparse
from collections import Counter
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

ESTADOS = {"COINCIDENTE", "COINCIDE_REFERENCIAS", "DIVERGENTE", "PENDENTE", "NAO_EXAMINADO", "NAO_APLICAVEL"}
CONFRONTADOS = {"COINCIDENTE", "COINCIDE_REFERENCIAS", "DIVERGENTE"}


def texto(value):
    return isinstance(value, str) and bool(value.strip())


def chave(row):
    return tuple(row.get(k) for k in ("pilar", "trecho", "controle"))


def analisar(data):
    erros = []
    esperado = set()
    ocorrencias = set()
    vistos = set()
    contagens = Counter()
    pendencias = []
    nao_examinados = []
    if not isinstance(data, dict):
        return {"erros": ["A matriz deve ser um objeto JSON."], "cobertura_classificada": False}
    if not texto(data.get("escopo")):
        erros.append("Escopo ausente.")
    inventory = data.get("inventario")
    checks = data.get("verificacoes")
    if not isinstance(inventory, list) or not inventory:
        erros.append("Inventário ausente ou vazio.")
        inventory = []
    if not isinstance(checks, list):
        erros.append("Lista de verificações ausente.")
        checks = []
    for index, occurrence in enumerate(inventory):
        if not isinstance(occurrence, dict) or not all(texto(occurrence.get(k)) for k in ("pilar", "trecho")):
            erros.append(f"Ocorrência {index}: identificação inválida.")
            continue
        occurrence_key = (occurrence["pilar"], occurrence["trecho"])
        if occurrence_key in ocorrencias:
            erros.append(f"Ocorrência duplicada: {occurrence_key}.")
        ocorrencias.add(occurrence_key)
        controls = occurrence.get("controles")
        if not isinstance(controls, list) or not controls or not all(texto(c) for c in controls):
            erros.append(f"{occurrence_key}: controles esperados ausentes/inválidos.")
            continue
        for control in controls:
            key = (*occurrence_key, control)
            if key in esperado:
                erros.append(f"Controle esperado duplicado: {key}.")
            esperado.add(key)
    for index, row in enumerate(checks):
        if not isinstance(row, dict) or not all(texto(row.get(k)) for k in ("pilar", "trecho", "controle")):
            erros.append(f"Verificação {index}: chave inválida.")
            continue
        key = chave(row)
        if key in vistos:
            erros.append(f"Verificação duplicada: {key}.")
            continue
        vistos.add(key)
        if key not in esperado:
            erros.append(f"Verificação fora do inventário: {key}.")
            continue
        state = row.get("estado")
        if not isinstance(state, str) or state not in ESTADOS:
            erros.append(f"{key}: estado inválido.")
            continue
        contagens[state] += 1
        if state == "COINCIDE_REFERENCIAS" and row["controle"] != "comprimento_referencias":
            erros.append(f"{key}: correspondência de referências não conclui esse controle.")
        if state in CONFRONTADOS and row["controle"] == "comprimento_cotado":
            direct = row.get("dados_detalhamento", {})
            direct = direct.get("cota_direta_lida") if isinstance(direct, dict) else None
            valid = isinstance(direct, dict) and isinstance(direct.get("unidade"), str) and direct["unidade"] in {"cm", "m"}
            if valid:
                try:
                    value = Decimal(str(direct.get("valor")))
                    valid = value.is_finite() and value > 0
                except InvalidOperation:
                    valid = False
            if not valid:
                erros.append(f"{key}: cota direta lida ausente/inválida; intervalo calculado não a substitui.")
        if state in CONFRONTADOS:
            for side in ("forma", "detalhamento"):
                readings = row.get("dados_" + side)
                if not isinstance(readings, dict) or not readings or all(v is None for v in readings.values()):
                    erros.append(f"{key}: dados independentes de {side} ausentes.")
                sources = row.get("fontes_" + side)
                if not isinstance(sources, list) or not sources:
                    erros.append(f"{key}: fontes de {side} ausentes.")
                    continue
                for source in sources:
                    if not isinstance(source, dict) or not all(texto(source.get(k)) for k in ("arquivo", "revisao", "localizacao", "evidencia")):
                        erros.append(f"{key}: fonte de {side} incompleta.")
        if state in {"PENDENTE", "NAO_APLICAVEL"} and not texto(row.get("motivo")):
            erros.append(f"{key}: {state} sem justificativa.")
        if state == "PENDENTE":
            pendencias.append({"chave": list(key), "motivo": row.get("motivo")})
        if state == "NAO_EXAMINADO":
            nao_examinados.append(list(key))
    ausentes = sorted(esperado - vistos)
    if ausentes:
        erros.append(f"{len(ausentes)} controles esperados sem registro.")
    if nao_examinados:
        erros.append(f"{len(nao_examinados)} controles ainda não examinados.")
    return {
        "escopo": data.get("escopo"),
        "pilares_inventariados": len({p for p, _ in ocorrencias}),
        "trechos_inventariados": len(ocorrencias),
        "controles_esperados": len(esperado),
        "estados": dict(sorted(contagens.items())),
        "controles_confrontados": sum(contagens[s] for s in CONFRONTADOS),
        "referencias_coincidentes": contagens["COINCIDE_REFERENCIAS"],
        "pendencias": pendencias,
        "nao_examinados": nao_examinados,
        "ausentes": [list(k) for k in ausentes],
        "erros": erros,
        "cobertura_classificada": bool(esperado) and not erros,
        "limite": "Cobertura classificada não significa conclusão das pendências nem aprovação estrutural. O inventário precisa ser reconciliado com os documentos.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matriz", type=Path)
    args = parser.parse_args()
    try:
        result = analisar(json.loads(args.matriz.read_text(encoding="utf-8-sig")))
    except (OSError, ValueError) as exc:
        print(json.dumps({"erro_leitura": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["cobertura_classificada"] else 1


if __name__ == "__main__":
    sys.exit(main())
