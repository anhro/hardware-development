## Завдання

Трасування (Routing) та полігони:
- розрахувати ширину провідників для струму двигуна 4 А з коефіцієнтом запасу ×2;
- клас мереж `HIGH_CURRENT` для силових ліній і ліній живлення 12 В;
- правило трасування `high_current`;
- трасування листа power_switches (у проєкті — **Inverter**) від входу живлення, без GND;
- полігони між J5 і ключами та між ключами, Kelvin-підключення шунтів, PWM не паралельно до
  аналогових ліній вимірювання струму.

**Звіт по 13 домашньому завданню:** [`assignments/homework_13/README.md`](../blob/hw13/assignments/homework_13/README.md).

## Що зроблено

**1. Ширина провідників.** IPC-2221, I = 4 А × 2 = 8 А, зовнішній шар 1 oz, ΔT ≈ 20 °C →
**3.5 мм** (при робочих 4 А перегрів ≈ 4 °C). Внутрішні шари 0.5 oz потребували б 18 мм, тому
силовий струм — лише на F.Cu. Via 0.8/0.4 мм ≈ 2.4 А.

**2. Класи мереж.**

| Клас | Мережі | Доріжка, мм | Зазор, мм |
|------|--------|-------------|-----------|
| `HIGH_CURRENT` | `+12_IN`, `+12_FUSED`, `+12M`, `/Inverter/PWR.S*` | 3.5 | 0.2 |
| `KELVIN_LINE` | `/Inverter/SH_*` | 0.3 | 0.15 |
| `Supply` | `+12V`, `+12ML`, `+5V`, `+3.3V` | 0.5 | 0.15 |
| `Default` | решта | 0.2 | 0.15 |

Силові мережі відокремлені від сигнальних відгалужень footprint-ами **NetTie**:

| NetTie | Що відокремлює |
|--------|----------------|
| NT1–NT6 | Kelvin-лінії `SH_Hx`/`SH_Lx` від падів шунтів (`PWR.SLx`, `GND`) |
| NT8–NT13 | лінії SHx/SLx драйвера (`/Gate Driver/PH.Sxx`) від силових `PWR.Sxx` |
| NT7 | живлення драйвера `+12ML` (PVDD, VDRAIN) від `+12M` |

**3. Правила `.kicad_dru`.**
- `high_current` — мінімум 3.5 мм, зазор 0.2 мм, via ≥ 0.8/0.4 мм.
- `high_current_neckdown_12m`, `high_current_neckdown_taps` — звуження до 0.5 мм лише для
  `+12M` біля VD3/C24/C38 і для `PWR.S*` біля Q2/Q4/Q6, R16/R19/R22. Перша версія з
  `intersectsCourtyard('*')` пропускала довгі вузькі доріжки, тому її звужено.
- `high_current_zone_smd` — суцільне підключення силових SMD-падів до полігонів.

**4. Трасування від входу живлення.** XT1 → F1 → VD1/VD3/VD2 → `+12M` → ключі: доріжки 3.5 мм
і полігони на F.Cu, без via у силовому колі. GND за умовою не трасовано.

**5. Полігони, Kelvin, PWM.**
- 6 полігонів на F.Cu: `+12_IN`, `+12_FUSED`, `+12M`, `PWR.SHA/B/C`; підключення падів
  суцільне, включно з XT1 і J5.
- Kelvin: вимірювальні лінії відходять від внутрішніх країв падів шунтів через NetTie і парами
  йдуть до RC-фільтрів R13–R21/C27, C30, C33.
- PWM ↔ аналог: скрипт [`tools/check-parallel.py`](../blob/hw13/tools/check-parallel.py) —
  паралельних ділянок із зазором < 1 мм немає, найближча — 2.5 мм із зазором 1.0 мм.

**Зміни схеми:**

| Що | Було | Стало | Чому |
|----|------|-------|------|
| Мережа після F1 | `Net-(VD3-Anode_1)` | power-мітка `+12_FUSED` + `PWR_FLAG` | стабільна назва для шаблону класу |
| Фазні мережі | `/Gate Driver/PH.SHx`, `PH.SLx` цілі | `/Inverter/PWR.SHx`, `PWR.SLx` + NetTie NT8–NT13 | правило 3.5 мм діє лише на силову мідь |
| Kelvin-лінії шунтів | частина `PH.SLx` і `GND` | `SH_Hx`, `SH_Lx` через NT1–NT6 | 4-wire; полігон GND не з'єднається з лінією |
| Живлення DRV8305 | `+12M` | `+12ML` через NT7 + `PWR_FLAG` на `+12M` | тонка доріжка до PVDD поза `HIGH_CURRENT` |

## Де дивитися

- **Звіт:** [`assignments/homework_13/README.md`](../blob/hw13/assignments/homework_13/README.md)
- **Інженерні рішення та відкриті питання:** [`design-notes.md`](../blob/hw13/motor-drive-controller/docs/design-notes.md)
- **Плата:** [`motor-drive-controller.kicad_pcb`](../blob/hw13/motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_pcb), правила DRC — [`motor-drive-controller.kicad_dru`](../blob/hw13/motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_dru)
- **Схеми:**
  - [`inverter.kicad_sch`](../blob/hw13/motor-drive-controller/hardware/kicad/inverter.kicad_sch) (ключі, шунти, NetTie);
  - [`gate-driver.kicad_sch`](../blob/hw13/motor-drive-controller/hardware/kicad/gate-driver.kicad_sch) (NT7, `+12ML`);
  - [`power.kicad_sch`](../blob/hw13/motor-drive-controller/hardware/kicad/power.kicad_sch) (`+12_FUSED`, `PWR_FLAG`).
- **Скрипт перевірки PWM ↔ аналог:** [`tools/check-parallel.py`](../blob/hw13/tools/check-parallel.py)
- **Перевірка за чеклістом:** [`checklist.md`](../blob/hw13/assignments/homework_13/checklist.md)
- **Схема у PDF, BOM, звіт ERC, звіт `.docx`:** вкладка **Checks → CI → Artifacts**.

Локально:
- `make hardware` — ERC + PDF + BOM;
- `make report HW=13` — звіт у `.docx`;
- `tools/check-parallel.py motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_pcb` — паралельні ділянки.

## Стан ERC/DRC і відкриті питання

ERC: **0 error, 0 warning**. DRC: **0 порушень**, 0 розбіжностей зі схемою. Нерозведені
з'єднання — 118: GND (60, за умовою) і логіка MCU/драйвера (58); у силових мережах — 0.

Відкриті питання:

- **GND:** полігон землі на внутрішньому шарі; полігон GND на F.Cu між падами шунтів і
  C25/C29/C32; 4–6 via 0.8/0.4 мм біля кожного GND-пада шунта.
- **Нерозведені сигнали** листів MCU і Gate Driver, зокрема PWM (`DRV.INHx/INLx`) і
  `ANALOG.SO1–3` — подалі від фільтрів CSA.
- **Пайка XT1 і J5:** пади під'єднані суцільно, полігон лише на F.Cu — перевірити на прототипі.

## Чекліст

Детальна перевірка кожного пункту — у [`checklist.md`](../blob/hw13/assignments/homework_13/checklist.md).

**Звіт**
- [x] Звіт у Markdown, зображення в `images/` (5 посилань коректні)
- [x] Рішення та відкриті питання внесені в `design-notes.md`
- [x] Документація проєкту (README, `architecture.md`) оновлена

**Завдання**
- [x] Ширина провідників для 4 А × 2: 3.5 мм (IPC-2221)
- [x] Клас мереж `HIGH_CURRENT`
- [x] Правило `high_current` і звужені винятки
- [x] Трасування від входу живлення, без GND
- [x] J5 ↔ ключі та ключі між собою — полігонами
- [x] Kelvin-підключення шунтів (NetTie, `KELVIN_LINE`)
- [x] PWM не паралельно аналоговим лініям (зазор < 1 мм — 0)

**Схема (KiCad)**
- [x] ERC: 0 error, 0 warning
- [x] NetTie NT1–NT13, power-мітки й `PWR_FLAG`
- [x] BOM: 37 рядків, 88 компонентів

**Плата (PCB)**
- [x] Класи мереж і 6 полігонів
- [x] DRC: 0 порушень, 0 розбіжностей зі схемою
- [x] Нерозведені лише GND і логіка

**Репозиторій**
- [x] Немає абсолютних шляхів
- [x] Скрипт `tools/check-parallel.py`
