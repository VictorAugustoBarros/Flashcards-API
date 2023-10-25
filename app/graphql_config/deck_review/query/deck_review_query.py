import sentry_sdk
from ariadne import QueryType

from app.connections.mysql import MySQLDB
from app.graphql_config.models import DeckReviewResponse
from app.services.deck_review_service import DeckReviewService
from app.graphql_config.models.response import Response
from app.utils.errors import TokenError, DatabaseQueryFailed
from app.utils.middleware_validation import validate_token

deck_review_query = QueryType()


@deck_review_query.field("get_deck_review")
@validate_token
def resolve_get_deck_review(
    *_, deck_review_id: int, token: dict
) -> DeckReviewResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        deck_review_service = DeckReviewService(session=MySQLDB().session)

        deck_review_user = deck_review_service.validate_subdeck_review_user(
            user_id=user_info["id"], deck_review_id=deck_review_id
        )
        if not deck_review_user:
            return DeckReviewResponse(
                response=Response(success=False, message="Review não encontrado!")
            )

        deck_review = deck_review_service.get_deck_review(
            deck_review_id=deck_review_id
        )

        return DeckReviewResponse(
            deck_review=deck_review, response=Response(success=True)
        )

    except DatabaseQueryFailed:
        return DeckReviewResponse(
            response=Response(success=False, message="Falha ao buscar DeckReview")
        )

    except TokenError as error:
        return DeckReviewResponse(
            response=Response(success=False, message=str(error))
        )

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return DeckReviewResponse(
            response=Response(success=False, message="Falha ao buscar DeckReview!")
        )
