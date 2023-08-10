"""Deck Router."""
import strawberry

from app.routers.decks.query.deck_query import DeckQuery

graphql_decks_schema = strawberry.Schema(query=DeckQuery)
