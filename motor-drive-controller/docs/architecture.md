# Архітектура

Стан схеми після ДЗ 11. Аркуші MCU, Gate Driver, Inverter, Power; відкриті
питання — у [`design-notes.md`](design-notes.md#відкриті-питання).

## Сигнали

```mermaid
flowchart LR
    HSE["Кварц 8 МГц"] --> MCU
    DBG["SWD 1×6<br/>J1"] --- MCU
    HALL["Датчики Холла<br/>роз'єм J2"] -- "HALL1–3 → PC6–PC8 (FT)" --> MCU

    MCU["<b>MCU</b><br/>STM32F405RGT6<br/>168 МГц"]
    DRV["<b>Gate Driver</b><br/>DRV8305NPHP<br/>підсилювачі струму"]
    INV["<b>Inverter</b><br/>3× напівміст AOD4184A<br/>шунти 7.5 мОм, NTC"]

    MCU -- "INHA…INLC<br/>TIM1 CH1–3 / CH1N–3N" --> DRV
    DRV -- "nFAULT → PC4<br/>PWRGD → PC5" --> MCU
    MCU -- "SPI1, EN_GATE, WAKE" --> DRV
    DRV -- "SO1–3 → ADC1–3" --> MCU
    DRV -- "GHx / GLx" --> INV
    INV -- "SHx, SN / SP" --> DRV
    INV -- "TEMP_SENSE → PC0 (ADC1_IN10)" --> MCU
    INV --> M(("BLDC"))
```

Між листами сигнали йдуть ієрархічними шинами (`DRV{…}`, `GATE{GATE6}`,
`PH{SENSE6}`, `CS{SHUNT6}`, `ANALOG{AIN4}`), див. [README проєкту](../README.md).

## Живлення

```mermaid
flowchart LR
    IN["+12_IN<br/>XT30"] --> F1["F1 1206TD-10AS<br/>TVS SMBJ18A"]
    F1 -- "VD3 SS10P4" --> V12M["+12M<br/>≈ 5 А"]
    F1 -- "VD2 SS14" --> V12["+12V<br/>≈ 81 мА"]
    V12M --> Q["Стоки верхніх ключів<br/>AOD4184A"]
    V12M --> PVDD["DRV8305<br/>PVDD, VDRAIN (100 Ом)"]
    V12 --> BUCK["Buck LMR51610<br/>U3"]
    BUCK --> V5["+5V"]
    V5 --> HALL["Датчики Холла<br/>підтяжка WAKE"]
    V5 --> LDO["LDO AZ1117C<br/>VR1"]
    LDO --> V33["+3.3V"]
    V33 --> MCUP["STM32F405<br/>VDD, VDDA (через FL1) → VREF DRV8305"]
    V33 --> DRVL["DRV8305<br/>VREG (R9 330 Ом)"]
    V33 --> PU["Підтяжки nFAULT/PWRGD<br/>SWD VTref, NTC"]
    V33 --> VBAT["VBAT MCU<br/>без батарейки"]
```

Шини +12M (двигун) і +12V (логіка) розв'язані діодами Шотткі: струм гальмування
двигуна не потрапляє на живлення логіки. LDO після buck прибирає пульсації з VDDA
(опорна АЦП і VREF драйвера).

## Ключові рішення

| Вузол | Рішення | Обґрунтування |
|-------|---------|---------------|
| Силові ключі | AOD4184A, 40 В / 50 А, 5.8 мОм, TO-252 | [ДЗ 6](../../assignments/homework_06/README.md) |
| Шунти | WSR57L500FEA, 7.5 мОм, 5 Вт | [ДЗ 6](../../assignments/homework_06/README.md) |
| MCU | STM32F405RGT6: TIM1 з комплементарним ШІМ і dead-time, 3 ADC | [ДЗ 7](../../assignments/homework_07/README.md) |
| Тактування | HSE 8 МГц (ABLS-8.000MHz-D-3-Y-T), C<sub>ext</sub> = 22 пФ, R<sub>ext</sub> = 0, PLL → 168 МГц | [ДЗ 7](../../assignments/homework_07/README.md), [рішення ДЗ 12](design-notes.md) |
| Драйвер затворів | DRV8305NPHP (без LDO): вбудовані підсилювачі струму, SPI | [ДЗ 8](../../assignments/homework_08/README.md), [ДЗ 9](../../assignments/homework_09/README.md) |
| Датчики Холла | PC6–PC8: FT-піни, водночас TIM3_CH1–CH3 (апаратний інтерфейс Холла) | [ДЗ 8](../../assignments/homework_08/README.md) |
| Вхідний захист | запобіжник 1206TD-10AS (10 А, time-delay; до ДЗ 12 — PTC MF-R700), TVS SMBJ18A, Шотткі SS10P4 (+12M) / SS14 (+12V) | [ДЗ 10](../../assignments/homework_10/README.md), [ДЗ 12](../../assignments/homework_12/README.md) |
| +5V / +3.3V | buck LMR51610 (1 А, 400 кГц) → LDO AZ1117C (0.8 А) | [ДЗ 10](../../assignments/homework_10/README.md) |

Детально — у [`design-notes.md`](design-notes.md).

## Вимоги

| Параметр | Значення | Джерело |
|----------|----------|---------|
| Напруга живлення | 12 В | ДЗ 6 |
| Потужність двигуна з навантаженням | 60 Вт (5 А); двигун замінено на менш потужний, у ДЗ 6 було 168 Вт (~14 А) | ДЗ 6, 10 |
| Запас ключів за струмом / напругою | ≥ 1.5–2× / ≥ 1.5–2× (комфортно 3×) | ДЗ 6 |
| Максимальна напруга сигналу струму на вході АЦП | 3.3 В | ДЗ 6 |
| Підсилення сигналу струму | 10 В/В (значення DRV8305 після скидання, регістр 0x0A); для двигуна 5 А достатньо | ДЗ 9, 12 |
| Живлення логіки драйвера | +3.3V; VDRAIN — від +12M | ДЗ 8 |
