import boto3
import prompts.values as prompts
import json

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

def get_song_from_curator(city):
    session = boto3.Session()
    client = session.client("bedrock-runtime", region_name="eu-west-2")

    conversation = [
        {
            "role": "user",
            "content": [{"text": city}],
        }
    ]
    
    first_turn_recommendation_text = ask_curator(client, conversation)
    
    enrich_conversation(conversation, first_turn_recommendation_text)

    second_turn_recommendation_text = ask_curator(client, conversation)

    song = json.loads(second_turn_recommendation_text)
    return song

def enrich_conversation(conversation, first_turn_recommendation_text):
    conversation.append({
        "role": "assistant",
        "content": [{"text": first_turn_recommendation_text}],
    })
    conversation.append({
        "role": "user",
        "content": [{"text": prompts.followUpPrompt}],
    })

def ask_curator(client, conversation):
    response = client.converse(modelId=MODEL_ID,messages=conversation,
                               system=[{"text": prompts.systemPrompt}],
                               inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9})

    responseText = response["output"]["message"]["content"][0]["text"]

    return responseText
    