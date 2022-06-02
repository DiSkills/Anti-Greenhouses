# Anti-Greenhouses

<a href="https://github.com/Anti-Counter021/Anti-Greenhouses/actions?query=workflow" target="_blank">
    <img src="https://github.com/Anti-Counter021/Anti-Greenhouses/workflows/Test/badge.svg" alt="Test">
</a>

## TODO

- [ ] Auth
    - [ ] Database structure
        - [ ] User
            - [ ] Id (int, primary_key, autoincrement, unique, nullable = False)
            - [ ] Username (str, unique, max_length = 150, nullable = False)
            - [ ] Email (str, unique, validate, nullable = False)
            - [ ] Password (str - hash, unique, validate, nullable = False)
            - [ ] Is superuser (bool, default = False, nullable = False)
            - [ ] OTP (bool, default = False, nullable = False)
            - [ ] OTP secret (str, default = otp secret, nullable = False)
            - [ ] Avatar (str, nullable = True)
            - [ ] Date joined (datetime, default = utcnow, nullable = False)
        - [x] Verification
            - [x] Id (int, primary_key, autoincrement, unique, nullable = False)
            - [x] Uuid (str, default = uuid4, nullable = False)
            - [x] Email (str, unique, validate, nullable = False)
        - [ ] Google account (Not clear yet)
    - [ ] Domain
    - [ ] Repository
    - [ ] Service layer
    - [ ] Unit of work (uow)
    - [ ] Functional
        - [ ] Register (Send email with uuid => register)
            - [ ] Confirm email
                - [ ] Celery
        - [ ] Login (cookies)
            - [ ] Access token
            - [ ] Refresh token
        - [ ] Logout
        - [ ] Change data
        - [ ] Change password
        - [ ] Reset password
        - [ ] Load / change / delete avatar (cloud)
            - [ ] Get avatar
        - [ ] My profile
        - [ ] Get username by email
        - [ ] Google auth
        - [ ] Export user data
            - [ ] Celery
        - [ ] 2-step auth
            - [ ] On / off
            - [ ] Login
            - [ ] Request OTP when user change password / reset password
            - [ ] Request OTP when user change data
        - [ ] Permissions
            - [ ] Is anonymous user
            - [ ] Is authenticated user
            - [ ] Is superuser
    - [ ] Tests
        - [ ] Unit
        - [ ] Integration
        - [ ] E2E
        - [ ] Coverage 100%
    - [ ] Admin
        - [ ] Get all users (filter, sort)
        - [ ] Get user
        - [ ] Create
        - [ ] Update
        - [ ] Delete
