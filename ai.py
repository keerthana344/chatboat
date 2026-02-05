import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
token = os.environ.get("GITHUB_TOKEN")

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

conversation_history = [SystemMessage("You are a helpful assistant.")]

def get_ai_response(user_input):
    conversation_history.append(UserMessage(content=user_input))
    try:
        response = client.complete(
            messages=conversation_history,
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model,
        )
        assistant_message = response.choices[0].message.content
        conversation_history.append(AssistantMessage(assistant_message))
        return assistant_message
    except Exception as e:
        return f"An error occurred: {str(e)}"
