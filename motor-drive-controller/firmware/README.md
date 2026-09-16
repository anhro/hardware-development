# Прошивка

Джерело правди для пінів, тактування та периферії —
[`motor-drive-controller.ioc`](motor-drive-controller.ioc) (STM32CubeMX).
Код пишеться лише між маркерами `/* USER CODE BEGIN … */ … /* USER CODE END … */`
або в окремих файлах — інакше CubeMX перезапише його при генерації.

## Що в git

| Шлях | У git | Чому |
|------|:-----:|------|
| `motor-drive-controller.ioc` | ✅ | конфігурація |
| `Core/`, власні модулі | ✅ | код |
| `CMakeLists.txt`, `CMakePresets.json`, `cmake/`, `*.ld`, `startup_*.s` | ✅ | збірка без CubeMX (CI) |
| `Drivers/` (лише необхідні файли HAL/CMSIS) | ✅ | фіксована версія бібліотек → відтворювана збірка; змінюється тільки при оновленні FW-пакета |
| `build/`, `EWARM/`, `.mxproject` | ❌ | генерується / не використовується |

## Перехід на CMake + VS Code (одноразово)

У `.ioc` вже виставлено: *Toolchain/IDE* = **CMake**, *Code generator* =
**Copy only the necessary library files**, ім'я проєкту `motor-drive-controller`.
Раніше проєкт був згенерований для IAR EWARM і з повною копією CMSIS (57 МБ).

```bash
cd motor-drive-controller/firmware
rm -rf Drivers EWARM .mxproject     # усе це відтворюється з .ioc і FW_F4 V1.28.3
```

1. Відкрити `.ioc` у STM32CubeMX → перевірити *Project Manager* → **Generate Code**.
2. Виправити тактування й dead-time (див. [design-notes](../docs/design-notes.md#відкриті-питання)).
3. VS Code з розширенням **STM32Cube for Visual Studio Code** → *Import CMake project*.
4. Перевірити збірку: `make firmware` (з кореня репозиторію).

Для цього потрібен STM32CubeCLT (компілятор, CMake, Ninja, ST-LINK GDB server) —
розширення VS Code запропонує встановити його автоматично.
