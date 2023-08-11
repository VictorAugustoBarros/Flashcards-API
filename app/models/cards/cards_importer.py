"""Cards."""
from graphene import Schema

from app.models.cards.query.card_query import CardQuery
from app.models.cards.mutation.card_mutations import CardMutation

graphql_cards_schema = Schema(query=CardQuery, mutation=CardMutation)
