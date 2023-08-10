"""Cards Router."""
import strawberry

from app.routers.cards.mutations.card_mutations import Mutation
from app.routers.cards.query.card_query import CardQuery

graphql_cards_schema = strawberry.Schema(query=CardQuery, mutation=Mutation)
