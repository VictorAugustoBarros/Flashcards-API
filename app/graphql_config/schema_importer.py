"""Cards."""
import os

from ariadne import load_schema, make_executable_schema

from app.graphql_config.cards.mutation.card_mutations import card_mutation
from app.graphql_config.cards.query.card_query import card_query
from app.graphql_config.decks.mutation.deck_mutations import deck_mutation
from app.graphql_config.decks.query.deck_query import deck_query
from app.graphql_config.subdecks.mutation.subdeck_mutations import subdeck_mutation
from app.graphql_config.subdecks.query.subdeck_query import subdeck_query
from app.graphql_config.user_deck.mutation.user_deck_mutations import user_deck_mutation
from app.graphql_config.user_deck.query.user_deck_query import user_deck_query
from app.graphql_config.user_subdeck.mutation.user_subdeck_mutations import (
    user_subdeck_mutation,
)
from app.graphql_config.user_subdeck.query.user_subdeck_query import user_subdeck_query
from app.graphql_config.users.mutation.user_mutations import user_mutation
from app.graphql_config.users.query.user_query import user_query

graphql_schema_file = load_schema.read_graphql_file(
    os.path.join(os.getcwd(), "graphql_config/schema.graphql")
)

graphql_schema = make_executable_schema(
    [graphql_schema_file],
    [
        card_query,
        card_mutation,
        deck_query,
        deck_mutation,
        user_query,
        user_mutation,
        subdeck_query,
        subdeck_mutation,
        user_deck_query,
        user_deck_mutation,
        user_subdeck_query,
        user_subdeck_mutation,
    ],
)
