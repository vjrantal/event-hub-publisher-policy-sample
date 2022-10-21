# Event Hub Publisher Policy Sample

## Purpose

This is a sample that demonstrates how to use [publisher policy](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features#publisher-policy) with the [Event Hubs Python SDK](https://pypi.org/project/azure-eventhub/).

## Running locally

The required environment variables are:

```shell
EVENT_HUB_HOSTNAME=<event hubs name>.servicebus.windows.net
EVENT_HUB_NAME=<event hub name>
EVENTHUB_CONSUMER_GROUP=<consumer group name>
EVENT_HUB_SAS_POLICY=<name of the policy>
EVENT_HUB_SAS_KEY=<primary or secondary key of the policy>
EVENT_HUB_CONNECTION_STRING=<primary or secondary connection string that is being used in the receiver side>
```

### Example output

#### receive.py

```shell
$ python receive.py
Partition: 2 has been initialized
Partition: 3 has been initialized
Partition: 1 has been initialized
Partition: 0 has been initialized
Received from publisher-1 via partition 3 with delay 2.527073
Received from publisher-2 via partition 3 with delay 2.20232
Received from publisher-3 via partition 1 with delay 1.882049
Received from publisher-4 via partition 1 with delay 2.041642
Received from publisher-5 via partition 1 with delay 1.947876
Received from publisher-1 via partition 3 with delay 0.119867
Received from publisher-2 via partition 3 with delay 0.300956
Received from publisher-3 via partition 1 with delay 0.301772
Received from publisher-4 via partition 1 with delay 0.271735
Received from publisher-5 via partition 1 with delay 0.239962
```

#### send.py

```shell
$ python send.py
Sent as publisher-1
Sent as publisher-2
Sent as publisher-3
Sent as publisher-4
Sent as publisher-5
Sent as publisher-1
Sent as publisher-2
Sent as publisher-3
Sent as publisher-4
Sent as publisher-5
```

## Related quotas and limits

Please always review from the [authoritative source](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-quotas) but at the time of writing, there is no limit to the amount of publishers as such. Publishers are created by the user and verified in Event Hubs service at the time of authentication (doesn't have to be pre-registered).

There is a limit of 12 authorization rules (same as SAS policy) but one can create as many publishers per rule as wanted.

The limit of number of brokered connections per namespace may effectively limit the amount of publishers as well because each publisher needs a new connection. This limit varies per tier but as an example, it is currently 5000 for the Standard tier.

## Attribution

Most of the code originates from the [SDK samples](https://github.com/azure/azure-sdk-for-python/tree/main/sdk/eventhub/azure-eventhub/samples) and has been modified to work with publisher policies.
