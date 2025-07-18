### Implement a microservice that exposes an API to solve different mathematical operations

- the pow function

- the n-th fibbonaci number

- the factorial of the number


Each CLI request is logged in a local **SQLite** database using SQLAlchemy.

Technologies Used

- Python 3.12+
- `click` – command-line interface
- `requests` – to send HTTP requests to the backend
- `FastAPI` – REST API framework
- `SQLite` (via `SQLAlchemy`) – to persist requests

All CLI requests are logged into `requests.db` using a `RequestLog` table.

Fields stored:
- `operation` – type of operation (`factorial`, `fibonacci`, `power`)
- `input` – request parameters
- `output` – result of the operation
- `api_key` – provided API key

Start FastAPI server with : python -m uvicorn api.main:app --reload
Run CLI commands with python cli.py factorial/ fibo/power

# Design an API as a production ready service , needs to include

## TODO

- [x] select a framework (sugerez fast api)
- [x] follow MVC pattern
- [x] consider an implementation that supports extensibility
- [x] use a database layer (SQLite)
- [x] make the API endpoints architecture (adica ce metode sa avem , e.g. /pow /fibo_number /factorial etc.. , si cum sa definim requests/response)



Each CLI request is logged in a local **SQLite** database using SQLAlchemy.


## Nice to have - o sa facem obligatoriu =)

- [ ] containerization (la final adaugam docker)
- [x] add API key
- [ ] monitoring
- [x] caching (putem folosi redis pentru caching in special la fibonacci , sa stocam pana intr-o anumita limita - adica primele 50 de numere de exemplu, si cand primim sa returnam al n-lea numar nu mai calculam ci doar dam retrieve din cache - <https://dev.to/sivakumarmanoharan/caching-in-fastapi-unlocking-high-performance-development-20ej>)
- [x] authorization (<https://fastapi.tiangolo.com/tutorial/security/> || <https://stackoverflow.com/questions/76504006/i-want-to-verify-the-jwt-token>)
- [x] logging (loguru / logger-ul din fast api , loguru doar sa fie un utility extern)
- [x] make a cli version out of it
- [ ] make an automated testing program (putem folosi pytest aici)
- [ ] use postman / advanced-rest-client for manual testing
- [ ] make a frontend application that consumes the api
