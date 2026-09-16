# Єдина точка входу для рутинних дій. `make` або `make help` — перелік команд.
SHELL := /bin/bash
.DEFAULT_GOAL := help

PROJECT      := motor-drive-controller
KICAD_DIR    := $(PROJECT)/hardware/kicad
ASSIGNMENTS  := $(sort $(wildcard assignments/homework_*))

.PHONY: help setup datasheets datasheets-check hardware erc report reports firmware clean

help: ## Показати цей список
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*## "}{printf "  make %-18s %s\n", $$1, $$2}'
	@echo
	@echo "  Приклад: make report HW=07"

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

firmware: ## Зібрати прошивку (потрібні cmake, ninja, arm-none-eabi-gcc)
	cd $(PROJECT)/firmware && cmake --preset Debug && cmake --build --preset Debug

clean: ## Видалити build/
	rm -rf build
