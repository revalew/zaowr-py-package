.PHONY: all clean bump-version build upload-prod upload-testpypi

all: clean bump-version build upload-prod upload-testpypi

VERSION_FILE=./src/zaowr_polsl_kisiel/__init__.py
VERSION=$(shell python3 -c 'import re; f=open("$(VERSION_FILE)"); print(re.search(r"__version__ = \"(.*?)\"", f.read()).group(1))')

clean:
	rm -rf dist/ **/*.egg-info

build:
	python3 -m build

upload-prod:
	@if [ -d "dist" ]; then \
		python3 -m twine upload dist/*; \
	else \
		echo "Error: dist directory does not exist. Run 'make build' first."; \
		exit 1; \
	fi

upload-testpypi:
	@if [ -d "dist" ]; then \
		python3 -m twine upload --repository testpypi dist/*; \
	else \
		echo "Error: dist directory does not exist. Run 'make build' first."; \
		exit 1; \
	fi

bump-version:
	@echo "Current version: $(VERSION)"
	@read -p "Choose version type to bump (major, minor, patch -> 'major.minor.patch'): " versiontype; \
	case $$versiontype in \
		patch) newversion=$$(echo $(VERSION) | awk -F. '{printf "%d.%d.%d", $$1, $$2, $$3+1}');; \
		minor) newversion=$$(echo $(VERSION) | awk -F. '{printf "%d.%d.%d", $$1, $$2+1, 0}');; \
		major) newversion=$$(echo $(VERSION) | awk -F. '{printf "%d.%d.%d", $$1+1, 0, 0}');; \
		*) echo "Invalid option! Please choose either major, minor, or patch."; exit 1;; \
	esac; \
	sed -i "s/__version__ = \"$(VERSION)\"/__version__ = \"$$newversion\"/" $(VERSION_FILE); \
	echo "Version updated to $$newversion"; \
	read -p "Enter commit message: " commitmsg; \
	git add .; \
	git commit -am "$$commitmsg (version $$newversion)"; \
	git tag -a v$$newversion -m "$$commitmsg" -f; \
	git push --follow-tags
