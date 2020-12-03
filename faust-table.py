# Please complete the TODO items in the code

from dataclasses import asdict, dataclass
import json
import random

import faust


@dataclass
class ClickEvent(faust.Record):
    email: str
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise6", broker="kafka://localhost:9092")
clickevents_topic = app.topic("lesson4.solution5.click_events", value_type=ClickEvent)

#
# Define a uri summary table
#       See: https://faust.readthedocs.io/en/latest/userguide/tables.html#basics
#
uri_summary_table = app.Table("uri_summary", default=int)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    #
    # Group By URI
    #       See: https://faust.readthedocs.io/en/latest/userguide/streams.html#group-by-repartition-the-stream
    # make sure co-partition before start loopibf

    async for clickevent in clickevents.group_by(ClickEvent.uri):
        #
        #  Use the URI as key, and add the number for each click event. Print the updated
        #       entry for each key so you can see how the table is changing.
        #       See: https://faust.readthedocs.io/en/latest/userguide/tables.html#basics
        #
        uri_summary_table[clickevent.uri] += clickevent.number
        print(f"{clickevent.uri} has value of {uri_summary_table[clickevent.uri]}")


if __name__ == "__main__":
    app.main()
