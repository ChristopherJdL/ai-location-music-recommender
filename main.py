import lambda_function

if __name__ == '__main__':
    dic = {
        "queryStringParameters": {
            "cityName": "Paris"
        }
    }
    print(lambda_function.lambda_handler(dic, None))