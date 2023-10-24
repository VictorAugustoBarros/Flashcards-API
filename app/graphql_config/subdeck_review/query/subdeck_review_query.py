import sentry_sdk
from ariadne import QueryType

from app.connections.mysql import MySQLDB
from app.graphql_config.models import SubDeckReviewResponse
from app.services.subdeck_review_service import SubdeckReviewService
from app.graphql_config.models.response import Response
from app.utils.errors import TokenError, DatabaseQueryFailed
from app.utils.middleware_validation import validate_token

subdeck_review_query = QueryType()


@subdeck_review_query.field("get_subdeck_review")
@validate_token
def resolve_get_subdeck_review(
    *_, subdeck_review_id: int, token: dict
) -> SubDeckReviewResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        subdeck_review_service = SubdeckReviewService(session=MySQLDB().session)

        subdeck_review_user = subdeck_review_service.validate_subdeck_review_user(
            user_id=user_info["id"], subdeck_review_id=subdeck_review_id
        )
        if not subdeck_review_user:
            return SubDeckReviewResponse(
                response=Response(success=False, message="Review não encontrado!")
            )

        subdeck_review = subdeck_review_service.get_subdeck_review(
            subdeck_review_id=subdeck_review_id
        )

        return SubDeckReviewResponse(
            subdeck_review=subdeck_review, response=Response(success=True)
        )

    except DatabaseQueryFailed:
        return SubDeckReviewResponse(
            response=Response(success=False, message="Falha ao buscar Review")
        )

    except TokenError as error:
        return SubDeckReviewResponse(
            response=Response(success=False, message=str(error))
        )

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return SubDeckReviewResponse(
            response=Response(success=False, message="Falha ao buscar Review!")
        )
