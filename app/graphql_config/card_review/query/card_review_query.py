import sentry_sdk
from ariadne import QueryType

from app.connections.mysql import MySQLDB
from app.graphql_config.models import CardReviewResponse
from app.services.card_review_service import CardReviewService
from app.graphql_config.models.response import Response
from app.utils.errors import TokenError, DatabaseQueryFailed
from app.utils.middleware_validation import validate_token

card_review_query = QueryType()


@card_review_query.field("get_card_review")
@validate_token
def resolve_get_card_review(*_, card_review_id: int, token: dict) -> CardReviewResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        card_review_service = CardReviewService(session=MySQLDB().session)

        card_review_user = card_review_service.validate_card_review_user(
            user_id=user_info["id"], card_review_id=card_review_id
        )
        if not card_review_user:
            return CardReviewResponse(
                response=Response(success=False, message="CardReview não encontrado!")
            )

        card_review = card_review_service.get_card_review(
            card_review_id=card_review_id
        )

        return CardReviewResponse(
            card_review=card_review, response=Response(success=True)
        )

    except DatabaseQueryFailed:
        return CardReviewResponse(
            response=Response(success=False, message="Falha ao buscar CardReview")
        )

    except TokenError as error:
        return CardReviewResponse(
            response=Response(success=False, message=str(error))
        )

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return CardReviewResponse(
            response=Response(success=False, message="Falha ao buscar CardReview!")
        )
