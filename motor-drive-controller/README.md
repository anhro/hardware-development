# motor-drive-controller

Контролер трифазного BLDC-двигуна: 12 В, до 14 А (168 Вт).

| Вузол | Стан | Файли |
|-------|------|-------|
| Силовий інвертор: 3 напівмости AOD4184A, шунти WSR5 7.5 мОм | схема (ДЗ 6) | [`hardware/kicad/inverter.kicad_sch`](hardware/kicad/inverter.kicad_sch) |
| MCU STM32F405RGT6: живлення, HSE 8 МГц, JTAG/SWD, VBAT, роз'єм датчиків Холла | схема (ДЗ 7, 8) | [`hardware/kicad/mcu.kicad_sch`](hardware/kicad/mcu.kicad_sch) |
| Драйвер затворів DRV83053PHP (DRV8305): накачка заряду, VREG 3.3 В, nFAULT/PWRGD | схема (ДЗ 8) | [`hardware/kicad/gate-driver.kicad_sch`](hardware/kicad/gate-driver.kicad_sch) |
| Конфігурація MCU: SYSCLK 168 МГц (HSE → PLL), TIM1 CH1–3/CH1N–3N → INHA…INLC, входи DRV_nFAULT/DRV_PWRGD, HALL1–3, ADC1 IN10 (NTC) | CubeMX (ДЗ 7, 8) | [`firmware/motor-drive-controller.ioc`](firmware/motor-drive-controller.ioc) |
| Прошивка: ініціалізація периферії, збірка CMake | збирається в CI | [`firmware/`](firmware/) |
| Друкована плата | не розпочато | [`hardware/kicad/motor-drive-controller.kicad_pcb`](hardware/kicad/motor-drive-controller.kicad_pcb) |

## Сигнали MCU

| Сигнал | Пін | Функція | Куди |
|--------|-----|---------|------|
| INHA / INLA | PA8 / PA7 | TIM1_CH1 / CH1N | DRV8305 |
| INHB / INLB | PA9 / PB0 | TIM1_CH2 / CH2N | DRV8305 |
| INHC / INLC | PA10 / PB1 | TIM1_CH3 / CH3N | DRV8305 |
| DRV_nFAULT | PC4 | вхід (open-drain, 10 кОм до 3.3 В) | DRV8305 |
| DRV_PWRGD | PC5 | вхід (open-drain, 10 кОм до 3.3 В) | DRV8305 |
| HALL1–HALL3 | PC6–PC8 | вхід, FT (5 V tolerant) | роз'єм J4 |
| TEMP_SENSE | PC0 | ADC1_IN10 | NTC на інверторі |

## Готовність до розведення плати

Схема ще не готова до PCB: 123 порушення ERC, не з'єднані мітки між листами,
не підключені WAKE/EN_GATE/SPI драйвера, footprint'и пасивних компонентів не
призначені. Повний перелік — у [`docs/design-notes.md`](docs/design-notes.md#відкриті-питання).

## Документація

- Архітектура: [`docs/architecture.md`](docs/architecture.md)
- Інженерні рішення та відкриті питання: [`docs/design-notes.md`](docs/design-notes.md)
- Прошивка: [`firmware/README.md`](firmware/README.md)

```bash
make hardware    # ERC + PDF схеми + BOM -> build/hardware/
make firmware    # збірка прошивки -> firmware/build/Debug/
```
