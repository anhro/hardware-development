# Єдина точка входу для рутинних дій. `make` або `make help` — перелік команд.
SHELL := /bin/bash
.DEFAULT_GOAL := help

# Проєкт: ім'я папки в корені або в prototypes/ — make hardware PROJECT=stepper-motor
PROJECT      := motor-drive-controller
PROJECT_DIR  := $(or $(firstword $(wildcard $(PROJECT)/ prototypes/$(PROJECT)/)),$(error Проєкт '$(PROJECT)' не знайдено ні в корені, ні в prototypes/))
KICAD_DIR    := $(PROJECT_DIR)hardware/kicad
ARDUINO_CLI  ?= arduino-cli
ASSIGNMENTS  := $(sort $(wildcard assignments/homework_*))

.PHONY: help setup datasheets datasheets-check hardware erc report reports firmware clean

help: ## Показати цей список
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*## "}{printf "  make %-18s %s\n", $$1, $$2}'
	@echo
	@echo "  Приклад: make report HW=07"
	@echo "           make hardware PROJECT=stepper-motor"

setup: ## Після клонування: налаштувати git і завантажити datasheets
	git config diff.ltspice.textconv tools/ltspice-textconv.sh
	$(MAKE) datasheets

datasheets: ## Завантажити відсутні datasheets з маніфестів datasheets.txt
	python3 tools/fetch-datasheets.py

datasheets-check: ## Показати відсутні та не описані в маніфесті datasheets
	python3 tools/fetch-datasheets.py --check

hardware: ## KiCad: ERC, схема PDF, BOM -> build/hardware/
	tools/kicad-outputs.sh $(KICAD_DIR)

erc: ## KiCad: суворий ERC — помилка, якщо є порушення рівня error
	ERC_STRICT=1 tools/kicad-outputs.sh $(KICAD_DIR)

report: ## Звіт ДЗ у .docx: make report HW=07 -> build/reports/
	@test -n "$(HW)" || { echo "Вкажіть номер: make report HW=07"; exit 1; }
	tools/build-report.sh assignments/homework_$(HW)

reports: ## Усі звіти ДЗ у .docx
	@for d in $(ASSIGNMENTS); do tools/build-report.sh $$d || exit 1; done

firmware: ## Зібрати прошивку: CMake (STM32) або Arduino (sketch.yaml, потрібен arduino-cli)
ifneq ($(wildcard $(PROJECT_DIR)firmware/sketch.yaml),)
	cd $(PROJECT_DIR)firmware && $(ARDUINO_CLI) compile --build-path build .
else
	cd $(PROJECT_DIR)firmware && cmake --preset Debug && cmake --build --preset Debug
endif

clean: ## Видалити build/
	rm -rf build
