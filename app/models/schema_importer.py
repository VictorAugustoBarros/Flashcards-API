"""Cards."""
import os
from ariadne import load_schema, make_executable_schema

# Query / Mutation
# Card
from app.models.cards.query.cards_query import card_query
from app.models.cards.mutation.cards_mutations import card_mutation

# Deck
from app.models.decks.query.decks_query import deck_query
from app.models.decks.mutation.decks_mutations import deck_mutation

graphql_schema_file = load_schema.read_graphql_file(os.path.join(os.getcwd(), "schema.graphql"))

graphql_schema = make_executable_schema(
    [graphql_schema_file], [card_query, card_mutation, deck_query, deck_mutation]
)
