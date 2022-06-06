# Anti-Greenhouses

---

<a href="https://github.com/Anti-Counter021/Anti-Greenhouses/actions?query=workflow" target="_blank">
    <img src="https://github.com/Anti-Counter021/Anti-Greenhouses/actions/workflows/test.yml/badge.svg" alt="Test">
</a>

<a href="https://github.com/Anti-Counter021/Anti-Greenhouses/search?l=python" target="_blank">
    <img src="https://img.shields.io/github/languages/top/Anti-Counter021/Anti-Greenhouses" alt="Top language"/>
</a>

<a href="https://github.com/Anti-Counter021/Anti-Greenhouses/blob/master/.python-version" target="_blank">
    <img src="https://img.shields.io/badge/python-3.9.5-brightgreen" alt="Python version"/>
</a>

<a href="https://github.com/Anti-Counter021/Anti-Greenhouses/blob/master/pyproject.toml" target="_blank">
    <img src="https://img.shields.io/badge/API-v0.1.0-brightgreen" alt="API version"/>
</a>

<a href="https://github.com/Anti-Counter021/Anti-Greenhouses/blob/master/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/Anti-Counter021/Anti-Greenhouses" alt="license"/>
</a>

<a href="https://opensource.org/docs/definition.php" target="_blank">
    <img src="https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github" alt="Open source"/>
</a>

---

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
