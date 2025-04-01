BASEDIR=$(CURDIR)
CURRENT_UID := $(shell id -u)
CURRENT_UID_OPT=--user $(CURRENT_UID)

build:
	docker build --no-cache -t danielsteinke/fortanix-demo ./

run:
	docker run -v $(CURDIR):$(CURDIR) -w $(CURDIR) \
		$(CURRENT_UID_OPT) \
		danielsteinke/fortanix-demo make python-run

python-run:
	python ./main.py


.PHONY: build run python-run
