def lambda_handler(event, context):
    city = event["queryStringParameters"]["cityName"]

    return {"response" :"hello world {}".format(city)}