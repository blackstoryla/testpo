import pytest
import json

from api import PetFriends

valid_email = "shulga.olga03@yandex.ru"
valid_password = "12345"
pf = PetFriends()

@pytest.fixture
def auth_key(email=valid_email, password=valid_password) -> json:
    status, result = pf.get_api_key(email=email, password=password)
    assert status == 200
    assert 'key' in result
    return result['key']


@pytest.fixture
@pytest.mark.parametrize("name", ["Алиса"])
@pytest.mark.parametrize("animal_type", ["Собака"])
@pytest.mark.parametrize("age", [1])
def pet_id(auth_key, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status == 200
    assert 'id' in result
    return result['id']

def test_get_api_key_valid():
    status, result = pf.get_api_key(email=valid_email, password=valid_password)

    assert status == 200
    assert 'key' in result
    assert result['key'] != ""

def test_get_api_key_not_valid_email():
    status, result = pf.get_api_key(email=valid_email+"a", password=valid_password)

    assert status != 200

def test_get_api_key_not_valid_password():
    status, result = pf.get_api_key(email=valid_email, password=valid_password+"a")

    assert status != 200

@pytest.mark.parametrize("name", ["W", "w", "Ц", "ц", "Alisa", "Алиса"])
@pytest.mark.parametrize("animal_type", ["Собака", "Попугай", "Крокодил"])
@pytest.mark.parametrize("age", [0, 1, 10])
def test_add_new_pet_valid_data(auth_key, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


@pytest.mark.parametrize("name", ["", "аааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааа"])
@pytest.mark.parametrize("animal_type", ["Собака"])
@pytest.mark.parametrize("age", [1])
def test_add_new_pet_not_valid_name(auth_key, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status != 200


@pytest.mark.parametrize("name", ["Алиса"])
@pytest.mark.parametrize("animal_type", ["", "Человек"])
@pytest.mark.parametrize("age", [1])
def test_add_new_pet_not_valid_animal_type(auth_key, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status != 200

@pytest.mark.parametrize("name", ["Алиса"])
@pytest.mark.parametrize("animal_type", ["Собака"])
@pytest.mark.parametrize("age", [-1, 100])
def test_add_new_pet_not_valid_age(auth_key, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status != 200

@pytest.mark.parametrize("name", ["W", "w", "Ц", "ц", "Alisa", "Алиса"])
@pytest.mark.parametrize("animal_type", ["Собака", "Попугай", "Крокодил"])
@pytest.mark.parametrize("age", [0, 1, 10])
def test_update_pet_info_valid(auth_key, pet_id, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    assert status == 200

@pytest.mark.parametrize("name", ["Алиса"])
@pytest.mark.parametrize("pet_id_not_valid", ["", "d2ea9bec-6b8c-4c66-8c1c-aeeb3f441052"])
@pytest.mark.parametrize("animal_type", ["Собака"])
@pytest.mark.parametrize("age", [1])
def test_update_pet_info_not_valid_pet_id(auth_key, pet_id_not_valid, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.update_pet_info(auth_key, pet_id_not_valid, name, animal_type, age)

    assert status != 200

@pytest.mark.parametrize("name", ["", "аааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааа"])
@pytest.mark.parametrize("animal_type", ["Собака"])
@pytest.mark.parametrize("age", [1])
def test_update_pet_info_not_valid_name(auth_key, pet_id, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    assert status != 200


@pytest.mark.parametrize("name", ["Алиса"])
@pytest.mark.parametrize("animal_type", ["", "Человек"])
@pytest.mark.parametrize("age", [1])
def test_update_pet_info_not_valid_animal_type(auth_key, pet_id, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.aupdate_pet_info(auth_key, pet_id, name, animal_type, age)

    assert status != 200

@pytest.mark.parametrize("name", ["Алиса"])
@pytest.mark.parametrize("animal_type", ["Собака"])
@pytest.mark.parametrize("age", [-1, 100])
def test_update_pet_info_not_valid_age(auth_key, pet_id, name, animal_type, age):
    auth_key = {'key': auth_key}

    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    assert status != 200

@pytest.mark.parametrize("filter", ["","my_pets"])
def test_get_list_of_pets_valid( auth_key, filter):
    auth_key = {'key': auth_key}

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200

@pytest.mark.parametrize("auth_key", ["abracadabra"])
@pytest.mark.parametrize("filter", ["","my_pets"])
def test_get_list_of_pets_not_valid_key( auth_key, filter):
    auth_key = {'key': auth_key}

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200

@pytest.mark.parametrize("filter", ["abracadabra", "e2c4926695071b220431a96f3a1ccd9c0f9e6e0e43e2e0aec70ad1e9"])
def test_get_list_of_pets_not_valid_filter( auth_key, filter):
    auth_key = {'key': auth_key}

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200