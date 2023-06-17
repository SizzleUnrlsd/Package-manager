IMAGE_NAME = server
CONTAINER_NAME = server_package

all:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d -p 8080:8080 --name $(CONTAINER_NAME) $(IMAGE_NAME)

it:
	docker exec -it $(CONTAINER_NAME) /bin/bash

data_cp:
	docker cp $(CONTAINER_NAME):/data/data.json ./data.json

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
