import os
import boto3
import prompts.values as prompts

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
# connect bedrock
# connect spotify API
# if spotify API doesnt return anything with song and artist, try with song only, and of still not, try get a default song.
def lambda_handler(event, context):
    city = event["queryStringParameters"]["cityName"]
    song = get_song(city)
    return {"response" :"hello world {}".format(song)}

def get_song(city):
    client = boto3.client("bedrock-runtime", region_name="eu-west-2",
                          aws_access_key_id=os.getenv("A86K6fA2C8C"),
                          aws_secret_access_key=os.getenv("A86S6fA2C8C"))
    
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompts.clientInput}],
        }
    ]
    
    response = client.converse(modelId=MODEL_ID,messages=conversation,
                               system=[{"text": prompts.systemPrompt}],
                               inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9})

    response_text = response["output"]["message"]["content"][0]["text"]
    return response_text
    