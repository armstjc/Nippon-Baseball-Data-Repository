import requests


def get_json_from_url(url:str):
    """
    
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f'Could not connect. The connection was refused.\nHTTP Status Code 401.'
        )
    else:
        raise ConnectionError(
            f'Could not connect.\nHTTP Status code {response.status_code}'
        )

    json_data = response.json()

    return json_data