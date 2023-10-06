from app.models.card import Card
from app.models.subdeck import SubDeck


class BaseService:

    def get_subdecks(self, subdecks: list):
        deck_subdecks = []
        for subdeck in subdecks:
            subdeck_cards = []
            if cards := subdeck.cards:
                subdeck_cards = self.get_cards(cards=cards)

            deck_subdecks.append(SubDeck(
                id=subdeck.id,
                name=subdeck.name,
                description=subdeck.description,
                creation_date=subdeck.creation_date,
                cards=subdeck_cards
            ))

        return deck_subdecks

    def get_cards(self, cards: list):
        subdeck_cards = []
        for card in cards:
            subdeck_cards.append(Card(
                id=card.id,
                question=card.question,
                answer=card.answer,
                creation_date=card.creation_date
            ))

        return subdeck_cards
