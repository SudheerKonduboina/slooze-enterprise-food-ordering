import urllib.request, urllib.error, json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3ItdGhhbm9zIiwicm9sZSI6Ik1FTUJFUiIsImNvdW50cnkiOiJJTkRJQSIsImVtYWlsIjoidGhhbm9zQHRpdGFuLnNwYWNlIiwiZXhwIjoxNzc3NjM0ODc3fQ.vIEbc-USOyNPHg00vYzllXo3oiARF_nXixXViuGuEr8"
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# 1. Create an order
order_data = {
    "restaurant_id": "rest-taj-mahal",
    "items": [{"menu_item_id": "e60e5b2b-3fdd-4d32-a7d5-4e568960df85", "quantity": 1}],
    "notes": "No notes"
}
req1 = urllib.request.Request('http://localhost:8000/api/v1/orders', data=json.dumps(order_data).encode('utf-8'), headers=headers, method='POST')
order_res = json.loads(urllib.request.urlopen(req1).read())
order_id = order_res['id']
print(f"Created order: {order_id}")

# 2. Try to checkout (should fail)
checkout_data = {"payment_method_id": "pm-card-1"}
req2 = urllib.request.Request(f'http://localhost:8000/api/v1/orders/{order_id}/checkout', data=json.dumps(checkout_data).encode('utf-8'), headers=headers, method='POST')
try:
    urllib.request.urlopen(req2)
    print("Success! (Uh oh, this should have failed)")
except urllib.error.HTTPError as e:
    print(f"Checkout Status: {e.code}, Reason: {e.read().decode()}")
