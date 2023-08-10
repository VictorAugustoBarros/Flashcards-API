"""Construção da Api FastAPI."""

import fastapi
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from app.routers.cards.cards_router import graphql_cards_schema
from app.routers.decks.decks_router import graphql_decks_schema

app = FastAPI()

# type: ignore
# @TODO -> Alterar a Lib MongoDB para Motor Async (Poll de conexão)
# @TODO -> Criar testes unitários
# @TODO -> Usar Injeção de dependencia -> Trocar o MongoDB pelo DynamoDB de forma simples


class CreateApp:
    """Classe para criação da API FastAPI."""

    def __init__(self, api_app: FastAPI):
        """Construtor da classe.

        Args:
            api_app (FastAPI): Instancia da API FastAPI
        """
        self.api_app = api_app

    @staticmethod
    @app.get("/status")
    def status():
        """Rota para verificação do status da API.

        Returns: Status da aplicação e versionamento das libs utilizadas na API
        """
        return {
            "status": "active",
            "libs": {
                "FastAPI": fastapi.__version__,
                "Uvicorn": uvicorn.__version__,
            },
        }

    def load_graphql(self):
        """Instancia do GraphQL e seus Schemas."""
        graphql_app = GraphQL(graphql_cards_schema, graphql_decks_schema)

        self.api_app.add_route("/graphql", graphql_app)
        self.api_app.add_websocket_route("/graphql", graphql_app)

    def start(self):
        """Carregamento das configurações da API."""
        self.load_graphql()
        return self.api_app


app = CreateApp(api_app=app).start()

if __name__ == "__main__":  # type: ignore
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
