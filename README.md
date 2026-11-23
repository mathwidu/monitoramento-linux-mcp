# Monitoramento Linux com MCP

Trabalho 2 de Sistemas Distribuídos da Universidade Feevale. O servidor usa
Python 3.13 e FastMCP para expor métricas do Linux. Um cliente MCP descobre as
ferramentas e faz as consultas por Streamable HTTP. O registro das ferramentas
com `@mcp.tool` e a porta `9000` seguem o exemplo de servidor da disciplina.

## Executar com Docker

Com o Docker Desktop aberto, execute na pasta do projeto:

```sh
docker compose up --build
```

O endpoint MCP fica em `http://127.0.0.1:9000/mcp`. O Compose publica a porta
apenas no endereço local do computador. Para encerrar e remover o contêiner
criado pelo projeto, execute `docker compose down`.

## Testar com o MCP Inspector

Em outro terminal, com Node.js 22.7.5 ou posterior, abra a versão do Inspector
usada na demonstração:

```sh
npx --yes @modelcontextprotocol/inspector@1.0.6
```

1. Na interface do Inspector, selecione **Streamable HTTP** em **Transport Type**.
2. Informe `http://127.0.0.1:9000/mcp` no campo **URL** e clique em **Connect**.
3. Abra **Tools** e clique em **List Tools**.
4. Selecione uma ferramenta e clique em **Run Tool**. As sete ferramentas
   funcionam sem parâmetros.

Com Node.js 22.19.0 ou posterior, o Inspector 2.13.0 permite chamar uma
ferramenta pelo terminal:

```sh
npx --yes @modelcontextprotocol/inspector@2.13.0 --cli http://127.0.0.1:9000/mcp \
  --transport http --method tools/call --tool-name kernelVersion
```

## Ferramentas

| Nome | Resultado | Origem no Linux |
| --- | --- | --- |
| `cpuName` | Modelo do processador, quando informado | `lscpu` |
| `availableRoot` | Espaço disponível em `/`, em GiB | `shutil.disk_usage` |
| `sizeRoot` | Capacidade total de `/`, em GiB | `shutil.disk_usage` |
| `kernelVersion` | Versão do kernel em execução | `platform.release` |
| `availableRAM` | RAM disponível para novas aplicações, em MiB | `MemAvailable` em `/proc/meminfo` |
| `tasks` | Total de processos visíveis ao servidor, em qualquer estado | Diretórios de PID em `/proc` |
| `systemLoad` | Carga média em 1, 5 e 15 minutos | `os.getloadavg` |

No Docker Desktop para Mac, o servidor consulta o Linux em que o contêiner
roda. O diretório `/` e os processos são os que o contêiner enxerga. A RAM,
a carga e o kernel vêm do Linux da máquina virtual do Docker. Em Apple Silicon,
se o Linux omitir o modelo de CPU, `cpuName` mostra o fabricante e a arquitetura
disponíveis e informa a ausência do modelo.

## Organização

- `main.py` registra as ferramentas, trata as unidades e sobe o servidor HTTP.
- `metricas_linux.py` concentra a leitura de `lscpu` e dos dados em `/proc`.
- `Dockerfile` define o ambiente Linux. `compose.yaml` conecta a porta do
  contêiner à porta local usada pelo Inspector.
