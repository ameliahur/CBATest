import requests
from jsonschema import validate

# Base URL for the Swagger Pet Store API
BASE_URL = "https://petstore.swagger.io/v2"

# JSON Schema for validation (example for Pet object)
PET_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "category": {"type": "object"},
        "name": {"type": "string"},
        "photoUrls": {"type": "array"},
        "tags": {"type": "array"},
        "status": {"type": "string"}
    },
    "required": ["id", "name", "photoUrls", "status"]
}

# Test cases for the /pet endpoints

def test_get_pet_by_id():
    """
    Test retrieving a pet by its ID.
    """
    # Create a pet for the test
    pet = {
        "id": 1,
        "category": {"id": 1, "name": "dog"},
        "name": "TestPet",
        "photoUrls": ["http://example.com/testpet.jpg"],
        "tags": [{"id": 1, "name": "test"}],
        "status": "available"
    }
    requests.post(f"{BASE_URL}/pet", json=pet)
    
    # Retrieve the pet
    response = requests.get(f"{BASE_URL}/pet/{pet['id']}")
    assert response.status_code == 200, "Expected status code 200"
    
    # Validate the response schema
    validate(instance=response.json(), schema=PET_SCHEMA)

def test_get_pet_by_invalid_id():
    """
    Test retrieving a pet with an invalid ID.
    """
    pet_id = -1  # Invalid pet ID
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    assert response.status_code == 404, "Expected status code 404 for non-existent pet"

def test_add_new_pet():
    """
    Test adding a new pet to the store.
    """
    new_pet = {
        "id": 12345,
        "category": {"id": 1, "name": "dog"},
        "name": "Buddy",
        "photoUrls": ["http://example.com/dog.jpg"],
        "tags": [{"id": 1, "name": "friendly"}],
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=new_pet)
    assert response.status_code == 200, "Expected status code 200"
    
    # Validate the response schema
    validate(instance=response.json(), schema=PET_SCHEMA)

def test_update_existing_pet():
    """
    Test updating an existing pet.
    """
    updated_pet = {
        "id": 12345,
        "category": {"id": 1, "name": "dog"},
        "name": "BuddyUpdated",
        "photoUrls": ["http://example.com/dog.jpg"],
        "tags": [{"id": 1, "name": "friendly"}],
        "status": "sold"
    }
    response = requests.put(f"{BASE_URL}/pet", json=updated_pet)
    assert response.status_code == 200, "Expected status code 200"
    
    # Validate the response schema
    validate(instance=response.json(), schema=PET_SCHEMA)

def test_find_pets_by_status():
    """
    Test retrieving pets by status.
    """
    response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "available"})
    assert response.status_code == 200, "Expected status code 200"
    assert isinstance(response.json(), list), "Expected a list of pets"

def test_delete_pet():
    """
    Test deleting a pet by its ID.
    """
    # Create a pet for the test
    pet = {
        "id": 2,
        "category": {"id": 1, "name": "cat"},
        "name": "DeletePet",
        "photoUrls": ["http://example.com/deletepet.jpg"],
        "tags": [{"id": 2, "name": "delete"}],
        "status": "available"
    }
    requests.post(f"{BASE_URL}/pet", json=pet)
    
    # Delete the pet
    response = requests.delete(f"{BASE_URL}/pet/{pet['id']}", headers={"api_key": "special-key"})
    assert response.status_code == 200, "Expected status code 200 for successful deletion"

    # Verify the pet no longer exists
    response = requests.get(f"{BASE_URL}/pet/{pet['id']}")
    assert response.status_code == 404, "Expected status code 404 for deleted pet"

def test_delete_nonexistent_pet():
    """
    Test deleting a pet that does not exist.
    """
    pet_id = 99999  # Non-existent pet ID
    response = requests.delete(f"{BASE_URL}/pet/{pet_id}", headers={"api_key": "special-key"})
    assert response.status_code == 404, "Expected status code 404"
