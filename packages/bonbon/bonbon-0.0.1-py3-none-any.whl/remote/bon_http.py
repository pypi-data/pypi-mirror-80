import requests


def http_get(**params):
    res = requests.get(**params)
    return res


def http_post(**params):
    res = requests.post(**params)
    return res


if __name__ == "__main__":
    print('### bone http ###')
    url = 'https://discordapp.com/api/webhooks/756388829866229856/KhmGYNADrBHCOqAWUgemQdoBt0XohA00E93hcB28JuQ8BVYIaVtFFtcBWCxrPuIAmXrj'
    data = {
        "username": "Webhook",
        "avatar_url": "https://i.imgur.com/4M34hi2.png",
        "content": "Text message. Up to 2000 characters."
    }
    print(http_post(url=url, data=data))
    print(http_get(url='http://maps.googleapis.com/maps/api/geocode/json'))
