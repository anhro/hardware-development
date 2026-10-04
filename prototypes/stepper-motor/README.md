# stepper-motor

Макетний проєкт (breadboard): керування кроковим двигуном.

<!-- TODO: мета, двигун (тип, напруга, струм фази, кроків/оберт), драйвер, MCU -->
Кроковий двигун. Тип невідомий. Розмір 40 x 40 x 32 мм. Опір кожної з двох обмоток 24 Ом.
Підозрюю що при роботі з напругою 12 В він буде нормально працювати. Струм в такому випадку
буде дорівнювати I = V / R = 12 В / 24 Ом = 0.5 А - звичайний робочий струм для такого мотора.

Мета - навчитися працювати з кроковим двигуном та використовувати драйвер A4988.

| Вузол | Стан | Файли |
|-------|------|-------|
| Схема макета | не розпочато | [`hardware/kicad/`](hardware/kicad/) |
| Прошивка: ESP32 (Arduino), AccelStepper; кнопки вліво/вправо → 400 кроків | збирається | [`firmware/firmware.ino`](firmware/firmware.ino) |

## Макет

<!-- Фото: docs/images/breadboard.jpg (JPEG, стиснене, до ~500 КБ) -->
<!-- ![Макет](docs/images/breadboard.jpg) -->

## З'єднання

| Від | До | Сигнал | Примітка |
|-----|----|--------|----------|
|     |    |        |          |

## Прошивка

Скетч Arduino: [`firmware/firmware.ino`](firmware/firmware.ino). Плата, ядро ESP32 та
бібліотеки з точними версіями — у [`firmware/sketch.yaml`](firmware/sketch.yaml);
самі бібліотеки в git не зберігаються, `arduino-cli` завантажує їх під час збірки.

- **Arduino IDE 2:** File → Open → `firmware/firmware.ino`. Плата підставиться з
  `sketch.yaml`; бібліотеку AccelStepper встановити через Library Manager.
- **Командний рядок:** `make firmware PROJECT=stepper-motor` (потрібен `arduino-cli`
  у `PATH` або `ARDUINO_CLI=/шлях/до/arduino-cli`). Завантаження в плату:
  `arduino-cli upload -p /dev/ttyUSB0 --input-dir prototypes/stepper-motor/firmware/build prototypes/stepper-motor/firmware`.
- Нова бібліотека: `arduino-cli lib install <Name>`, потім додати рядок
  `- <Name> (<версія>)` у `libraries:` профілю в `sketch.yaml`.

## Команди

```bash
make hardware PROJECT=stepper-motor    # ERC + PDF схеми + BOM -> build/hardware/
make firmware PROJECT=stepper-motor    # збірка прошивки
make datasheets                        # PDF за hardware/datasheets/datasheets.txt
```
