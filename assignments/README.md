# Домашні завдання

| № | Тема | Звіт | Файли проєкту | Здача |
|---|------|------|---------------|-------|
| 1 | Робоче середовище, пошук компонента | [README](homework_01/README.md) | — | [hw01](https://github.com/anhro/hardware-development/releases/tag/hw01) |
| 2 | Основні поняття в електроніці | [README](homework_02/README.md) | LTspice: [`homework_02/`](homework_02/) | [hw02](https://github.com/anhro/hardware-development/releases/tag/hw02) |
| 3 | Компонентна база: пасивні та активні компоненти | [README](homework_03/README.md) | — | [hw03](https://github.com/anhro/hardware-development/releases/tag/hw03) |
| 4 | Аналогова схемотехніка. Симуляції схем | [README](homework_04/README.md) | LTspice: [`homework_04/`](homework_04/) | [hw04](https://github.com/anhro/hardware-development/releases/tag/hw04) |
| 5 | Цифрова схемотехніка. Симуляції схем | [README](homework_05/README.md) | LTspice, розрахунок ЦАП (`.xlsx`) | [hw05](https://github.com/anhro/hardware-development/releases/tag/hw05) |
| 6 | Інтерфейс KiCad та створення проєкту | [README](homework_06/README.md) | [`inverter.kicad_sch`](../motor-drive-controller/hardware/kicad/inverter.kicad_sch) | [hw06](https://github.com/anhro/hardware-development/releases/tag/hw06) |
| 7 | Архітектура MCU та системи живлення | [README](homework_07/README.md) | [`mcu.kicad_sch`](../motor-drive-controller/hardware/kicad/mcu.kicad_sch), [`.ioc`](../motor-drive-controller/firmware/motor-drive-controller.ioc) | [hw07](https://github.com/anhro/hardware-development/releases/tag/hw07) |
| 8 | Електричні двигуни. Принципи роботи і керування | [README](homework_08/README.md) | [`gate-driver.kicad_sch`](../motor-drive-controller/hardware/kicad/gate-driver.kicad_sch), [`mcu.kicad_sch`](../motor-drive-controller/hardware/kicad/mcu.kicad_sch), [`.ioc`](../motor-drive-controller/firmware/motor-drive-controller.ioc) | [PR #1](https://github.com/anhro/hardware-development/pull/1) |

**Здача:** Release `hwNN` — зафіксований стан на момент здачі з готовими файлами
(звіт `.docx`, схема PDF, BOM); PR — завдання на перевірці. Після прийняття PR
зливається в `master` і позначається тегом `hwNN` (див. [`docs/workflow.md`](../docs/workflow.md)).

ДЗ 1–7 перенесені з `.docx` (pandoc) без змін змісту. Починаючи з ДЗ 6 схеми
живуть у проєкті [`motor-drive-controller`](../motor-drive-controller/).
Починаючи з ДЗ 8 кожне завдання здається через Pull Request; у папці завдання,
крім звіту, лежать опис PR (`pull-request.md`) і перевірка за чеклістом
(`checklist.md`).

Новий звіт: `cp -r assignments/TEMPLATE assignments/homework_NN`,
`.docx` для сайту: `make report HW=NN`.
