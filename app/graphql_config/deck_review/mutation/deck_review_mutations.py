"""Card Mutations GraphQL."""
import sentry_sdk
from ariadne import MutationType

from app.connections.mysql import MySQLDB

from app.utils.errors import TokenError
from app.models.deck_review import DeckReview
from app.utils.middleware_validation import validate_token
from app.services.deck_review_service import DeckReviewService
from app.services.deck_service import DeckService
from app.graphql_config.models import DeckReviewResponse, Response

deck_review_mutation = MutationType()


@deck_review_mutation.field("add_deck_review")
@validate_token
def resolve_add_deck_review(_, info, deck_id: int, token: dict) -> DeckReviewResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        user_info = token["user_info"]

        mysql_session = MySQLDB().session
        deck_service = DeckService(session=mysql_session)
        deck_user = deck_service.validate_deck_user(user_id=user_info["id"], deck_id=deck_id)
        if not deck_user:
            return DeckReviewResponse(response=Response(success=False, message="Deck não encontrado!"))

        deck_review_service = DeckReviewService(session=mysql_session)
        deck_review = deck_review_service.create_deck_review(
            deck_review=DeckReview(
                deck_id=deck_id
            )
        )
        if not deck_review:
            return DeckReviewResponse(
                response=Response(
                    success=False,
                    message="Falha ao criar DeckReview, informações inválidas!",
                )
            )

        return DeckReviewResponse(
            deck_review=deck_review,
            response=Response(success=True, message="DeckReview criado com sucesso!"),
        )

    except TokenError as error:
        return DeckReviewResponse(
            response=Response(success=False, message=str(error))
        )

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return DeckReviewResponse(
            response=Response(success=False, message="Falha ao criar DeckReview!")
        )


@deck_review_mutation.field("delete_deck_review")
@validate_token
def resolve_delete_deck_review(
    _, info, deck_review_id: int, token: dict
) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        user_info = token["user_info"]

        deck_review_service = DeckReviewService(session=MySQLDB().session)
        deck_review_user = deck_review_service.validate_deck_review_user(user_id=user_info["id"], deck_review_id=deck_review_id)
        if not deck_review_user:
            return Response(success=False, message="DeckReview não encontrado!")

        deck_review_service.delete_deck_review(deck_review_id=deck_review_id)

        return Response(success=True, message="DeckReview deletado com sucesso!")

    except TokenError as error:
        return Response(success=False, message=str(error))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=False, message="Falha ao remover DeckReview!")
