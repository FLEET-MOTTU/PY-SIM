# PY-SIM
Simulador de Eventos IoT para API Mottu (Python FastAPI)


## Descrição do Projeto

Este projeto é uma API de simulação desenvolvida em Python com FastAPI. Seu objetivo é gerar e enviar eventos de interação de tags BLE (Bluetooth Low Energy) para a API C# de gerenciamento de frota da Mottu, permitindo testar o recebimento e processamento desses eventos pela API principal.

O simulador permite disparar eventos que representam uma tag sendo detectada por um beacon, incluindo informações como o código da tag, o ID do beacon, timestamp e, opcionalmente, o nível da bateria da tag e um tipo de evento customizado.

**Tecnologias Utilizadas:**
* Python 3.12
* FastAPI
* Uvicorn (servidor ASGI)
* HTTPX (para fazer chamadas HTTP para a API C#)
* Docker


## Pré-requisitos

Para rodar este simulador usando Docker, você precisará de:

1.  **Docker Desktop** instalado e em execução.


## Configuração e Inicialização com Docker

Este simulador foi projetado para ser executado como um container Docker.

**1. Construir a Imagem Docker do Simulador:**
   * Clone este repositório (git clone https://github.com/FLEET-MOTTU/PY-SIM)
   * No seu terminal, a partir da pasta raiz do projeto `PY-SIM` (onde está o `Dockerfile`), execute:
     docker build -t mottu-py-simulator .
     Isso construirá a imagem Docker com o nome `mottu-py-simulator`.

**2. Configurar a URL da API C#:**
   O simulador precisa saber para onde enviar os eventos. Isso é feito através da variável de ambiente `CSHARP_API_BASE_URL`.
   * Quando a API C# estiver rodando e acessível em `http://localhost:8080` na sua máquina, você usará esse valor.
   * Na raiz do projeto renomeie o arquivo .env.example para .env e substitua o valor de "URL_API_CSHARP_AQUI" para "http://localhost:8080" (ou a porta em que a API estiver rodando)

**3. Rodar o Container do Simulador Python:**
     docker run --rm -d -p 9090:80 --name simulador-iot mottu-py-simulator


## Como Usar o Simulador para Enviar Eventos para a API C#

Com o simulador Python rodando (acessível em `http://localhost:9090` ou a porta que você mapeou) e sua API C# rodando (acessível em `http://localhost:8080`), você pode usar a interface do Swagger UI do simulador (`http://localhost:9090/docs`) para enviar eventos.

**Endpoint Principal do Simulador:**

* **`POST /simular/interacao_tag`**
    * **Descrição:** Simula uma tag BLE sendo detectada por um beacon.
    * **Parâmetros:**
        * `codigo_unico_tag` (string, obrigatório): O código da tag que foi "vista"(deve ser um código de uma tag que existe e está associada a uma moto no banco de dados da API C#).
        * `beacon_id_detectado` (string, obrigatório): O ID do beacon que "viu" a tag. Ex: `BEACON_ZONA_ENTRADA`.
        * `timestamp_evento` (string ISO datetime, opcional): Data e hora do evento. Se omitido, o simulador usa a hora atual UTC. Ex: `2025-05-20T15:30:00Z`.
        * `nivel_bateria` (integer, opcional): Nível da bateria da tag (0-100).
        * `tipo_evento_custom` (string, opcional): Um texto para descrever o evento. Ex: `entrada_patio`.
    * **Ação:** Ao chamar este endpoint no simulador, ele montará um payload JSON e fará uma requisição `POST` para o endpoint `/api/iot-events/tag-interaction` da API C#.
    * **Verificação:** Observe os logs do container da API C# para ver o processamento do evento e verifique no banco de dados Oracle se os campos da moto (`UltimoBeaconConhecidoId`, `UltimaVezVistoEmPatio`) e da tag (`NivelBateria`) foram atualizados.


## Testando a API
* Copie todo o conteúdo do arquivo JSON 'Mottu_Python_Simulator.postman_collection' localizado na raiz do projeto
* Abra o Postman.
* Cole o contúdo do JSON 'Mottu_Python_Simulator.postman_collection' na aba "Raw text", clique em "Continue" e depois em "Import".
* Uma nova coleção chamada "Mottu Python IoT Simulator - Testes" aparecerá no Postman.
* IMPORTANTE: Você precisará configurar a variável de coleção pythonSimulatorBaseUrl.
    * Clique na coleção "Mottu Python IoT Simulator - Testes".
    * Vá na aba "Variables".
    * Edite a variável pythonSimulatorBaseUrl e no campo "CURRENT VALUE" coloque: http://localhost:9090 (ou a porta que a API Python estiver usando localmente).
* As outras variáveis (targetTagCodigoUnico, etc.) têm valores iniciais baseados em uma moto já cadastrada no banco de dados Oracle da API C#, mas você pode ajustá-las conforme preferir.
