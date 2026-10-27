## Завдання

Зібрати схему живлення моторного контролера з вхідною напругою **+12_IN** за заданою архітектурою:
- вхідний роз'єм і захист;
- силова шина +12M (двигун і драйвер ключів);
- DC/DC 12 → 5 V (датчики Холла);
- LDO 5 → 3.3 V (логіка).

**Звіт по 10 домашньому завданню:** [`assignments/homework_10/README.md`](../blob/hw10/assignments/homework_10/README.md).

## Що зроблено

**1. Вхідне коло.** Двигун замінено на менш потужний: 5 A замість 14 A з ДЗ 6. Струм на вході:
I<sub>12_IN</sub> = 5 A (двигун) + 19 mA (DRV8305) + 81 mA (вхід DC/DC) ≈ **5.1 A**.

| Позиція | Компонент | Параметри | Запас |
|---|---|---|---|
| XT1 | Amass XT30PW-M | 15 A тривало | ≈ 3× |
| F1 | Bourns MF-R700 | PolySwitch, I<sub>hold</sub> 7 A, I<sub>trip</sub> 14 A, 30 V | ≈ 1.4× (≈ 1.14× при +40 °C) |
| VD2 | Littelfuse SMBJ18A | TVS, однонаправлений, V<sub>RWM</sub> 18 V, I<sub>PP</sub> 20.6 A, V<sub>C</sub> 29.2 V | — |
| VD3 | SS14 | Шотткі 1 A / 40 V, шина плати +12V | ≈ 12× |
| VD5 | Vishay SS10P4-M3/86A | Шотткі 10 A / 40 V, V<sub>F</sub> 0.41 V @ 5 A, силова шина +12M | 2× |

Компоненти, задані умовою, при струмі 5.1 A працювали б без запасу, тому F1 і VD5 замінено:
- **F1:** замість PolySwitch 5 A / 16 V узято MF-R700. I<sub>hold</sub> 7 A при +23 °C і 5.81 A при +40 °C.
- **VD5:** замість SK54 узято SS10P4: удвічі більший струм, ≈ 2.1 W втрат замість 2.75 W.

VD3 і VD5 розв'язують шини: струм гальмування двигуна не потрапляє на живлення логіки.

**2. DC/DC 12 → 5 V — TI LMR51610XDBVR.** Синхронний buck, 1 A, V<sub>IN</sub> до 65 V, 400 kHz, SOT-23-6.
- Обв'язка за таблицею даташита для 5 V:
  - L1 — Coilcraft XAL6060-333MEC, 33 µH, I<sub>sat</sub> 3.7 A > I<sub>HS_PK(OC)</sub> max 1.95 A;
  - вхід: C<sub>IN</sub> 2.2 µF / 50 V + 100 nF ВЧ;
  - C<sub>OUT</sub> 22 µF / 25 V;
  - C<sub>BOOT</sub> 0.1 µF.
- Дільник 118k / 22.1k дає 5.07 V.
- Навантаження 165 mA, запас ≈ 6×.

**3. LDO 5 → 3.3 V — Diodes AZ1117CH-3.3TRG1.** 0.8 A, SOT-223, стабільний з керамікою.
- Бюджет +3.3V — 60…130 mA (MCU + логіка). Запас 0.8 / 0.13 ≈ 6× при вимозі ≥ 2×.
- Падіння 1.7 V > V<sub>DROP</sub> max 1.3 V.
- Втрати 0.22 W, T<sub>J</sub> ≈ 67.5 °C при T<sub>A</sub> = 40 °C.

**4. Аркуш Power у KiCad.** Новий ієрархічний аркуш `power.kicad_sch`. Живлення йде на інші аркуші глобальними power-символами:
- +12M: Gate Driver (PVDD), Inverter;
- +5V: MCU, Gate Driver;
- +3.3V: MCU, Gate Driver, Inverter.

**Додатково:**
- **Термопад EP DRV8305 з'єднано з GND через Net_Tie_2.** Так прибрано зауваження «Both GND and EP are attached to the same items».
- **Footprint NT1:** `NetTie:NetTie-2_SMD_Pad0.5mm`.
- **R8 330 Ом послідовно у VREG.** Він обмежує струм через внутрішній діод VREG → PVDD, коли PVDD < VREG.
- **Виправлено типи пінів у символах:**
  - AZ1117: `power_out` / `power_in`;
  - CB у LMR51610: `passive`.
- **У конденсаторів аркуша Power є поле `Voltage`.** Робоча напруга видна в BOM.

## Де дивитися

- **Звіт:** [`assignments/homework_10/README.md`](../blob/hw10/assignments/homework_10/README.md)
- **Інженерні рішення та відкриті питання:** [`design-notes.md`](../blob/hw10/motor-drive-controller/docs/design-notes.md)
- **Схеми:**
  - [`power.kicad_sch`](../blob/hw10/motor-drive-controller/hardware/kicad/power.kicad_sch) (новий);
  - [`gate-driver.kicad_sch`](../blob/hw10/motor-drive-controller/hardware/kicad/gate-driver.kicad_sch);
  - [`inverter.kicad_sch`](../blob/hw10/motor-drive-controller/hardware/kicad/inverter.kicad_sch);
  - [`mcu.kicad_sch`](../blob/hw10/motor-drive-controller/hardware/kicad/mcu.kicad_sch).
- **Бібліотеки компонентів:** [`lib/parts/`](../blob/hw10/motor-drive-controller/hardware/kicad/lib/parts)
- **Datasheets:** [`datasheets.txt`](../blob/hw10/motor-drive-controller/hardware/datasheets/datasheets.txt)
- **Перевірка за чеклістом:** [`checklist.md`](../blob/hw10/assignments/homework_10/checklist.md)
- **Схема у PDF, BOM, звіт ERC, звіт `.docx`:** вкладка **Checks → CI → Artifacts**.

Локально:
- `make hardware` — ERC + PDF + BOM;
- `make report HW=10` — звіт у `.docx`.

## Стан ERC і відкриті питання

ERC: **0 error, 0 warning**. У ДЗ 9 було 1 warning, а кола +3.3V/+5V не мали джерела. Тепер вони живляться від VR1 і U4.
`PWR_FLAG` лишився тільки на +12_IN і +12V, бо роз'єм і діоди мають пасивні виводи.

Відкриті питання:

- **Нагрів VD5.** ≈ 2.1 W розсіюється на VD5, тому потрібен полігон міді під катодом на обох шарах з перехідними отворами.
  Альтернатива — ідеальний діод (LM74700 + MOSFET).
- **Малий запас F1 при нагріві.** За таблицею Thermal Derating MF-R700: I<sub>hold</sub> 5.81 A при +40 °C,
  тобто запас ≈ 1.14 при вхідному струмі 5.1 A. На PCB F1 треба розмістити подалі від VD5 і ключів.
- **ККД buck.** ККД 0.85 при 165 mA — припущення; звірити з графіком даташиту LMR51610.
- **З ДЗ 9:** момент заміру струму, налаштування DRV8305 по SPI, захист входів АЦП, dead-time TIM1.

## Чекліст

Детальна перевірка кожного пункту — у [`checklist.md`](../blob/hw10/assignments/homework_10/checklist.md).

**Звіт**
- [x] Звіт у Markdown оновлено, зображення в `images/`
- [x] Рішення та відкриті питання внесені в `design-notes.md`

**Схема (KiCad)**
- [x] 7 нових компонентів у `lib/parts/`, усі 8 datasheets у маніфесті
- [x] Усі компоненти мають номінал і footprint (92/92)
- [x] Живлення між листами з'єднане глобальними power-символами
- [x] ERC: 0 error, 0 warning

**Прошивка (CubeMX)**
- [x] Змін у прошивці немає

**Репозиторій**
- [x] Немає абсолютних шляхів та згенерованих файлів
