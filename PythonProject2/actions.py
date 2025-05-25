from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionSaveAppointment(Action):
    def name(self) -> Text:
        return "action_save_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        date = tracker.get_slot("DATE")
        time = tracker.get_slot("TIME")
        email = tracker.get_slot("EMAIL")

        # Here you would integrate with calendar/email API
        # For now, just confirm back to user
        dispatcher.utter_message(text=f"Thanks {name}, I’ve scheduled the session on {date} at {time}. We’ll send a confirmation to {email}.")

        return [SlotSet("DATE", None), SlotSet("TIME", None), SlotSet("EMAIL", None)]