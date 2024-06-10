TRAGET = $(word 1, $(subst ==, ,$(arg)))
VERSION = $(word 2, $(subst ==, ,$(arg)))

.PHONY: all run build

all: build run

build:
	if [ -z "$(TRAGET)" ] || [ -z "$(VERSION)" ]; then \
		echo "Package and version must be specified"; \
	exit 1; \
	fi
	@echo "Target Package: $(TRAGET)"
	@echo "Target Version: $(VERSION)"

	docker build --build-arg TARGET=$(TRAGET) \
		--build-arg VERSION=$(VERSION) \
		-t pcfuzzer:$(TRAGET)-$(VERSION) .

run:
	docker run -it -d \
		-v $(PWD)/result:/result \
		--name pcfuzzer-$(TRAGET)-$(VERSION) \
		pcfuzzer:$(TRAGET)-$(VERSION)
