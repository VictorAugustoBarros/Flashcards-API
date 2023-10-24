"""Card Mutations GraphQL."""
import sentry_sdk
from ariadne import MutationType

from app.connections.mysql import MySQLDB

from app.utils.errors import TokenError
from app.models.subdeck_review import SubDeckReview
from app.utils.middleware_validation import validate_token
from app.services.subdeck_review_service import SubdeckReviewService
from app.graphql_config.models import SubDeckReviewResponse, Response

subdeck_review_mutation = MutationType()


@subdeck_review_mutation.field("add_subdeck_review")
@validate_token
def resolve_add_subdeck_review(
    _, info, deck_id: int, subdeck_id: int, token: dict
) -> SubDeckReviewResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        subdeck_review_service = SubdeckReviewService(session=MySQLDB().session)
        subdeck_review = subdeck_review_service.create_review(
            subdeck_review=SubDeckReview(
                deck_id=deck_id,
                subdeck_id=subdeck_id,
            )
        )
        if not subdeck_review:
            return SubDeckReviewResponse(
                response=Response(
                    success=False,
                    message="Falha ao criar Review, informações inválidas!",
                )
            )

        return SubDeckReviewResponse(
            subdeck_review=subdeck_review,
            response=Response(success=True, message="Review criado com sucesso!"),
        )

    except TokenError as error:
        return SubDeckReviewResponse(
            response=Response(success=False, message=str(error))
        )

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return SubDeckReviewResponse(
            response=Response(success=False, message="Falha ao criar Review!")
        )


@subdeck_review_mutation.field("delete_subdeck_review")
@validate_token
def resolve_delete_subdeck_review(
    _, info, subdeck_review_id: int, token: dict
) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        subdeck_review_service = SubdeckReviewService(session=MySQLDB().session)
        subdeck_review_service.delete_subdeck_review(
            subdeck_review_id=subdeck_review_id
        )

        return Response(success=True, message="Review deletado com sucesso!")

    except TokenError as error:
        return Response(success=False, message=str(error))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=False, message="Falha ao remover Review!")
