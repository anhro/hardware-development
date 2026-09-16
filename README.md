# Hardware Development: від схеми до прототипу

Навчальний репозиторій курсу: домашні завдання та наскрізний проєкт —
**контролер BLDC-двигуна** на STM32F405 (трифазний інвертор 12 В / 14 А).

| Що | Де |
|----|----|
| Звіти домашніх завдань | [`assignments/`](assignments/) |
| Проєкт курсу: схема, прошивка, документація | [`motor-drive-controller/`](motor-drive-controller/) |
| Як переглянути роботу (для викладача) | [`docs/reviewer-guide.md`](docs/reviewer-guide.md) |
| Процес роботи, інструменти, правила репозиторію | [`docs/workflow.md`](docs/workflow.md) |

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
| `make report HW=07` | звіт ДЗ 7 у `.docx` → `build/reports/` |
| `make firmware` | збірка прошивки (CMake + arm-none-eabi-gcc) |

Потрібно: `git`, `make`, `python3`; для звітів — `pandoc` **або** Docker;
для схем — KiCad 10 **або** Docker.

## Структура

```
.
├── assignments/                 # ДЗ: README.md (звіт) + images/ + симуляції *.asc
├── motor-drive-controller/
│   ├── docs/                    # архітектура, інженерні рішення
│   ├── hardware/
│   │   ├── kicad/               # проєкт KiCad + lib/parts (символи, footprints, 3D)
│   │   ├── simulations/ltspice/ # симуляції вузлів
│   │   └── datasheets/          # лише маніфест datasheets.txt, PDF — локально
│   └── firmware/                # STM32CubeMX (.ioc) + код
├── docs/                        # процеси та інструкції
├── tools/                       # скрипти автоматизації
├── .github/workflows/ci.yml     # CI: схема/BOM/звіти/прошивка, релізи за тегами
└── Makefile
```
