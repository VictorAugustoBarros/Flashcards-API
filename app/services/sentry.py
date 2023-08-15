"""Sentry."""
import sentry_sdk


# pylint: disable=too-few-public-methods
class Sentry:
    """Classe de inicialização do Sentry."""

    def __init__(self):
        """Construtor da classe."""
        self.dsn = (
            "https://f9693fd4f1cea1e52b2c2e251f1a551b@o1007602.ingest.sentry.io/4505672229322752"
        )

    def start(self):
        """Startando o Sentry no projeto."""
        sentry_sdk.init(dsn=self.dsn, traces_sample_rate=1.0)
