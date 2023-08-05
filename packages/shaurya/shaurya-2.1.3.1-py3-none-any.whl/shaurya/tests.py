
from shaurya.main import *
from shaurya.virus import Virus

auth = 23
actual_auth = 23
var = Authenticate(auth, actual_auth)
if var is True:
    print("ok")
else:
    print("incorrect")

auth = 23
actual_auth = 45
var = Authenticate(auth, actual_auth)
if var is True:
    print("ok")
else:
    print("incorrect")

time = telltime()
print(time)

youtube = return_url_youtube("Arduino")
google = return_url_browser("Arduino")
print(youtube)
print(google)

print_beautify("Hello world! bonjour!")

# no = generate_number(5)
# print(no)
Virus()