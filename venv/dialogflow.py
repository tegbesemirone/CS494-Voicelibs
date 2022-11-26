from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
import os

#credentials to connect to dialogflow API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "venv\single-inquiry-369823-b1c6244e4daf.json"
DIALOGFLOW_PROJECT_ID = 'single-inquiry-369823'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
SESSION_ID = 'madlibs-session'


#this function takes in a string and returns the dialogflow agent's response to string given. 
def callAgent(transcript):
    agentResponse = ""
    text_to_be_analyzed = transcript
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    #queries, prints json values if error thrown
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        agentResponse = response.query_result.fulfillment_text
    except InvalidArgument:
        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
        raise

    return agentResponse