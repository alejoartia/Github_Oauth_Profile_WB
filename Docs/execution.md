

to run it locally , in the root of you project:
uvicorn app.index:app --host 0.0.0.0 --port 15400 --reload

To run with docker compose.  be sure you have docker installed:
docker-compose up -d 