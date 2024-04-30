# Make file for Geminal project
SHELL=/bin/bash

# ANSI color codes
RED=$(shell tput -Txterm setaf 1)
GREEN=$(shell tput -Txterm setaf 2)
YELLOW=$(shell tput -Txterm setaf 3)
BLUE=$(shell tput -Txterm setaf 4)
RESET=$(shell tput -Txterm sgr0)

# Build Geminal from source code.
build:
	@$(MAKE) -s check-to-build
	@echo
	@echo "$(BLUE)Building Geminal from source code...$(RESET)"
	@rm -rf dist/
	@poetry build
	@pip install dist/geminal-*.tar.gz
	@echo "$(GREEN)[✓] Geminal built successfully.$(RESET)"

# Check dependencies to build Geminal
check-to-build:
	@echo "$(BLUE)Checking dependencies...$(RESET)"
	@$(MAKE) -s check-os
	@$(MAKE) -s check-pip
	@$(MAKE) -s check-python
	@$(MAKE) -s check-poetry
	@echo "$(GREEN)[✓] Dependencies checked successfully.$(RESET)"

# Install Geminal
install:
	@$(MAKE) -s check-to-install
	@echo
	@echo "$(BLUE)Installing Geminal...$(RESET)"
	@pip install dist/geminal-*.tar.gz
	@echo "$(GREEN)[✓] Geminal installed successfully.$(RESET)"

# Check dependencies to install Geminal
check-to-install:
	@echo "$(BLUE)Checking dependencies...$(RESET)"
	@$(MAKE) -s check-os
	@$(MAKE) -s check-pip
	@$(MAKE) -s check-python
	@echo "$(GREEN)[✓] Dependencies checked successfully.$(RESET)"

# Dockerize Geminal as an image
dockerize:
	@$(MAKE) -s check-to-dockerize
	@echo
	@echo "$(BLUE)Dockerizing Geminal...$(RESET)"
	@docker rmi -f geminal
	@docker buildx build --build-arg GOOGLE_API_KEY=$(echo "$GOOGLE_API_KEY") -t geminal .
	@echo "$(GREEN)[✓] Geminal dockerized successfully.$(RESET)"
	@echo
	@echo "$(BLUE)[*] Good to know:$(RESET)"
	@echo "$(BLUE)    > To use Geminal from just the created image, run:$(RESET)"
	@echo "$(BLUE)        \`docker run -it --rm --name geminal geminal\`$(RESET)"
	@echo "$(BLUE)    > However, to save time, you can set an alias for this command in your \`.bashrc\` or \`.bash_profile\` file for quick invocation next time.$(RESET)"
	@echo "$(BLUE)      Example: Open a new Terminal window, run \`echo \"alias geminal='docker run -it --rm --name geminal geminal'\" >> ~/.bashrc\`, then restart your Terminal and run \`geminal\`$(RESET)"

# Check dependencies to dockerize Geminal
check-to-dockerize:
	@echo "$(BLUE)Checking dependencies...$(RESET)"
	@$(MAKE) -s check-os
	@$(MAKE) -s check-docker
	@echo "$(GREEN)[✓] Dependencies checked successfully.$(RESET)"

check-os:
	@echo "$(BLUE)  > Checking operation system...$(RESET)"
	@if [ "$(shell uname)" = "Darwin" ]; then \
		echo "$(GREEN)    [✓] MacOS detected.$(RESET)"; \
	elif [ "$(shell uname)" = "Linux" ]; then \
	    echo "$(GREEN)    [✓] Linux detected.$(RESET)"; \
    elif [ "$$(uname -r | grep -i microsoft))" ]; then \
      	echo "$(GREEN)    [✓] Windows Subsystem for Linux detected.$(RESET)"; \
    else \
      	echo "$(RED)Unsupported system detected. Please, use macOS, Linux, or Windows Subsystem for Linux (WSL).$(RESET)"; \
    fi

check-pip:
	@echo "$(BLUE)  > Checking Pip installation...$(RESET)"
	@if command -v pip > /dev/null; then \
  		echo "$(GREEN)    [✓] OK.$(RESET)"; \
  	else \
  	  	echo "$(RED)    [✗] Pip is not installed. Please, install it to continue.$(RESET)"; \
  	fi

check-python:
	@echo "$(BLUE)  > Checking Python 3.10 installation...$(RESET)"
	@if command -v python3.10 > /dev/null; then \
  		echo "$(GREEN)    [✓] OK.$(RESET)"; \
  	else \
  	  	echo "$(RED)    [✗] Python 3.10 is not installed. Please, install it to continue.$(RESET)"; \
  	  	exit 0; \
  	fi

check-poetry:
	@echo "$(BLUE)  > Checking Poetry installation...$(RESET)"
	@if command -v poetry > /dev/null; then \
  		echo "$(GREEN)    [✓] OK.$(RESET)"; \
  	else \
  	  	echo "$(RED)    [✗] Poetry is not installed. Please, install it to continue.$(RESET)"; \
  	fi

check-docker:
	@echo "$(BLUE)  > (Optional) Checking Docker installation...$(RESET)"
	@if command -v docker > /dev/null; then \
  		echo "$(GREEN)    [✓] OK.$(RESET)"; \
  	else \
  	  	echo "$(YELLOW)    [!] Docker is not installed. If you want to dockerize this program, please install Docker.$(RESET)"; \
  	fi

# Phony targets
.PHONY: check-os check-python check-pip check-docker check-to-build build check-to-install install check-to-dockerize dockerize
