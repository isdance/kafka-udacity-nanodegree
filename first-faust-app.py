# Please complete the TODO items in this code

import faust

#
# Create the faust app with a name and broker
#       See: https://faust.readthedocs.io/en/latest/userguide/application.html#application-parameters
#
app = faust.App("my-first-app", broker="localhost:9092")

#
# Connect Faust to lesson4.solution5.click_events, which is created from "rest-proxy-produce-json.py"
#       See: https://faust.readthedocs.io/en/latest/userguide/application.html#app-topic-create-a-topic-description
#
my_topic = app.topic("lesson4.solution5.click_events")

#
# pipe a Kafka topic to an Faust agent
#       See: https://faust.readthedocs.io/en/latest/userguide/application.html#app-agent-define-a-new-stream-processor
#
@app.agent(my_topic)
async def clickevent(clickevents):
    # Define the async for loop that iterates over the infinite "clickevents" stream
    #       See: https://faust.readthedocs.io/en/latest/userguide/agents.html#the-stream
    async for clickevent in clickevents:
        print("clickevent", clickevent)


if __name__ == "__main__":
    app.main()
