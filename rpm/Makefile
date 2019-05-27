NAME    := python2-pyosmkit
SPEC    ?= $(NAME).spec
DOCKER  ?= 1
VER     := $(shell awk '/Version:/ {print $$2}' $(SPEC))
ARCHIVE := $(NAME)-$(VER).tar.gz
USERID  := $(shell id -u)
IMAGE   := builder-centos7_pyosmkit

ifeq ($(DOCKER),1)
CMD_PREFIX := docker run --rm -it -v $(PWD):/host:ro -v $(HOME)/rpmbuild:/home/builder/rpmbuild:rw $(IMAGE)
SPEC       := /host/$(SPEC)
endif

.PHONY: rpm clean

$(HOME)/rpmbuild:
	mkdir -p $@

$(HOME)/rpmbuild/SOURCES:
	$(CMD_PREFIX) rpmdev-setuptree

$(HOME)/rpmbuild/SOURCES/$(ARCHIVE): $(HOME)/rpmbuild $(HOME)/rpmbuild/SOURCES
	$(CMD_PREFIX) spectool -R -g $(SPEC)

rpm: $(HOME)/rpmbuild/SOURCES/$(ARCHIVE)
	$(CMD_PREFIX) rpmbuild -ba $(SPEC)

clean:
	-rm $(ARCHIVE)

# docker targets
.PHONY: docker-image

docker-image:
	docker build --build-arg=USERID=$(USERID) -t $(IMAGE) .
