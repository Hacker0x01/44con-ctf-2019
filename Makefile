CONTAINERS := entrypoint $(wildcard rooms/*)
IMAGES := $(addprefix images/, $(CONTAINERS))

all: images $(IMAGES)

images:
	mkdir images
	mkdir images/rooms

.SECONDEXPANSION:
images/%: % $$(shell find $$* -type f)
	docker build -t $(notdir $<) $<
	@touch $@
	-@DIR=$(dir $(basename $<)); \
	if [ $$DIR == "rooms/" ]; then \
	echo 'Killing existing room instance'; \
	docker kill 1-$(notdir $<) > /dev/null 2>&1; \
	else \
	echo 'Killing entrypoint instance'; \
	docker kill entrypoint_entrypoint_1 > /dev/null 2>&1; \
	fi

.PHONY: clean
clean:
	rm -rf images

.PHONY: start
start: all
	cd entrypoint && docker-compose up -d

.PHONY: ssh
ssh: start
	ssh eldon@localhost -p 2222
