import requests

class dog_api:
    def req(self, api):
        resp = requests.get(f"{api}")
        if resp.status_code == 200:
            print("success")
            self.formatted_print(resp.json)
        else:
            print(f"{resp.status_code} error")

api = "https://api.thedogapi.com/v1/breeds"
params = {
    
}

dog_data = dog_api.req(api)
print(dog_data)