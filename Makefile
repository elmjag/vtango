all:
	docker compose build

clean:
	docker container prune -f
	docker image prune -f
	docker container prune -f
