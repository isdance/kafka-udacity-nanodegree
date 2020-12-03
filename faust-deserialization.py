from dataclasses import asdict, dataclass
import json
import faust


#
# Define a ClickEvent Record Class with an email (str), timestamp (str), uri(str),
#       and number (int)
#
#       See: https://docs.python.org/3/library/dataclasses.html
#       See: https://faust.readthedocs.io/en/latest/userguide/models.html#model-types
#
@dataclass
class ClickEvent(faust.Record, validation=True, serializer="json"):
    email: str
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise2", broker="kafka://localhost:9092")

#
# Pass 'ClickEvent' type to clickevents_topic, provide the key (uri) and value type to the clickevent
#
clickevents_topic = app.topic(
    "lesson4.solution5.click_events",
    key_type=str,
    value_type=ClickEvent,
)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    async for clickevent in clickevents:
        # now the incoming data from topic has already been type casted 'ClickEvent' object
        # previously it was 'dict' type
        print(type(clickevent))  # <class '__main__.ClickEvent'>
        print(json.dumps(asdict(clickevent), indent=2))


if __name__ == "__main__":
    app.main()
