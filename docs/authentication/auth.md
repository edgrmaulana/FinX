## Authentication

Success Codes:

### HTTP status 200
1. 2000101 -> Login Success
2. 2000102 -> Register success
3. 2000103 -> Change Password success (logged user)
4. 2000104 -> Username valid
5. 2000105 -> Email verification sent
6. 2000106 -> Set Password success (auth user)
7. 2000107 -> Change Password success (logged user)
8. 2000108 ->  success verify user


Error Codes:

### HTTP status 422

1. 4220101 -> Login Failed, username (phone or email) not found
2. 4220102 -> Login Failed, wrong password
3. 4220103 -> Invalid oauth backend value. available "google-oauth2" and "facebook-oauth2"
4. 4220104 -> Invalid password format. 
5. 4220105 -> Failed change password. Current password not match 
6. 4220106 -> Failed login with oauth. Invalid access token.
7. 4220107 -> Invalid phone number format.
8. 4220108 -> Email was alredy exist.
9. 4220109 -> Phone number was alredy exist.
10. 4220110 -> Type nvalid.
11. 4220111 -> Oauth invalid. available "google-oauth2" and "facebook-oauth2"
12. 4220112 -> Forgot token can not null.
13. 4220113 -> Forgot token invalid.
14. 4220114 -> Phone number was not exist in account.
15. 4220115 -> Phone number invalid.
16. 4220116 -> Failed sending OTP. OTP cred error or max attempt
17. 4220117 -> session_id required
18. 4220118 -> Failed verify OTP. wrong code or session_id

### HTTP status 403

1. 4030101 -> Account forbidden access.