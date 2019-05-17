IMAGE   := builder-centos7_pyosmkit
NAME    := python2-pyosmkit
USERID  := $(shell id -u)

VER     := $(shell awk '/Version:/ {print $$2}' $(NAME).spec)
ARCHIVE := $(NAME)-$(VER).tar.gz

DOCKER_RUN_OPTS = --rm -it -v $(PWD):/host -v $(HOME)/rpmbuild:/home/builder/rpmbuild

.PHONY: package clean

$(HOME)/rpmbuild:
	mkdir -p $@

$(HOME)/rpmbuild/SOURCES/$(ARCHIVE):
	spectool -R -g $(NAME).spec

package:
	rpmbuild -ba $(NAME).spec

clean:
	-rm $(ARCHIVE)

# docker targets
.PHONY: docker-shell docker-package docker-image docker-source

docker-source: $(HOME)/rpmbuild
	docker run $(DOCKER_RUN_OPTS) $(IMAGE) spectool -R -g /host/$(NAME).spec

docker-shell: $(HOME)/rpmbuild
	docker run $(DOCKER_RUN_OPTS) --user root $(IMAGE) /bin/bash

docker-image:
	docker build --build-arg=USERID=$(USERID) -t $(IMAGE) .

docker-package: $(HOME)/rpmbuild docker-source
	docker run $(DOCKER_RUN_OPTS) $(IMAGE) rpmbuild -ba /host/$(NAME).spec
