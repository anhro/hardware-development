# motor-drive-controller

Контролер трифазного BLDC-двигуна: 12 В, до 14 А (168 Вт).

| Вузол | Стан | Файли |
|-------|------|-------|
| Силовий інвертор: 3 напівмости AOD4184A, шунти WSR5 7.5 мОм | схема (ДЗ 6) | [`hardware/kicad/inverter.kicad_sch`](hardware/kicad/inverter.kicad_sch) |
| MCU STM32F405RGT6: живлення, HSE 8 МГц, JTAG/SWD, VBAT | схема (ДЗ 7) | [`hardware/kicad/mcu.kicad_sch`](hardware/kicad/mcu.kicad_sch) |
| Конфігурація периферії: TIM1 CH1–3/CH1N–3N, ADC1 IN10 (NTC) | CubeMX (ДЗ 7) | [`firmware/motor-drive-controller.ioc`](firmware/motor-drive-controller.ioc) |
| Друкована плата | не розпочато | [`hardware/kicad/motor-drive-controller.kicad_pcb`](hardware/kicad/motor-drive-controller.kicad_pcb) |

- Архітектура: [`docs/architecture.md`](docs/architecture.md)
- Інженерні рішення та відкриті питання: [`docs/design-notes.md`](docs/design-notes.md)
- Прошивка: [`firmware/README.md`](firmware/README.md)

```bash
make hardware    # ERC + PDF схеми + BOM -> build/hardware/
make firmware    # після генерації CMake-проєкту в CubeMX
```
