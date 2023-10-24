"""Cards."""
import os

from ariadne import load_schema, make_executable_schema

from app.graphql_config.cards import card_mutations, card_query
from app.graphql_config.decks import deck_mutations, deck_query
from app.graphql_config.subdecks import subdeck_mutations, subdeck_query
from app.graphql_config.users import user_mutations, user_query
from app.graphql_config.subdeck_review import (
    subdeck_review_mutation,
    subdeck_review_query,
)

graphql_schema_file = load_schema.read_graphql_file(
    os.path.join(os.getcwd(), "graphql_config/schema.graphql")
)

graphql_schema = make_executable_schema(
    [graphql_schema_file],
    [
        card_mutations,
        card_query,
        deck_mutations,
        deck_query,
        subdeck_mutations,
        subdeck_query,
        user_mutations,
        user_query,
        subdeck_review_mutation,
        subdeck_review_query,
    ],
)
