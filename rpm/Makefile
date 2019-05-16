IMAGE   := builder-centos7_pyosmkit
NAME    := python2-pyosmkit
USERID  := $(shell id -u)

DOCKER_RUN_OPTS = --name $(NAME) -it -v $(PWD):/host

.PHONY: shell package image clean

shell:
	docker run $(DOCKER_RUN_OPTS) $(IMAGE) /bin/bash

image:
	docker build --build-arg=USERID=$(USERID) -t $(IMAGE) .

package:
	docker run $(DOCKER_RUN_OPTS) $(IMAGE) /host/build_$(NAME).sh /host/$(NAME).spec
	docker cp -a $(NAME):/home/builder/rpmbuild/RPMS ./
	docker rm $(NAME)

clean:
	docker rm $(NAME)
