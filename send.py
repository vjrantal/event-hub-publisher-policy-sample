import os
import time
from datetime import datetime, timezone

from azure.core.credentials import AccessToken
from azure.eventhub import EventData, EventHubProducerClient

from token_service import get_expiry, get_token

PRODUCER_COUNT = int(os.environ.get("EVENT_HUB_PRODUCER_COUNT", 1))

FULLY_QUALIFIED_NAMESPACE = os.environ["EVENT_HUB_HOSTNAME"]
EVENTHUB_NAME = os.environ["EVENT_HUB_NAME"]


class CustomizedSASCredential(object):
    def __init__(self, publisher_id):
        self.publisher_id = publisher_id
        self.token_type = b"servicebus.windows.net:sastoken"

    def get_token(self, *scopes, **kwargs):
        # Trigger token renewal when 90% of the expiry time is elapsed
        expiry = time.time() + (get_expiry() * 0.9)
        return AccessToken(get_token(self.publisher_id), expiry)


producers = []
for i in range(1, PRODUCER_COUNT + 1):
    publisher_id = f"publisher-{i}"
    producers.append(
        EventHubProducerClient(
            fully_qualified_namespace=FULLY_QUALIFIED_NAMESPACE,
            # The name part contains the publisher and this needs to match
            # the value that was used to generate the access token or
            # otherwise the server will reject the connection and return
            # an "Unauthorized access"-error
            eventhub_name=f"{EVENTHUB_NAME}/publishers/{publisher_id}",
            credential=CustomizedSASCredential(publisher_id)
        )
    )

i = 0
send_delay_in_seconds = 0.1
while True:
    try:
        producers[i].send_event(
            EventData(str(datetime.now(timezone.utc)))
        )
        print(f"Sent as publisher-{i + 1}")
        i = i < PRODUCER_COUNT - 1 and i + 1 or 0
        time.sleep(send_delay_in_seconds)
    except KeyboardInterrupt:
        for producer in producers:
            producer.close()
        print("Stopped sending")
        break
