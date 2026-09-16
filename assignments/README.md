# Домашні завдання

| № | Тема | Звіт | Файли проєкту |
|---|------|------|---------------|
| 1 | Робоче середовище, пошук компонента | [README](homework_01/README.md) | — |
| 2 | Основні поняття в електроніці | [README](homework_02/README.md) | LTspice: [`homework_02/`](homework_02/) |
| 3 | Компонентна база: пасивні та активні компоненти | [README](homework_03/README.md) | — |
| 4 | Аналогова схемотехніка. Симуляції схем | [README](homework_04/README.md) | LTspice: [`homework_04/`](homework_04/) |
| 5 | Цифрова схемотехніка. Симуляції схем | [README](homework_05/README.md) | LTspice, розрахунок ЦАП (`.xlsx`) |
| 6 | Інтерфейс KiCad та створення проєкту | [README](homework_06/README.md) | [`inverter.kicad_sch`](../motor-drive-controller/hardware/kicad/inverter.kicad_sch) |
| 7 | Архітектура MCU та системи живлення | [README](homework_07/README.md) | [`mcu.kicad_sch`](../motor-drive-controller/hardware/kicad/mcu.kicad_sch), [`.ioc`](../motor-drive-controller/firmware/motor-drive-controller.ioc) |

ДЗ 1–7 перенесені з `.docx` (pandoc) без змін змісту. Починаючи з ДЗ 6 схеми
живуть у проєкті [`motor-drive-controller`](../motor-drive-controller/), а стан
на момент здачі фіксується тегом `hwNN`.

Новий звіт: `cp -r assignments/TEMPLATE assignments/homework_NN`,
`.docx` для сайту: `make report HW=NN`.
