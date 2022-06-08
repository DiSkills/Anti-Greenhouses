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

## Technology stack

### Back-end

<a href="https://www.python.org/" target="_blank">
    <img alt="Python" src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen"/>
</a>

<a href="https://fastapi.tiangolo.com/" target="_blank">
    <img alt="FastAPI" src="https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white"/>
</a>

<a href="https://www.sqlalchemy.org/" target="_blank">
    <img alt="SQLAlchemy" src="https://img.shields.io/badge/-SqlAlchemy-FCA121?style=for-the-badge&logo=SqlAlchemy"/>
</a>

<a href="https://www.postgresql.org/" target="_blank">
    <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
</a>

<a href="https://sqlite.org/index.html" target="_blank">
    <img alt="SQLite" src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/>
</a>

<a href="https://www.docker.com/" target="_blank">
    <img alt="Docker" src="https://img.shields.io/badge/-Docker-46a2f1?style=for-the-badge&logo=docker&logoColor=white"/>
</a>

<a href="https://github.com/features/actions" target="_blank">
    <img alt="GitHub actions" src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white"/>
</a>

### Tools

<a href="https://www.jetbrains.com/pycharm/" target="_blank">
    <img alt="PyCharm" src="https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green"/>
</a>

<a href="https://ubuntu.com/" target="_blank">
    <img alt="Linux" src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"/>
</a>

<a href="https://ubuntu.com/" target="_blank">
    <img alt="Ubuntu" src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"/>
</a>

<a href="https://git-scm.com/" target="_blank">
    <img alt="Git" src="https://img.shields.io/badge/-Git-black?style=for-the-badge&logo=git"/>
</a>

<a href="https://github.com/" target="_blank">
    <img alt="GitHub" src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github"/>
</a>

---

## Quick start

    You need docker, docker-compose and make.

    Change the config.example.***.env files in the directory "./configs/" to configs.***.env and add the values.

### Production

    make production

### Testing

    make testing

---

## TODO

- [x] Docker
- [x] GitHub actions
- [ ] Auth
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
