# Як переглянути роботу

Нічого встановлювати не потрібно — усе видно в браузері.

## 1. Звіт з домашнього завдання

Посилання, яке надсилається на перевірку, веде на одне з:

- **Pull Request** (`…/pull/N`) — вкладка **Files changed** показує, що саме
  змінилося в межах завдання; коментарі можна залишати прямо до рядків.
  Звіт `assignments/homework_NN/README.md` відкривається кнопкою
  **⋯ → View file**.
- **Release** (`…/releases/tag/hwNN`) — зафіксований стан на момент здачі.
  Внизу, у **Assets**, лежать готові файли:
  - `homework_NN.docx` — звіт у форматі Word;
  - `motor-drive-controller-schematic.pdf` — схема;
  - `motor-drive-controller-bom.csv` — перелік компонентів;
  - `motor-drive-controller-erc.rpt` — результат електричної перевірки (ERC).

## 2. Проміжні результати (без релізу)

У Pull Request: вкладка **Checks → CI → Artifacts** (потрібен вхід у GitHub).

## 3. Завантажити все на свій комп'ютер

- Без git: на головній сторінці репозиторію **Code → Download ZIP**
  (або **Source code (zip)** у релізі — саме та версія, що здавалася).
- З git:
  ```bash
  git clone https://github.com/anhro/hardware-development.git
  cd hardware-development
  git checkout hw07        # стан на момент здачі ДЗ 7
  make setup               # за бажанням: завантажити datasheets
  ```
  Схему відкривати файлом `motor-drive-controller/hardware/kicad/motor-drive-controller.kicad_pro`
  (KiCad 10) — усі бібліотеки компонентів у репозиторії, додаткове налаштування не потрібне.
