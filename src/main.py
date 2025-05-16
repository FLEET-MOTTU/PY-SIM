from fastapi import FastAPI, HTTPException
import httpx
import datetime
import os

app = FastAPI(
    title="Simulador de Eventos IoT",
    description="Essa API simula eventos de tags e beacons para testar a API C#",
    version="0.1.0"
)

CSHARP_API_BASE_URL = os.getenv("CSHARP_API_BASE_URL")

async def enviar_evento_para_api_csharp(endpoint_csharp: str, payload: dict, method: str = "POST"):
    """
    Função genérica para enviar um evento para a API C#
    """
    if not CSHARP_API_BASE_URL:
        raise HTTPException(status_code=400, detail="CSHARP_API_BASE_URL não configurada.")

    url_completa = f"{CSHARP_API_BASE_URL.rstrip('/')}/{endpoint_csharp.lstrip('/')}"
    headers = {'Content-Type': 'application/json'}

    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == "POST":
                response = await client.post(url_completa, json=payload, headers=headers)
            elif method.upper() == "PATCH":
                response = await client.patch(url_completa, json=payload, headers=headers)
            # Adicione outros métodos (PUT, DELETE) se necessário
            else:
                raise ValueError(f"Método HTTP '{method}' não suportado pela função de envio.")

            response.raise_for_status()
            return {"status_simulador": "Evento enviado com sucesso para API C#", "resposta_csharp": response.json()}
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Erro da API C#: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Não foi possível conectar à API C#: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Simulador de IoT up. /docs ve as opções"}


@app.post("/simular/movimentacao_tag", summary="Simula a movimentação de uma tag")
async def simular_movimentacao(tag_id: str, beacon_id: str, tipo_evento: str = "entry"):
    """
    Simula uma tag entrando ('entry') ou saindo ('exit') da área de um beacon.
    """
    payload = {
        "tagId": tag_id,
        "beaconId": beacon_id,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "eventType": tipo_evento
    }
    endpoint_csharp = "movimentacoes"
    return await enviar_evento_para_api_csharp(endpoint_csharp, payload, method="POST")


@app.post("/simular/status_bateria_tag", summary="Simula uma atualização de status da bateria da tag")
async def simular_status_bateria(tag_id: str, nivel_bateria: int):
    """
    Simula uma atualização do nível de bateria de uma tag.
    A API C# deverá ter um endpoint para receber esse status (ex: /tags/{id}/status ou /alertas).
    """
    payload = {
        "batteryLevel": nivel_bateria,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    endpoint_csharp = f"tags/{tag_id}/status"
    return await enviar_evento_para_api_csharp(endpoint_csharp, payload, method="PATCH")
