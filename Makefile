.PHONY: export

export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes


build: export
	docker build -t fastapi-photo --platform linux/amd64 . 

run: build
	docker run -ti --rm -p 80:80 -v $(CURDIR)/data:/app/data fastapi-photo


clean:
	rm data/*.jpg


locust-headless:
	cd load_test && locust --headless --users 40 --spawn-rate 1 -H http://127.0.0.1:80

locust:
	cd load_test && locust