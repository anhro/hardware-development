# Hardware Development: від схеми до прототипу

[![CI](https://github.com/anhro/hardware-development/actions/workflows/ci.yml/badge.svg)](https://github.com/anhro/hardware-development/actions/workflows/ci.yml)

Навчальний репозиторій курсу: домашні завдання та наскрізний проєкт —
**контролер BLDC-двигуна** на STM32F405 (трифазний інвертор 12 В / 14 А).

**Поточний стан:** виконано ДЗ 1–8. Схема: силовий інвертор (AOD4184A),
драйвер затворів DRV8305, MCU STM32F405 з конфігурацією CubeMX; прошивка
збирається в CI. Друкована плата — не розпочата.
Відкриті інженерні питання — у [`design-notes.md`](motor-drive-controller/docs/design-notes.md).

| Що | Де |
|----|----|
| Звіти домашніх завдань і посилання на здачу (Release / PR) | [`assignments/`](assignments/) |
| Проєкт курсу: схема, прошивка, документація | [`motor-drive-controller/`](motor-drive-controller/) |
| Як переглянути роботу (для викладача) | [`docs/reviewer-guide.md`](docs/reviewer-guide.md) |
| Процес роботи, інструменти, правила репозиторію | [`docs/workflow.md`](docs/workflow.md) |
| Релізи (звіт `.docx`, схема PDF, BOM для кожного ДЗ) | [Releases](https://github.com/anhro/hardware-development/releases) |

## Швидкий старт

```bash
git clone https://github.com/anhro/hardware-development.git
cd hardware-development
make setup          # git-налаштування + завантаження datasheets
make help           # усі команди
```

Основні команди:

| Команда | Результат |
|---------|-----------|
| `make datasheets` | завантажує PDF за маніфестами `datasheets.txt` |
| `make hardware` | ERC, схема у PDF, BOM → `build/hardware/` |
| `make report HW=08` | звіт ДЗ 8 у `.docx` → `build/reports/` |
| `make firmware` | збірка прошивки (CMake + arm-none-eabi-gcc) |

Потрібно: `git`, `make`, `python3`; для звітів — `pandoc` **або** Docker;
для схем — KiCad 10 **або** Docker; для прошивки — STM32CubeCLT або
`gcc-arm-none-eabi` + `cmake` + `ninja`. Для VS Code є рекомендовані розширення
(`.vscode/extensions.json`).

## Здача домашнього завдання

```
гілка hwNN → коміти → push → Pull Request (посилання на сайт курсу + .docx)
          → правки в тій самій гілці → Squash and merge → тег hwNN → Release
```

CI перевіряє кожен PR (ERC, схема PDF, BOM, звіти `.docx`, прошивка) і за тегом
`hwNN` створює Release. Для кожного PR у папці завдання ведуться опис
(`pull-request.md`) і перевірка за чеклістом (`checklist.md`); шаблон чекліста —
[`.github/pull_request_template.md`](.github/pull_request_template.md).
Детально — [`docs/workflow.md`](docs/workflow.md).

## Структура

```
.
├── assignments/                 # ДЗ: README.md (звіт) + images/ + симуляції *.asc
│   └── homework_NN/             #   з ДЗ 8 — також pull-request.md, checklist.md
├── motor-drive-controller/
│   ├── docs/                    # архітектура, інженерні рішення
│   ├── hardware/
│   │   ├── kicad/               # проєкт KiCad: листи MCU, Gate Driver, Inverter
│   │   │   └── lib/parts/<PART>/ # символ, <PART>.pretty/ (footprint), 3D
│   │   ├── simulations/ltspice/ # симуляції вузлів
│   │   └── datasheets/          # лише маніфест datasheets.txt, PDF — локально
│   └── firmware/                # STM32CubeMX (.ioc) + CMake-проєкт + HAL
├── docs/                        # процеси та інструкції
├── tools/                       # скрипти автоматизації
├── .github/
│   ├── workflows/ci.yml         # CI: схема/BOM/звіти/прошивка, релізи за тегами
│   └── pull_request_template.md # чекліст PR
└── Makefile
```
