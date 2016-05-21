# from django.test import TestCase
from rest_framework.test import APIClient

print "Testing Inventory API"
client = APIClient()
# client.login(username='mahmoud.alismail@gmail.com', password='pass4mahmoud')
response = client.post('/inventory/check_in/', {'shop_id':12, 'products_list': [{'id': 54529006579, 'quantity':20}],}, format='json')
print "Response Code", response.status_code
print response.content
response = client.post('/inventory/check_out/', {'shop_id':12, 'products_list': [{'id': 54529006579, 'quantity':19}],}, format='json')
print "Response Code", response.status_code
print response.content