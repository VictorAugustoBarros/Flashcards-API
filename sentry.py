import sentry_sdk

sentry_sdk.init(
    dsn="https://f9693fd4f1cea1e52b2c2e251f1a551b@o1007602.ingest.sentry.io/4505672229322752",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

try:
    division_by_zero = 1 / 0

except Exception as error:
    print(error)
