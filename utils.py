from datetime import datetime
from hashlib import sha256

time_now = datetime.now().strftime('%H:%M:%S, %d-%m-%Y')

# generating an API key
crypto_password = sha256(time_now.encode('utf-8')).hexdigest()

print(crypto_password)
