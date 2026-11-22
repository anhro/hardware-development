# motor-drive-controller

Контролер трифазного BLDC-двигуна: 12 В, 5 А (60 Вт).

| Вузол | Стан | Файли |
|-------|------|-------|
| Силовий інвертор: 3 напівмости AOD4184A, шунти WSR5 7.5 мОм з Kelvin-підключенням (NetTie), фільтр входів CSA 800 кГц, 150 мкФ + 100 нФ на +12M | схема (ДЗ 6, 9, 11, 13) | [`hardware/kicad/inverter.kicad_sch`](hardware/kicad/inverter.kicad_sch) |
| MCU STM32F405RGT6: HSE 8 МГц, SWD (1×6), VBAT, роз'єм датчиків Холла, SPI1 до драйвера, входи АЦП SO1–SO3 | схема (ДЗ 7–9) | [`hardware/kicad/mcu.kicad_sch`](hardware/kicad/mcu.kicad_sch) |
| Драйвер затворів DRV8305NPHP: накачка заряду, SPI, підсилювачі струму (VREF = VDDA MCU), EN_GATE, WAKE, nFAULT/PWRGD | схема (ДЗ 8, 9) | [`hardware/kicad/gate-driver.kicad_sch`](hardware/kicad/gate-driver.kicad_sch) |
| Конфігурація MCU: SYSCLK 168 МГц, TIM1 ШІМ 20 кГц (center-aligned), SPI1 5.25 МГц, ADC1/2/3 triple injected simultaneous, GPIO драйвера і датчиків Холла | CubeMX (ДЗ 7–9) | [`firmware/motor-drive-controller.ioc`](firmware/motor-drive-controller.ioc) |
| Прошивка: ініціалізація периферії, збірка CMake | збирається в CI | [`firmware/`](firmware/) |
| Блок живлення: XT30 → запобіжник 1206TD-10AS → TVS SMBJ18A → шини +12M (SS10P4) / +12V (SS14), buck LMR51610 12 → 5 В, LDO AZ1117C 5 → 3.3 В, електроліти 150 мкФ на виходах | схема (ДЗ 10, 11, 12) | [`hardware/kicad/power.kicad_sch`](hardware/kicad/power.kicad_sch) |
| Друкована плата: монтажні отвори M3, тестові точки, розміщення (ДЗ 12); трасування силової частини — доріжки 3.5 мм і полігони на F.Cu, Kelvin-лінії шунтів, правила `high_current` (ДЗ 13); лінії живлення 12V, 12_M, 5V, 3V3 — DC/DC і LDO (ДЗ 14, виконано в рамках ДЗ 13); повне трасування сигналів, In1/In2 — суцільний GND, stitching via, DRC 0 / 0 нерозведених (ДЗ 15) | в роботі (ДЗ 12–15) | [`hardware/kicad/motor-drive-controller.kicad_pcb`](hardware/kicad/motor-drive-controller.kicad_pcb) |

Листи з'єднані ієрархічними шинами: `DRV{PWM6}`, `DRV{SPI}`, `DRV{CTRL}`,
`DRV{STATUS}` (MCU ↔ Gate Driver), `GATE{GATE6}`, `PH{SENSE6}`, `CS{SHUNT6}`
(Inverter ↔ Gate Driver), `ANALOG{AIN4}` (усі три листи). Шини живлення
+12M, +12V, +5V, +3.3V — глобальні символи живлення з джерелом на листі Power.
Силові мережі відокремлені від сигнальних відгалужень NetTie NT1–NT13 (ДЗ 13):
`PWR.SHx`/`PWR.SLx` → лінії драйвера `PH.SHx`/`PH.SLx` і Kelvin-лінії `SH_Hx`/`SH_Lx`,
`+12M` → `+12ML` (PVDD і VDRAIN драйвера).

## Сигнали MCU

Імена збігаються з мітками на схемі та User Labels у `.ioc` (у коді — `DRV_INHA_Pin` тощо).

| Сигнал | Пін | Функція | Куди |
|--------|-----|---------|------|
| DRV.INHA / DRV.INLA | PA8 / PA7 | TIM1_CH1 / CH1N | DRV8305 |
| DRV.INHB / DRV.INLB | PA9 / PB0 | TIM1_CH2 / CH2N | DRV8305 |
| DRV.INHC / DRV.INLC | PA10 / PB1 | TIM1_CH3 / CH3N | DRV8305 |
| DRV.SCLK / DRV.SDO / DRV.SDI | PA5 / PA6 / PB5 | SPI1 (16 біт, CPOL 0, CPHA 2 Edge) | DRV8305; SDO — 1.5 кОм до 3.3 В |
| DRV.nSCS | PA4 | вихід, High (10 кОм до 3.3 В) | DRV8305 |
| DRV.EN_GATE | PC9 | вихід, Low | DRV8305 |
| DRV.WAKE | PC10 | вихід open-drain, FT (10 кОм до 5 В) | DRV8305 |
| DRV.nFAULT | PC4 | вхід (open-drain, 10 кОм до 3.3 В) | DRV8305 |
| DRV.PWRGD | PC5 | вхід (open-drain, 10 кОм до 3.3 В) | DRV8305 |
| ANALOG.SO1 / SO2 / SO3 | PC3 / PC2 / PC1 | ADC3_IN13 / ADC2_IN12 / ADC1_IN11, injected, тригер TIM1 TRGO (SO1 ↔ SO3 поміняно в ДЗ 15) | виходи CSA драйвера |
| ANALOG.TEMP | PC0 | ADC1_IN10, regular | NTC на інверторі |
| HALL1–HALL3 | PC6–PC8 | вхід, FT (5 V tolerant) | роз'єм J2 |

## Стан розведення плати

ERC: 0 помилок, 0 попереджень. DRC: 0 порушень, **0 нерозведених**, 0 розбіжностей зі схемою
(ДЗ 15). Плата розведена повністю: силова частина на F.Cu (ДЗ 13), сигнали MCU і драйвера на
F.Cu/B.Cu, In1.Cu і In2.Cu — суцільні шари GND, 549 via GND (stitching з кроком 5 мм, via біля
кожного GND-пада, 8 via 0.8/0.4 на GND-пад шунта) — див. [ДЗ 15](../assignments/homework_15/README.md).
Лишається:

- **тепловідведення VD3 (SS10P4)** — ≈ 2.1 Вт при 5 А; полігон `+12M` на F.Cu є,
  полігону на B.Cu і via під катодом ще немає;
- **захисні резистори** між SOx і входами АЦП;

Повний перелік — у [`docs/design-notes.md`](docs/design-notes.md#відкриті-питання).

## Документація

- Архітектура: [`docs/architecture.md`](docs/architecture.md)
- Інженерні рішення та відкриті питання: [`docs/design-notes.md`](docs/design-notes.md)
- Прошивка: [`firmware/README.md`](firmware/README.md)

```bash
make hardware    # ERC + PDF схеми -> build/hardware/, BOM (і Gerber, якщо є плата) -> build/hardware/manufacturing/
make firmware    # збірка прошивки -> firmware/build/Debug/
../tools/check-parallel.py hardware/kicad/motor-drive-controller.kicad_pcb  # PWM ↔ аналог
```
