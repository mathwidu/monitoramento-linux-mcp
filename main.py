import os
import platform
import shutil

from fastmcp import FastMCP

from metricas_linux import contar_processos, identificar_processador, ler_ram_disponivel_mib


BYTES_POR_GIB = 1024 ** 3
mcp = FastMCP("Monitoramento Linux")


@mcp.tool(name="cpuName")
def nome_processador() -> str:
    """Retorna a identificação do processador disponível no Linux."""
    return identificar_processador()


@mcp.tool(name="availableRoot")
def espaco_disponivel_raiz() -> dict:
    """Retorna o espaço disponível no sistema de arquivos raiz (/) em GiB."""
    espaco = shutil.disk_usage("/").free
    return {"valor": round(espaco / BYTES_POR_GIB, 2), "unidade": "GiB"}


@mcp.tool(name="sizeRoot")
def capacidade_raiz() -> dict:
    """Retorna a capacidade total do sistema de arquivos raiz (/) em GiB."""
    capacidade = shutil.disk_usage("/").total
    return {"valor": round(capacidade / BYTES_POR_GIB, 2), "unidade": "GiB"}


@mcp.tool(name="kernelVersion")
def versao_kernel() -> str:
    """Retorna a versão do kernel Linux em execução."""
    return platform.release()


@mcp.tool(name="availableRAM")
def ram_disponivel() -> dict:
    """Retorna a estimativa de RAM disponível no Linux em MiB."""
    return {"valor": ler_ram_disponivel_mib(), "unidade": "MiB"}


@mcp.tool(name="tasks")
def quantidade_processos() -> int:
    """Retorna o total de processos visíveis ao servidor, em qualquer estado."""
    return contar_processos()


@mcp.tool(name="systemLoad")
def carga_media() -> dict:
    """Retorna a carga média do Linux nos últimos 1, 5 e 15 minutos."""
    carga_1_min, carga_5_min, carga_15_min = os.getloadavg()
    return {
        "1_min": round(carga_1_min, 2),
        "5_min": round(carga_5_min, 2),
        "15_min": round(carga_15_min, 2),
    }


if __name__ == "__main__":
    if platform.system() != "Linux":
        raise SystemExit("Execute o servidor em Linux ou pelo Docker.")

    endereco = os.environ.get("HOST_MCP", "127.0.0.1")
    mcp.run(
        transport="http", host=endereco, port=9000, path="/mcp", json_response=True
    )
