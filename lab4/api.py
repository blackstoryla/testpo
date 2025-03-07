import requests
import json

class PetFriends:
    def __init__(self):
       self.base_url = " https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
    
    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str) -> json:

        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
    
    def update_pet_info(self, auth_key: str, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result