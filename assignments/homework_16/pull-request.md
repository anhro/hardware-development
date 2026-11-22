## Завдання

Підготовка файлів для виробництва:
- підготувати виробничі файли проєкту: Gerber-файли і файл свердління;
- оформити тестове замовлення друкованої плати на JLCPCB для перевірки файлів, без оплати.

**Звіт по 16 домашньому завданню:** [`assignments/homework_16/README.md`](../blob/hw16/assignments/homework_16/README.md).

## Що зроблено

Виробничі файли готові й перевірені скриптом, у KiCad Gerber Viewer і в Gerber Viewer JLCPCB.
Тестове замовлення оформлено: **$29.90** за 5 плат, у кошику, не оплачено. Зауважень від
сервісу немає.

![Gerber у переглядачі JLCPCB](../blob/hw16/assignments/homework_16/images/JLCPCB-viewer.png?raw=true)

**1. Перевірка під можливості JLCPCB.** Правила плати порівняно з JLCPCB Capabilities
(4 шари, 1 oz). Плата вже відповідала. Правила DRC зроблено суворішими, щоб ловили
порушення надалі:

| Правило | Було | Стало |
|---------|------|-------|
| Мін. кільце via | 0.1 мм | 0.15 мм (абсолютний мінімум JLCPCB) |
| NPTH | загальний мінімум 0.3 мм | `jlc_npth_min_hole`: ≥ 0.5 мм |
| `hole_to_hole` | warning | error |
| Зазор класів Default, KELVIN_LINE, Supply | 0.15 мм | 0.2 мм (як мінімум плати) |
| Мін. перемичка маски | 0.1 мм | 0: KiCad більше не зливає вікна маски в Gerber |

Покриття — HASL with lead, найдешевше. Найменший крок на платі 0.5 мм.

**2. Маркування.** На B.SilkS, бо низ плати вільний: `${TITLE}` і `v${REVISION} ${ISSUE_DATE}`
з title block, дзеркальні.

**3–4. Gerber і drill.**

| Файли | Налаштування |
|-------|--------------|
| 11 Gerber + `.gbrjob` | Protel-розширення, без X2, 4.6 мм, шовкографія обрізана маскою |
| `motor-drive-controller.drl` | Excellon, мм, absolute, decimal. PTH (691) і NPTH (6, `NonPlated`) в одному файлі, без карти |

**5. Автоматизація — `make fab`.**

```
build/hardware/manufacturing/
├── gerber/                          Gerber і .drl
├── assembly/                        BOM і позиції SMD-компонентів
└── motor-drive-controller-fab.zip   архів для підприємства
```

- Скрипт повторює ручний експорт до рядка. Виняток — перезаливка полігонів F.Cu.
- `--board-plot-params` у kicad-cli 10.0.5 ігнорує вимкнений X2, тому опції задано явно.
- CI публікує zip в артефакти PR і в Release за тегом.

**6. Перевірка Gerber.** У KiCad Gerber Viewer:
- контур замкнений, 70 × 113 мм;
- отвори на падах;
- In1/In2 — суцільна земля;
- вікна маски лише над падами, via закриті;
- шовкографія не заходить на пади;
- паста лише на SMD.

Кількість і діаметри отворів у `.drl` збігаються з Board Statistics.

**7. Замовлення на JLCPCB.**

| Параметр | Вибрано |
|----------|---------|
| Плата | FR-4 TG135, 4 шари, 70 × 113 мм, 1.6 мм, 5 шт. |
| Мідь | 1 oz зовні / 0.5 oz всередині |
| Покриття / маска | HASL with lead / зелена, шовкографія біла |
| Via Covering | **Plugged**: Tented для 4 шарів більше недоступний, Plugged безкоштовний |
| Mark on PCB | **Remove Mark** |
| Specify Stackup | **JLC04161H-3313**, як у стеку KiCad |
| Вартість | $4.90 плата + $25.00 engineering fee = **$29.90**; DHL $91.33 |

## Де дивитися

- **Звіт:** [`assignments/homework_16/README.md`](../blob/hw16/assignments/homework_16/README.md)
- **Інженерні рішення:** [`design-notes.md`](../blob/hw16/motor-drive-controller/docs/design-notes.md), розділ «ДЗ 16»
- **Плата:** [`motor-drive-controller.kicad_pcb`](../blob/hw16/motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_pcb), правила DRC — [`motor-drive-controller.kicad_dru`](../blob/hw16/motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_dru)
- **Експорт для виробництва:** [`tools/kicad-outputs.sh`](../blob/hw16/tools/kicad-outputs.sh), [`Makefile`](../blob/hw16/Makefile)
- **Перевірка за чеклістом:** [`checklist.md`](../blob/hw16/assignments/homework_16/checklist.md)
- **Архів для заводу (`motor-drive-controller-fab.zip`), BOM, позиції, схема PDF, звіт ERC, звіт `.docx`:** вкладка **Checks → CI → Artifacts**.

Локально:
- `make fab` — Gerber, drill, BOM, позиції й zip у `build/hardware/manufacturing/`;
- `make hardware` — те саме, а також ERC і схема PDF;
- `make report HW=16` — звіт у `.docx`.

## Стан ERC/DRC і відкриті питання

ERC: **0 порушень**. DRC: **0 порушень, 0 нерозведених**, 0 розбіжностей зі схемою.

Відкриті питання:
- **Один drill-файл для PTH і NPTH.** Неметалізовані отвори позначені лише атрибутом.
  Якщо завод його проігнорує, 6 отворів M3 металізують. Для цієї плати це некритично.
- З ДЗ 15: пайка XT1 і J5, нагрів VD3 — перевірити на прототипі.

## Чекліст

Детальна перевірка кожного пункту — у [`checklist.md`](../blob/hw16/assignments/homework_16/checklist.md).

**Звіт**
- [x] Звіт у Markdown, зображення в `images/`
- [x] Рішення внесені в `design-notes.md`
- [x] Документація проєкту оновлена

**Завдання**
- [x] Gerber-файли: 11 шарів + job-файл
- [x] Файл свердління: 691 PTH + 6 NPTH, збігається з Board Statistics
- [x] Тестове замовлення JLCPCB без оплати, зауважень немає

**Плата (PCB)**
- [x] DRC 0 / 0 / 0
- [x] Технологічні параметри в межах JLCPCB, правила DRC під JLCPCB
- [x] Маркування на B.SilkS

**Схема (KiCad)**
- [x] ERC: 0 порушень
- [x] BOM: 37 рядків, 89 компонентів

**Репозиторій**
- [x] `make fab`, CI-артефакт і Release з архівом
- [x] Немає абсолютних шляхів і згенерованих файлів
