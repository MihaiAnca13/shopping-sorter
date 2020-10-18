import gkeepapi
import keyring

username = "mihai.anca13@gmail.com"

keep = gkeepapi.Keep()
keep.login(username, "")
token = keep.getMasterToken()
keyring.set_password('google-keep-token', username, token)


