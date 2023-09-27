"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the file that contains the status codes
from src import status 
# we need to import the unit under test - counter
from src.counter import app 
import json


class CounterTest(TestCase):
    """Counter tests"""


    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
    
    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    

    def test_update_a_counter(self):
        """It should update a counter"""
        # Step 1: Create a counter
        result = self.client.post('/counters/baz')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Step 2: Check the counter value as a baseline
        get_result = self.client.get('/counters/baz')
        self.assertEqual(get_result.status_code, status.HTTP_200_OK)
        baseline_value = get_result.json.get('baz')
        
        # Step 3: Make a call to update the counter
        update_result = self.client.put('/counters/baz')
        self.assertEqual(update_result.status_code, status.HTTP_200_OK)

        # Step 4: Check that the counter value is one more than the baseline
        get_result = self.client.get('/counters/baz')
        self.assertEqual(get_result.status_code, status.HTTP_200_OK)
        updated_value = get_result.json.get('baz')
        self.assertEqual(updated_value, baseline_value + 1)

    def test_read_a_counter(self):
        """It should read a counter"""
        # Step 1: Create a counter
        create_result = self.client.post('/counters/mycounter')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)

        # Step 2: Read the counter
        read_result = self.client.get('/counters/mycounter')
        self.assertEqual(read_result.status_code, status.HTTP_200_OK)
