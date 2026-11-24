import json
import os
import subprocess
from pathlib import Path


PROC = Path("/proc")


def identificar_processador() -> str:
    # O locale fixo mantém os nomes dos campos do lscpu em inglês.
    comando = subprocess.run(
        ["lscpu", "--json", "--hierarchic=never"],
        env={**os.environ, "LC_ALL": "C"},
        capture_output=True,
        text=True,
        check=True,
        timeout=5,
    )
    linhas = json.loads(comando.stdout)["lscpu"]
    campos = {item["field"].rstrip(":"): item["data"] for item in linhas}
    modelo = campos.get("Model name")
    if modelo and modelo != "-":
        return modelo

    # Algumas VMs deixam o modelo em branco, mesmo informando o fabricante.
    fabricante = campos.get("Vendor ID") or "Fabricante desconhecido"
    arquitetura = campos["Architecture"]
    return f"{fabricante} ({arquitetura}) — modelo não informado pelo Linux"


def ler_ram_disponivel_mib() -> float:
    for linha in (PROC / "meminfo").read_text().splitlines():
        if linha.startswith("MemAvailable:"):
            # O Linux lista esse campo em kB de 1024 bytes.
            return round(int(linha.split()[1]) / 1024, 2)

    raise RuntimeError("O Linux não informou MemAvailable em /proc/meminfo.")


def contar_processos() -> int:
    # Cada diretório numérico em /proc representa um PID visível ao servidor.
    return sum(1 for entrada in PROC.iterdir() if entrada.name.isdecimal())
