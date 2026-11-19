## Завдання

Електромагнітна сумісність (EMC/EMI):
- закінчити трасування плати;
- залити земляний полігон, зшити (stitching) землі на різних шарах;
- якщо є BT-модуль — зробити виріз полігону землі (cut-out) за datasheet;
- пройти DRC.

**Звіт по 15 домашньому завданню:** [`assignments/homework_15/README.md`](../blob/hw15/assignments/homework_15/README.md).

## Що зроблено

Плата розведена повністю: **DRC — 0 порушень, 0 нерозведених** (на початку — 118), 0 розбіжностей
зі схемою; ERC — 0.

![Шари міді: F.Cu, In1.Cu, In2.Cu, B.Cu](../blob/hw15/assignments/homework_15/images/layers.png?raw=true)

**1. Шари і полігони GND.** Стек сигнал / GND / GND / сигнал:

| Шар | Призначення |
|-----|-------------|
| F.Cu | компоненти, сигнали, силові полігони ДЗ 13, заливка GND |
| In1.Cu | суцільний GND, доріжки заборонені правилом `in1_gnd_no_tracks` |
| In2.Cu | суцільний GND, без доріжок |
| B.Cu | сигнали, заливка GND |

- GND — пріоритет 0, силові полігони — 1–6; зазор GND до силової міді 1 мм.
- Силові GND-пади (шунти, C25/C29/C32, XT1) і via термопада U2 — суцільно, без термобар'єра.
- Землю не ділю на AGND/PGND: струм двигуна повертається від шунтів по In1/In2/B.Cu прямо під
  силовим каскадом до XT1 і не проходить під MCU.

**2. Трасування.** Сигнали — лише на F.Cu і B.Cu (доріжка на внутрішньому шарі прорізала б
опорну землю).

| Вузол | Що зроблено |
|-------|-------------|
| Драйвер U2 | конденсатори підкачки заряду й живлення впритул до виводів (DVDD 8.6 → 2.1 мм, CP1 9–10 → 3.6/5.2 мм, VCPH 12.4 → 4.3 мм), усе на F.Cu без via; додано C45 1 мкФ на VREF |
| PWM, SPI, керування | 22–27 мм; порядок виводів INH/INL на U1 і U2 зворотний — перехрестя короткими ділянками на B.Cu |
| `ANALOG.SO1–3` | SO1 ↔ SO3 поміняно на входах АЦП → усі три по F.Cu без via; TP4–TP6 на самій трасі |
| MCU | C13 (NRST) 40 → 4 мм, C7 (VDDA) 12.9 → 4.1 мм, C10 (VCAP_2) 6.5 → 4.3 мм; кварц на F.Cu без via |
| HALL, TEMP | по B.Cu, відсунуті від краю плати (язик GND уздовж краю 81 мм прибрано) |

**3. Stitching.** 549 via GND:
- біля кожного GND-пада SMD (≤ 1 мм від краю пада);
- 8 × 0.8/0.4 на GND-пад кожного шунта (≈ 2.4 А на via), по 3 біля C25/C29/C32 і TVS VD1;
- сітка 5 мм у заливках і 53 via по периметру. Крок 5 мм: для фронтів PWM ≲ 300 МГц λ/20 ≈ 25 мм;
  спроба з кроком 1 мм (2343 via) нічого не давала й порушувала hole-to-hole;
- via GND біля сигнальних via (≤ 2–3 мм) — зворотний струм переходить з In1 на In2.

**4. BT cut-out** — не застосовно, радіомодуля немає.

**5. Перевірки.**

| Перевірка | Результат |
|-----------|-----------|
| DRC (з перезаливкою полігонів) | 0 порушень, 0 нерозведених, 0 розбіжностей зі схемою |
| ERC | 0 / 0 |
| Board Statistics | 623 наскрізних via; 2 мікровія (не ловить DRC) знайдено й виправлено на Through |
| `check-parallel.py` | Kelvin/CS ↔ затвори, фази, PWM — зазор < 2 мм відсутній |
| `check-gnd-tongues.py` | кожен шматок заливки > 1 мм² має via; In1/In2 — по одному шматку |

**Зміни схеми, прошивки й налаштувань плати:**

| Що | Було | Стало | Чому |
|----|------|-------|------|
| VREG (VREF) DRV8305N | R9 330 Ом від VDDA, без конденсатора | + C45 1 мкФ біля виводу 48 | фільтр опорної напруги підсилювачів струму ≈ 480 Гц |
| Входи АЦП | SO1 → PC1, SO3 → PC3 | SO1 → PC3 (ADC3_IN13), SO3 → PC1 (ADC1_IN11) | траса SO без перехресть і via; канали АЦП ті самі |
| Мін. зазор / доріжка | 0.1 / 0.15 мм | 0.2 / 0.2 мм | дешевше у виробництві |

## Де дивитися

- **Звіт:** [`assignments/homework_15/README.md`](../blob/hw15/assignments/homework_15/README.md)
- **Інженерні рішення та відкриті питання:** [`design-notes.md`](../blob/hw15/motor-drive-controller/docs/design-notes.md)
- **Плата:** [`motor-drive-controller.kicad_pcb`](../blob/hw15/motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_pcb), правила DRC — [`motor-drive-controller.kicad_dru`](../blob/hw15/motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_dru)
- **Схеми:** [`gate-driver.kicad_sch`](../blob/hw15/motor-drive-controller/hardware/kicad/gate-driver.kicad_sch) (C45), [`mcu.kicad_sch`](../blob/hw15/motor-drive-controller/hardware/kicad/mcu.kicad_sch) (SO1 ↔ SO3)
- **Скрипти перевірки:** [`tools/check-parallel.py`](../blob/hw15/tools/check-parallel.py), [`tools/check-gnd-tongues.py`](../blob/hw15/tools/check-gnd-tongues.py)
- **Перевірка за чеклістом:** [`checklist.md`](../blob/hw15/assignments/homework_15/checklist.md)
- **Схема у PDF, BOM, звіт ERC, звіт `.docx`:** вкладка **Checks → CI → Artifacts**.

Локально:
- `make hardware` — ERC + PDF + BOM;
- `make report HW=15` — звіт у `.docx`;
- `tools/check-gnd-tongues.py motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_pcb --refill` — язики заливки GND.

## Стан ERC/DRC і відкриті питання

ERC: **0 error, 0 warning**. DRC: **0 порушень, 0 нерозведених**, 0 розбіжностей зі схемою.

Відкриті питання:
- **Пайка XT1 і J5** (з ДЗ 13) — пади під'єднані суцільно, перевірити на прототипі.
- **Щілина 12.5 мм в In1/In2 під J5** — злиті антипади виводів роз'єму; сигнали над нею не йдуть — прийнято.
- **Прошивка:** після обміну SO1 ↔ SO3 фазу A міряє ADC3, фазу C — ADC1.

## Чекліст

Детальна перевірка кожного пункту — у [`checklist.md`](../blob/hw15/assignments/homework_15/checklist.md).

**Звіт**
- [x] Звіт у Markdown, зображення в `images/`
- [x] Рішення внесені в `design-notes.md`
- [x] Документація проєкту (README, `architecture.md`) оновлена

**Завдання**
- [x] Трасування закінчено: 0 нерозведених
- [x] Полігони GND на всіх шарах, In1/In2 суцільні
- [x] Stitching: 549 via GND, крок 5 мм, периметр, via біля падів і сигнальних via
- [x] BT cut-out — не застосовно
- [x] DRC: 0 порушень

**Схема (KiCad)**
- [x] ERC: 0 error, 0 warning
- [x] C45 на VREF, SO1 ↔ SO3
- [x] BOM: 37 рядків, 89 компонентів

**Плата (PCB)**
- [x] DRC 0 / 0, без мікровія
- [x] PWM ≠ аналог (`check-parallel.py`)
- [x] Цілісність землі (`check-gnd-tongues.py`)
- [x] Щілина під J5 — прийнято

**Репозиторій**
- [x] Немає абсолютних шляхів
- [x] Скрипт `tools/check-gnd-tongues.py`
