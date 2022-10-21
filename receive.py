import os
from datetime import datetime, timezone

from azure.eventhub import EventHubConsumerClient

CONNECTION_STRING = os.environ["EVENT_HUB_CONNECTION_STRING"]
CONSUMER_GROUP = os.environ["EVENTHUB_CONSUMER_GROUP"]
EVENTHUB_NAME = os.environ["EVENT_HUB_NAME"]


def on_event(partition_context, event):
    # The publisher gets added to the system propertes by the Event Hubs
    # service so it is not part of the payload which is under the control
    # of the sender
    publisher = event.system_properties[b"x-opt-publisher"].decode()
    partition_key = partition_context.partition_id
    time_in_message = datetime.fromisoformat(str(event.message))
    delay = (datetime.now(timezone.utc) - time_in_message).total_seconds()
    print(f"Received from {publisher} via partition {partition_key}"
          f" with delay {delay}")


def on_partition_initialize(partition_context):
    print("Partition: {} has been initialized".format(
        partition_context.partition_id)
    )


def on_partition_close(partition_context, reason):
    print(partition_context, reason)


def on_error(partition_context, error):
    print(partition_context, error)


consumer_client = EventHubConsumerClient.from_connection_string(
    CONNECTION_STRING,
    CONSUMER_GROUP,
    eventhub_name=EVENTHUB_NAME,
)

try:
    with consumer_client:
        consumer_client.receive(
            on_event=on_event,
            on_partition_initialize=on_partition_initialize,
            on_partition_close=on_partition_close,
            on_error=on_error
        )
except KeyboardInterrupt:
    print("Stopped receiving")
