# Austin Traffic Pipeline

Data pipeline that ingests, cleans, validates, and integrates Austin traffic and contextual data for analysis and reporting.


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
