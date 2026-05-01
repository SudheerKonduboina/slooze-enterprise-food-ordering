import urllib.request, urllib.error
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3ItdGhhbm9zIiwicm9sZSI6Ik1FTUJFUiIsImNvdW50cnkiOiJJTkRJQSIsImVtYWlsIjoidGhhbm9zQHRpdGFuLnNwYWNlIiwiZXhwIjoxNzc3NjM0ODc3fQ.vIEbc-USOyNPHg00vYzllXo3oiARF_nXixXViuGuEr8"
req = urllib.request.Request('http://localhost:8000/api/v1/restaurants/rest-liberty-grill', headers={'Authorization': f'Bearer {token}'})
try:
    urllib.request.urlopen(req)
    print("Success! (Uh oh, this should have failed)")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code}, Reason: {e.read().decode()}")
