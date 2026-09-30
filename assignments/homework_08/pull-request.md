## Завдання

Імпортувати компонент DRV8305, створити схему його підключення за даташитом, позначити
сигнали PWM/діагностики та підключити датчики Холла до FT-пінів MCU.

**Звіт по 8 домашньому завданню:** [`assignments/homework_08/README.md`](../blob/hw08/assignments/homework_08/README.md).

## Що зроблено

**1. Вибір і імпорт компонента.** З родини DRV8305 обрано **DRV83053PHP**: промислова
версія (без суфікса Q/Q1), вбудований стабілізатор на 3.3 В — під наявне живлення MCU,
корпус HTQFP-48 (PHP) у лотках, зручний для ручної пайки. Повний розбір суфіксів —
у звіті. Компонент із SnapEDA покладено в репозиторій як самодостатню бібліотеку:

```
motor-drive-controller/hardware/kicad/lib/parts/DRV83053PHP/
├── DRV83053PHP.kicad_sym
├── DRV83053PHP.step
└── DRV83053PHP.pretty/
    └── QFP50P900X900X120-49N.kicad_mod
```

Бібліотеки підключені як *Project Specific* через `${KIPRJMOD}`, datasheet додано в
`datasheets.txt` — проєкт відкривається на будь-якому комп'ютері без налаштувань.

**2. Схема драйвера** — новий лист [`gate-driver.kicad_sch`](../blob/hw08/motor-drive-controller/hardware/kicad/gate-driver.kicad_sch):
DRV83053PHP, 8 конденсаторів і 3 резистори за таблицею *External Components* (ст. 5
даташиту). Живлення логіки — +3V3, на VDRAIN подано напругу двигуна +12M.

**3. PWM.** Виходи advanced-таймера TIM1 позначено мітками `INHA…INLC` на обох листах —
і на схемі MCU, і на схемі драйвера. Ті самі імена задано як *User Label* у CubeMX,
тож вони однакові на схемі, в `.ioc` і в коді (`INHA_Pin`…`INLC_Pin`):

| Сигнал | Пін MCU | Функція | Вивід DRV8305 |
|--------|---------|---------|---------------|
| INHA / INLA | PA8 / PA7 | TIM1_CH1 / CH1N | 2 / 3 |
| INHB / INLB | PA9 / PB0 | TIM1_CH2 / CH2N | 4 / 5 |
| INHC / INLC | PA10 / PB1 | TIM1_CH3 / CH3N | 6 / 7 |

**4. Діагностика.** Сигнали `DRV_nFAULT` і `DRV_PWRGD` виведено на схему з
підтягувальними резисторами 10 кОм (open-drain, номінал за таблицею *Pin Functions*).
У CubeMX налаштовані як входи: PC4 — nFAULT, PC5 — PWRGD.

**5. Мітки.** Усім нетам на обох листах присвоєно локальні мітки: живлення (PVDD, DVDD,
AVDD, VREG, VCPH), затвори (GHA…GLC), фази (PHASE_A…C) та входи підсилювачів струму
(SN_HA…SN_LC, SLA…SLC).

**6. Датчики Холла.** `HALL1…HALL3` підключено до **PC6, PC7, PC8** — пінів з
підтримкою 5 V tolerant I/O (FT) за даташитом STM32F405 (DM00037051, с. 48–61).
У CubeMX налаштовані як GPIO-входи.

Конфігурацію MCU оновлено в [`motor-drive-controller.ioc`](../blob/hw08/motor-drive-controller/firmware/motor-drive-controller.ioc),
код перегенеровано: визначення пінів у `Core/Inc/main.h`, входи GPIOC — у `MX_GPIO_Init`,
піни ШІМ — у `HAL_TIM_MspPostInit`. Тактування виправлено: HSE 8 МГц → PLL → 168 МГц.
Прошивка збирається без попереджень (FLASH 1.07 %, RAM 1.32 %).

## Де дивитися

- **Звіт із розбором вибору компонента:** [`assignments/homework_08/README.md`](../blob/hw08/assignments/homework_08/README.md)
- **Схема драйвера:** [`gate-driver.kicad_sch`](../blob/hw08/motor-drive-controller/hardware/kicad/gate-driver.kicad_sch)
- **Схема MCU:** [`mcu.kicad_sch`](../blob/hw08/motor-drive-controller/hardware/kicad/mcu.kicad_sch)
- **Скріншоти** (схема драйвера, схема MCU, Pinout View, FT-піни) — у звіті.
- **Інженерні рішення та відкриті питання:** [`design-notes.md`](../blob/hw08/motor-drive-controller/docs/design-notes.md)
- **Перевірка за чеклістом:** [`checklist.md`](../blob/hw08/assignments/homework_08/checklist.md)
- **Схема у PDF, BOM, звіт ERC, звіт `.docx`:** вкладка **Checks → CI → Artifacts**.

Локально: `make hardware` (ERC + PDF + BOM), `make report HW=08` (звіт у `.docx`),
`make firmware` (збірка прошивки).

## Стан ERC і відкриті питання

`make hardware` дає 123 порушення (73 error, 50 warning). Вимоги завдання виконані;
порушення стосуються готовності схеми до розведення плати:

- **Міжлистові з'єднання.** Сигнали між листами MCU, Gate Driver та Inverter позначені
  *локальними* мітками, як вимагало завдання, тому електрично вони поки не з'єднані —
  звідси 45 попереджень `isolated_pin_label` і 23 `pin_not_driven`. Для реального
  з'єднання потрібні ієрархічні мітки з пінами листа або глобальні мітки.
- **41 непідключений пін** MCU і драйвера — будуть задіяні в наступних завданнях
  (SPI-керування драйвером, виходи підсилювачів струму SO1–SO3 → ADC).
- **Footprint'и пасивних компонентів** ще не призначені (є у 14 з 54 компонентів).

Знайдені під час аналізу схеми питання, які треба закрити до розведення плати
(детально — у [`design-notes.md`](../blob/hw08/motor-drive-controller/docs/design-notes.md)):

- шина +3.3V MCU живиться лише від VREG драйвера — перевірити запас струму та
  поведінку VREG у режимі sleep / при аварії;
- WAKE і EN_GATE драйвера не підключені;
- термопад драйвера (EP) не з'єднаний з GND;
- nFAULT варто завести на TIM1_BKIN (вільний PA6) для апаратного вимкнення ШІМ;
- dead-time TIM1 = 0, Break вимкнено;
- датчики Холла живляться від +5V, джерела якого на схемі ще немає.

## Чекліст

Детальна перевірка кожного пункту — у [`checklist.md`](../blob/hw08/assignments/homework_08/checklist.md).

**Звіт**
- [x] Звіт у Markdown оновлено, зображення в `images/`
- [x] Рішення та відкриті питання внесені в `design-notes.md`

**Схема (KiCad)**
- [x] Новий компонент у `lib/parts/DRV83053PHP/`, бібліотеки через `${KIPRJMOD}`,
      datasheet у `datasheets.txt`
- [ ] Усі компоненти мають номінал і footprint — номінали є, footprint'и пасивних
      компонентів ще не призначені
- [ ] Сигнали між листами з'єднані ієрархічними/глобальними мітками — за завданням
      використано локальні
- [ ] ERC: порушення пояснені, виправлення — у наступних завданнях

**Прошивка (CubeMX)**
- [x] Імена пінів у `.ioc` збігаються з мітками на схемі
- [x] Код перегенеровано, прошивка збирається (`make firmware`)

**Репозиторій**
- [x] Немає абсолютних шляхів та згенерованих файлів
