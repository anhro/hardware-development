# Процес роботи та правила репозиторію

## Принципи

1. **У git — лише джерела.** Схеми, код, Markdown, маніфести. Усе, що можна
   згенерувати (PDF, BOM, `.docx`, прошивка) чи завантажити (datasheets), —
   генерує `make`/CI і в git не потрапляє (див. [`.gitignore`](../.gitignore)).
2. **Без дублікатів.** Одна річ — одне місце. Звіт посилається на файли
   проєкту, а не копіює їх. Попередні версії — це історія git і теги, а не
   папки `old/`, `v2/`, `*_old`.
3. **Відтворюваність.** Після `git clone && make setup` проєкт відкривається й
   збирається на будь-якій машині: жодних абсолютних шляхів (`/home/...`,
   `~/Downloads`), усі бібліотеки — в репозиторії з відносними шляхами `${KIPRJMOD}`.
4. **Зображення — лише там, де немає текстового джерела** (скріншоти, графіки
   симуляцій, фото). Схеми для звіту не скріншотити вручну — PDF генерує CI.

## Цикл домашнього завдання

```bash
git switch master && git pull
git switch -c hw08                     # гілка на завдання

# ... робота в KiCad / LTspice / CubeMX, звіт у assignments/homework_08/README.md
make hardware                          # перевірити ERC, подивитися PDF
make report HW=08                      # за потреби — .docx для навчального сайту

git add -A && git commit -m "hw08: ..." # дрібні осмислені коміти
git push -u origin hw08                # відкрити Pull Request на GitHub
```

Після перевірки: **Merge** PR у `master`, потім зафіксувати версію тегом —
CI сам створить Release зі звітом `.docx`, PDF схеми та BOM:

```bash
git switch master && git pull
git tag -a hw08 -m "Заняття 8: ..." && git push origin hw08
```

На навчальний сайт — посилання на PR або Release (і, якщо вимагається, `.docx`
з релізу).

Новий звіт починати з шаблону: `cp -r assignments/TEMPLATE assignments/homework_08`.

## Інструменти

| Задача | Інструмент | Формат у git | Коментар |
|--------|-----------|--------------|----------|
| Схема і плата | **KiCad 10** | `.kicad_sch/.kicad_pcb/.kicad_pro` (текст) | Найкращий вибір для git: текстові файли, `kicad-cli` для CI. Залишаємо. |
| Симуляція | **LTspice 24** | `.asc` (+ `.plt`) | Стандарт індустрії, моделі ADI. `.raw/.log/.net` — генеруються, ігноруються. Альтернатива для CI — ngspice (KiCad має вбудований), але переходити не обов'язково. |
| Конфігурація MCU | **STM32CubeMX** | `.ioc` (текст) | Єдине джерело правди для пінів/периферії. Генерувати **CMake**-проєкт. |
| Код, збірка, налагодження | **VS Code + STM32Cube for VS Code** | `CMakeLists.txt`, `CMakePresets.json` | Офіційне розширення ST; CMake-проєкт збирається й у CI. Замінює STM32CubeIDE (Eclipse, багато службових файлів). |
| Документи | **Markdown** (VS Code) | `.md` + `images/*.png` | GitHub показує одразу; `.docx` генерується pandoc'ом. |
| Діаграми | **Mermaid** у Markdown або **draw.io** (`*.drawio.svg`) | текст / SVG | Mermaid рендериться GitHub'ом; `.drawio.svg` редагується в VS Code і водночас є картинкою. |
| Розрахунки | Markdown з формулами або **Python**-скрипт | `.md` / `.py` | Замість `.xlsx`: diff видно, результат відтворюється. |
| Datasheets | `datasheets.txt` + `make datasheets` | маніфест | PDF не зберігаються. |

VS Code запропонує рекомендовані розширення з [`.vscode/extensions.json`](../.vscode/extensions.json).

## Компоненти KiCad

Кожна нестандартна деталь — окрема папка
`motor-drive-controller/hardware/kicad/lib/parts/<PART>/`:

```
lib/parts/AOD4184A/
├── AOD4184A.kicad_sym        # символ
├── AOD4184A.pretty/*.kicad_mod
└── AOD4184A.step             # 3D-модель (за наявності)
```

Додати нову деталь (наприклад, завантажену з SnapEDA / Ultra Librarian):

1. Розпакувати в `lib/parts/<PART>/` за схемою вище.
2. KiCad → *Preferences → Manage Symbol/Footprint Libraries → Project Specific*:
   додати з nickname `<PART>` і шляхом `${KIPRJMOD}/lib/parts/<PART>/...`.
3. Додати datasheet у `hardware/datasheets/datasheets.txt`.

Не додавати бібліотеки в **Global Libraries** і не посилатися на `~/Downloads` —
інакше проєкт не відкриється на іншому комп'ютері.

## Datasheets

```
# hardware/datasheets/datasheets.txt
AOD4184A.pdf   https://www.aosmd.com/res/datasheets/AOD4184A.pdf
```

`make datasheets` завантажує відсутні; `make datasheets-check` показує PDF,
що лежать у папці, але не описані в маніфесті. Деякі сайти (st.com, molex.com)
блокують автоматичні завантаження — тоді скрипт виведе посилання для ручного
завантаження.

## Великі файли

Git LFS наразі не потрібен: бінарних файлів мало і вони не змінюються.
Якщо з'являться фото/відео прототипу понад кілька МБ — стискати (JPEG/WebP)
або вмикати LFS для `*.jpg`, `*.mp4`.
