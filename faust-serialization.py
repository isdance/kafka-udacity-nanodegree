from dataclasses import asdict, dataclass
import json

import faust


@dataclass
class ClickEvent(faust.Record, validation=True, serializer="json"):
    email: str
    timestamp: str
    uri: str
    number: int


@dataclass
# serializer="json|binary" means when serializing, encode to json first, then base64 encode the data to base64 stri
class ClickEventSanitized(faust.Record, validation=True, serializer="json|binary"):
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise3", broker="kafka://localhost:9092")
clickevents_topic = app.topic("lesson4.solution5.click_events", key_type=str, value_type=ClickEvent)
# for output
sanitized_topic = app.topic(
    "lesson4.solution5.click_events_sanitized", key_type=str, value_type=ClickEventSanitized
)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    async for clickevent in clickevents:
        # Modify the incoming click event to remove the user email.
        #       Create and send a ClickEventSanitized object.
        sanitized = ClickEventSanitized(
            timestamp=clickevent.timestamp, uri=clickevent.uri, number=clickevent.number
        )
        print(json.dumps(asdict(sanitized), indent=2))

        # Send the data to the topic you created above.
        #       Make sure to set a key and value
        #
        await sanitized_topic.send(key=sanitized.uri, value=sanitized)


if __name__ == "__main__":
    app.main()
