## Завдання

Завершити організацію багатолистової схеми в KiCad:
- ієрархічні мітки всередині листів;
- синхронізація аркушів на кореневому листі та з'єднання міток між аркушами;
- перевірка електричних правил (ERC);
- BOM для проєкту.

**Звіт по 11 домашньому завданню:** [`assignments/homework_11/README.md`](../blob/hw11/assignments/homework_11/README.md).

## Що зроблено

**1. Ієрархічні мітки.** Сигнали між листами згруповані в 8 ієрархічних шин (bus alias). На кожному листі шина виходить на ієрархічну мітку з тим самим ім'ям.

| Шина | Сигнали | Листи |
|------|---------|-------|
| `DRV{SPI}` | nSCS, SCLK, SDI, SDO | MCU ↔ Gate Driver |
| `DRV{PWM6}` | INHA, INLA, INHB, INLB, INHC, INLC | MCU → Gate Driver |
| `DRV{CTRL}` | EN_GATE, WAKE | MCU → Gate Driver |
| `DRV{STATUS}` | nFAULT, PWRGD | Gate Driver → MCU |
| `GATE{GATE6}` | GHA, GLA, GHB, GLB, GHC, GLC | Gate Driver → Inverter |
| `PH{SENSE6}` | SHA, SHB, SHC, SLA, SLB, SLC | Inverter ↔ Gate Driver |
| `CS{SHUNT6}` | SN_HA, SN_LA, SN_HB, SN_LB, SN_HC, SN_LC | Inverter → Gate Driver |
| `ANALOG{AIN4}` | SO1, SO2, SO3, TEMP | Gate Driver, Inverter → MCU |

Лист Power не має ієрархічних міток. Його виходи +12M, +12V, +5V, +3.3V і GND — глобальні power-символи.

**2. Кореневий лист.** Аркуші MCU, Gate Driver, Inverter і Power синхронізовані, а їхні виводи з'єднані шинами.

**3. ERC.** **0 error, 0 warning** по всьому проєкту.

**4. BOM.**
- **Нові поля:**
  - `MaxVoltage` — номінальна напруга конденсаторів: ≥ 2× робочої або за даташитом DRV8305;
  - `Manufacturer`, `MPN`, `Supplier`.
- **Заповнені для всіх компонентів:**
  - пасивні — YAGEO CC / RC0603;
  - решта — за виробником.
- **Уніфіковані значення:** `0.1u` → `100n`, `1000p` → `1n`, `100R` → `100`, `Thermistor` → `10k`. Однакові компоненти потрапляють в один рядок.
- **CI** (`tools/kicad-outputs.sh`):
  - колонки `Refs, Qty, Value, MaxVoltage, Footprint, Manufacturer, MPN, Supplier`;
  - групування за `Value, MaxVoltage, Footprint, MPN`;
  - `--exclude-dnp`.
- **Оптимізація BOM** (зауваження викладача): один номінал — один партномер з найбільшою потрібною напругою, бо кожен партномер — окремий фідер SMT-лінії.

  | Номінал | Було партномерів | Стало |
  |---|:---:|---|
  | 100n | 3 (10 / 16 / 25 В) | `CC0603KRX7R8BB104`, 25 В — 15 шт. |
  | 1u | 2 (16 / 25 В) | `CC0603KRX7R8BB105`, 25 В |
  | 2.2u | 3 (10 / 16 / 50 В) | `CC1206KKX7R9BB225`, 50 В, 1206 |
  | 4.7u | 2 (10 / 25 В) | `CC1206KKX7R8BB475`, 25 В, 1206 |
  | 10u | 2 (10 / 16 В) | `CC1206KKX7R7BB106`, 16 В, 1206 |
  | 47n | 2 (25 / 50 В) | `CC0603KRX7R9BB473`, 50 В |
  | 22u | 2 (10 / 25 В) | `CC1210KKX7R8BB226`, 25 В — 22u / 10 В видалено з виходу LDO |

- **Результат:** 37 рядків (конденсаторів 19 → 10), 92 компоненти. До оптимізації — 46 рядків, 93 компоненти.
- **Не входять у BOM:**
  - NT1 (net tie GND — EP драйвера) — мідь на платі;
  - батарейка CR2032 — купується окремо.

**Додатково:**
- **Конденсатори +12M інвертора: 330 → 150 мкФ** (C25, C29, C32, Nichicon `UCD1E151MCL6GS`, 25 В). Двигун 5 A, з запасом 2× — 10 A; правило 100…200 мкФ на 10 A.
- **Електроліти 150 мкФ / 25 В на виходах перетворювачів** (зауваження до ДЗ 10): C42 на +5V (buck), C44 на +3.3V (LDO).
- **Вихід LDO без кераміки** (зауваження викладача): керамічний 22 мкФ на виході VR1 видалено, залишився лише електроліт C44. Вимогу даташиту AZ1117C (≥ 10 мкФ, ESR < 20 Ом) він виконує.
- **Тримач батарейки** `CR2032` замінено на Harwin **S8421-45R** (J4) з MPN. Бібліотека в `lib/parts/S8421-45R`, datasheet у маніфесті.
- **C1 4.7 мкФ:** Y5V замінено на X7R (після уніфікації — `CC1206KKX7R8BB475`, як C22).
- **Переанотація** після додавання конденсаторів і заміни тримача:

  | Компонент | ДЗ 10 | ДЗ 11 |
  |---|---|---|
  | SMBJ18A | VD2 | VD1 |
  | SS14 | VD3 | VD2 |
  | SS10P4 | VD5 | VD3 |
  | 10 мкФ (+5V) | C42 | C43 |
  | 22 мкФ (+3.3V, кераміка) | C43 | видалено |
  | 150 мкФ (+3.3V, електроліт) | — | C44 |
  | DRV8305 | U3 | U2 |
  | LMR51610 | U4 | U3 |
  | роз'єм двигуна | J4 | J5 |
  | тримач батарейки | U2 | J4 |

## Де дивитися

- **Звіт:** [`assignments/homework_11/README.md`](../blob/hw11/assignments/homework_11/README.md)
- **Інженерні рішення та відкриті питання:** [`design-notes.md`](../blob/hw11/motor-drive-controller/docs/design-notes.md)
- **Схеми:**
  - [`motor-drive-controller.kicad_sch`](../blob/hw11/motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_sch) (кореневий лист);
  - [`mcu.kicad_sch`](../blob/hw11/motor-drive-controller/hardware/kicad/mcu.kicad_sch);
  - [`gate-driver.kicad_sch`](../blob/hw11/motor-drive-controller/hardware/kicad/gate-driver.kicad_sch);
  - [`inverter.kicad_sch`](../blob/hw11/motor-drive-controller/hardware/kicad/inverter.kicad_sch);
  - [`power.kicad_sch`](../blob/hw11/motor-drive-controller/hardware/kicad/power.kicad_sch).
- **Генерація BOM у CI:** [`tools/kicad-outputs.sh`](../blob/hw11/tools/kicad-outputs.sh)
- **Перевірка за чеклістом:** [`checklist.md`](../blob/hw11/assignments/homework_11/checklist.md)
- **Схема у PDF, BOM, звіт ERC, звіт `.docx`:** вкладка **Checks → CI → Artifacts**.

Локально:
- `make hardware` — ERC + PDF + BOM;
- `make report HW=11` — звіт у `.docx`.

## Стан ERC і відкриті питання

ERC: **0 error, 0 warning**.

Відкриті питання:

- **Пульсаційний струм C25, C29, C32.** Струм конденсаторів ланки живлення інвертора — до ≈ 2.5 A RMS на всі три, тобто ≈ 0.8 A на кожен. Звірити з допустимим ripple current `UCD1E151MCL6GS`.
- **З ДЗ 10:** нагрів VD3 (SS10P4, ≈ 2.1 W), малий запас F1 при +40 °C, ККД buck.
- **З ДЗ 9:** момент заміру струму, налаштування DRV8305 по SPI, захист входів АЦП, dead-time TIM1.

## Чекліст

Детальна перевірка кожного пункту — у [`checklist.md`](../blob/hw11/assignments/homework_11/checklist.md).

**Звіт**
- [x] Звіт у Markdown оновлено, зображення в `images/`
- [x] Рішення та відкриті питання внесені в `design-notes.md`

**Схема (KiCad)**
- [x] Ієрархічні мітки всередині листів (8 шин)
- [x] Аркуші синхронізовані, мітки з'єднані на кореневому листі
- [x] ERC: 0 error, 0 warning
- [x] Тримач S8421-45R у `lib/parts/`, datasheet у маніфесті
- [x] Усі компоненти мають номінал і footprint (93/93)
- [x] BOM: Manufacturer / MPN / Supplier заповнені для всіх 37 рядків, MaxVoltage — для всіх конденсаторів
- [x] BOM оптимізовано: один номінал — один партномер (46 → 37 рядків)
- [x] Вихід LDO без кераміки, лише електроліт C44
- [x] Значення уніфіковані

**Прошивка (CubeMX)**
- [x] Змін у прошивці немає

**Репозиторій**
- [x] Немає абсолютних шляхів та згенерованих файлів
- [x] CI генерує BOM з полями для замовлення
