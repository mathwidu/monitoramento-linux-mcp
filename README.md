# Monitoramento Linux com MCP

**Matheus Duarte** · Trabalho 2 de Sistemas Distribuídos · Universidade Feevale

Servidor em Python e FastMCP que consulta informações do Linux. O MCP Inspector
se conecta por Streamable HTTP, lista as ferramentas e chama cada uma pelo nome.

## Rodar com Docker

Abra o Docker Desktop e execute na pasta deste arquivo.

```sh
docker compose up --build -d
```

O endereço do servidor é `http://127.0.0.1:9000/mcp`. Para encerrar, execute
`docker compose down`.

## Consultar pelo MCP Inspector

Em outro terminal, com Node.js 22.7.5 ou posterior, abra o cliente usado no vídeo.

```sh
npx --yes @modelcontextprotocol/inspector@1.0.6
```

1. Selecione **Streamable HTTP** em **Transport Type**.
2. Digite `http://127.0.0.1:9000/mcp` no campo **URL** e clique em **Connect**.
3. Abra **Tools** e clique em **List Tools**.
4. Selecione uma ferramenta e clique em **Run Tool**. Nenhuma exige parâmetros.

| Ferramenta | O que devolve | De onde vem |
| --- | --- | --- |
| `cpuName` | Nome do processador, quando disponível | `lscpu` |
| `availableRoot` | Espaço disponível em `/`, em GiB | `shutil.disk_usage` |
| `sizeRoot` | Capacidade total de `/`, em GiB | `shutil.disk_usage` |
| `kernelVersion` | Versão do kernel em execução | `platform.release` |
| `availableRAM` | Estimativa de RAM disponível, em MiB | `MemAvailable` em `/proc/meminfo` |
| `tasks` | Total de processos visíveis ao servidor | Diretórios de PID em `/proc` |
| `systemLoad` | Carga média em 1, 5 e 15 minutos | `os.getloadavg` |

Para conferir um resultado do Inspector, compare `kernelVersion` com o comando
abaixo, executado dentro do mesmo contêiner.

```sh
docker compose exec -T monitoramento uname -r
```

No Docker Desktop para Mac, `/` e os processos são os que o contêiner enxerga.
A RAM, a carga e o kernel vêm do Linux da máquina virtual do Docker. Em Apple
Silicon, quando o Linux omite o modelo do processador, `cpuName` mostra o
fabricante e a arquitetura que conseguiu ler.

## Onde ler o código

- `main.py` registra as sete ferramentas e inicia o servidor.
- `metricas_linux.py` lê o processador, a memória e os processos no Linux.
- `requirements.txt` fixa as versões do FastMCP e do SDK MCP.
- `Dockerfile` monta o ambiente Python. `compose.yaml` publica a porta 9000 no Mac.

Em um Linux com Python 3.13 e `lscpu` disponíveis, também dá para rodar direto.

```sh
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

[Repositório da entrega](https://github.com/mathwidu/monitoramento-linux-mcp)
