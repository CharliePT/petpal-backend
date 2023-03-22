import requests

class dogcat_api:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {access_token}'}
    def get_data(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")







# dog_data = dog_api.req(api)
# print(dog_data)


