"""Cards."""
from graphene import ObjectType, String


# pylint: disable=R0903
class AdditionalInfo(ObjectType):
    """Classe modelo para os dados adicionais."""

    text = String()
    image = String()


class Card(ObjectType):
    """Classe modelo Card."""

    question = String()
    answer = String()
    # insert_date = Field(DateTime, default_value=None)
    # additional_info = Field(List(AdditionalInfo), default_value=None)
