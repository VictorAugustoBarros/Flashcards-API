"""Card Mutations GraphQL."""
import sentry_sdk
from ariadne import MutationType

from app.connections.mysql import MySQLDB

from app.utils.errors import TokenError
from app.models.card_review import CardReview
from app.utils.middleware_validation import validate_token
from app.services.card_service import CardService
from app.services.card_review_service import CardReviewService
from app.graphql_config.models import CardReviewResponse, Response

card_review_mutation = MutationType()


@card_review_mutation.field("add_card_review")
@validate_token
def resolve_add_card_review(_, info, card_id: int, subdeck_review_id: int, review_difficulties_id: int, token: dict) -> CardReviewResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        user_info = token["user_info"]

        mysql_session = MySQLDB().session
        card_service = CardService(session=mysql_session)
        card_user = card_service.validate_card_user(user_id=user_info["id"], card_id=card_id)
        if not card_user:
            return CardReviewResponse(response=Response(success=False, message="Card não encontrado!"))

        card_review_service = CardReviewService(session=mysql_session)
        card_review = card_review_service.create_card_review(
            card_review=CardReview(
                card_id=card_id,
                subdeck_review_id=subdeck_review_id,
                review_difficulties_id=review_difficulties_id
            )
        )
        if not card_review:
            return CardReviewResponse(
                response=Response(
                    success=False,
                    message="Falha ao criar CardReview, informações inválidas!",
                )
            )

        return CardReviewResponse(
            card_review=card_review,
            response=Response(success=True, message="CardReview criado com sucesso!"),
        )

    except TokenError as error:
        return CardReviewResponse(
            response=Response(success=False, message=str(error))
        )

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return CardReviewResponse(
            response=Response(success=False, message="Falha ao criar CardReview!")
        )


@card_review_mutation.field("delete_card_review")
@validate_token
def resolve_delete_card_review(
    _, info, card_review_id: int, token: dict
) -> Response:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        user_info = token["user_info"]

        card_review_service = CardReviewService(session=MySQLDB().session)
        card_review_user = card_review_service.validate_card_review_user(user_id=user_info["id"], card_review_id=card_review_id)
        if not card_review_user:
            return Response(success=False, message="CardReview não encontrado!")

        card_review_service.delete_card_review(card_review_id=card_review_id)

        return Response(success=True, message="CardReview deletado com sucesso!")

    except TokenError as error:
        return Response(success=False, message=str(error))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return Response(success=False, message="Falha ao remover CardReview!")
