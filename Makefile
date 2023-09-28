.PHONY: export

export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes


build: export
	docker build -t fastapi-photo --platform linux/amd64 . 

run: build
	docker run -ti --rm -p 80:80 -v $(CURDIR)/data:/app/data fastapi-photo