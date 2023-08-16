from unittest import TestCase
from python_graphql_client import GraphqlClient
from app.controllers.card_controller import CardController
from app.connections.dependencies import Dependencies


class TestCardMutation(TestCase):
    """Classe para testes unitário da classe CardController"""

    @classmethod
    def setUp(self) -> None:
        db_conn = Dependencies.create_database()
        self.card_controller = CardController(db_conn=db_conn)

    @classmethod
    def setUpClass(self) -> None:
        self.client = GraphqlClient(endpoint="http://localhost:8000/graphql/")

    def test_add_card(self):
        query = """
            mutation {
              add_card (subdeck_id: 3, question: "Hataraku", answer: "Trabalhar") {
                  card {
                    id
                  }    
                  response {
                      success
                  }    
              }
            }
        """
        result = self.client.execute(query=query)

        success = result["data"]["add_card"]["response"]["success"]
        if success:
            card_id = result["data"]["add_card"]["card"]["id"]
            self.card_controller.delete_card(card_id)

        self.assertTrue(success)
