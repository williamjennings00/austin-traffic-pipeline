# Austin Traffic Pipeline

This project ingests Austin traffic incidents, cleans the records, and loads them into PostgreSQL.


How to Run:

Install dependencies
```sh
python3 -m venv venv
```

```sh
source venv/bin/activate
```


```sh
pip install -r requirements.txt
```

Create the environment file and setup based on your system.

```sh
cp .env.example .env
```

Start the project
```sh
docker compose up --build
```
