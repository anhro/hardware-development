# Заняття 11: Джерела живлення. Частина 2

**Опис завдання**: завершити організацію багатолистової схеми в KiCad, виконати перевірку електричних правил та згенерувати BOM для проєкту.

1. Додайте ієрархічні мітки на лінії всередині листів зі схемами.

2. Синхронізуйте аркуші, закріплені на кореневому листі, та з’єднайте відповідні ієрархічні мітки між аркушами.

3. Виконайте перевірку електричних правил (ERC).

4. Згенеруйте BOM для проєкту.

## Рішення завдання

| № | Пункт | Стан |
|---|-------|------|
| 1 | Ієрархічні мітки всередині листів | ✅ виконано |
| 2 | Синхронізація аркушів і з'єднання на кореневому листі | ✅ виконано |
| 3 | ERC | ✅ 0 помилок, 0 попереджень |
| 4 | BOM | ⏳ потрібно виконати |

### 1. Ієрархічні мітки

Сигнали між листами згруповані в ієрархічні шини (bus alias, задані в проєкті).
На кожному листі шина виходить на ієрархічну мітку з тим самим ім'ям:

| Шина | Сигнали | Листи |
|------|---------|-------|
| `DRV{SPI}` | nSCS, SCLK, SDI, SDO | MCU ↔ Gate Driver |
| `DRV{PWM6}` | INHA, INLA, INHB, INLB, INHC, INLC | MCU --> Gate Driver |
| `DRV{CTRL}` | EN_GATE, WAKE | MCU --> Gate Driver |
| `DRV{STATUS}` | nFAULT, PWRGD | Gate Driver --> MCU |
| `GATE{GATE6}` | GHA, GLA, GHB, GLB, GHC, GLC | Gate Driver --> Inverter |
| `PH{SENSE6}` | SHA, SHB, SHC, SLA, SLB, SLC | Inverter ↔ Gate Driver |
| `CS{SHUNT6}` | SN_HA, SN_LA, SN_HB, SN_LB, SN_HC, SN_LC | Inverter --> Gate Driver |
| `ANALOG{AIN4}` | SO1, SO2, SO3, TEMP | Gate Driver, Inverter --> MCU |

Лист **Power** не має ієрархічних міток: усі його виходи (+12M, +12V, +5V, +3.3V, GND) -
символи живлення KiCad. Вони глобальні, тож з'єднуються з однойменними символами
на інших листах без проводів на кореневому листі.

### 2. Синхронізація листів

На кореневому листі для кожного аркуша виконано синхронізацію ієрархічних міток.
Отримані виводи аркушів з'єднані шинами:

![Кореневий лист: аркуші MCU, Gate Driver, Inverter, Power](images/root-sheet.png)

### 3. Перевірка електричних правил (ERC)

ERC по всьому проєкту (`make hardware` або **Inspect --> Electrical Rules Checker**):

```
***** Sheet /
***** Sheet /MCU/
***** Sheet /Gate Driver/
***** Sheet /Inverter/
***** Sheet /Power/

 ** ERC messages: 0  Errors 0  Warnings 0

 ** Ignored checks:
    - Global label only appears once in the schematic
    - Four connection points are joined together
    - SPICE model issue
    - Assigned footprint doesn't match footprint filters
```
