"""Cards."""
import os

from ariadne import load_schema, make_executable_schema

from app.models.cards.mutation.card_mutations import card_mutation
from app.models.cards.query.card_query import card_query
from app.models.decks.mutation.deck_mutations import deck_mutation
from app.models.decks.query.deck_query import deck_query
from app.models.subdecks.mutation.subdeck_mutations import subdeck_mutation
from app.models.subdecks.query.subdeck_query import subdeck_query
from app.models.user_deck.mutation.user_deck_mutations import user_deck_mutation
from app.models.user_deck.query.user_deck_query import user_deck_query
from app.models.user_subdeck.mutation.user_subdeck_mutations import user_subdeck_mutation
from app.models.user_subdeck.query.user_subdeck_query import user_subdeck_query
from app.models.users.mutation.user_mutations import user_mutation
from app.models.users.query.user_query import user_query

graphql_schema_file = load_schema.read_graphql_file(
    os.path.join(os.getcwd(), "gql_config/schema.graphql")
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
