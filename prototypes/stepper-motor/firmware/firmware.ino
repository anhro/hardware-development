#include <AccelStepper.h>

// Піни для драйвера A4988
const int stepPin = 12;
const int dirPin = 14;

// Піни для кнопок (замикаються на GND)
const int buttonLeftPin = 26;
const int buttonRightPin = 27;

// Створюємо об'єкт двигуна (1 = режим DRIVER)
AccelStepper stepper(1, stepPin, dirPin);

void setup() {
  // Налаштування пінів кнопок із внутрішньою підтяжкою до 3.3V
  pinMode(buttonLeftPin, INPUT_PULLUP);
  pinMode(buttonRightPin, INPUT_PULLUP);

  // Налаштування базових параметрів двигуна
  // stepper.setMaxSpeed(3000);     // Максимальна швидкість (кроків/сек)
  stepper.setMaxSpeed(1000);     // Максимальна швидкість (кроків/сек)
  // stepper.setAcceleration(1000);  // Прискорення (кроків/сек^2)
  stepper.setAcceleration(500);  // Прискорення (кроків/сек^2)

  // Ініціалізація генератора випадкових чисел за допомогою шуму на аналоговому піні
  randomSeed(analogRead(34));
}

void loop() {
  // Зчитуємо стан кнопок (LOW означає, що кнопку натиснуто)
  bool leftPressed = (digitalRead(buttonLeftPin) == LOW);
  bool rightPressed = (digitalRead(buttonRightPin) == LOW);

  // Якщо натиснута кнопка ВЛІВО і двигун завершив попередній рух
  if (leftPressed && !rightPressed && stepper.distanceToGo() == 0) {
    long randomSteps = 400; //random(100, 200);      // Випадкова кількість кроків
    float randomSpeed = 1000; //random(400, 800);    // Випадкова швидкість
    
    stepper.setMaxSpeed(randomSpeed);
    stepper.move(-randomSteps);               // Рух у негативну сторону (вліво)
  }
  
  // Якщо натиснута кнопка ВПРАВО і двигун завершив попередній рух
  else if (rightPressed && !leftPressed && stepper.distanceToGo() == 0) {
    long randomSteps = 400; //random(100, 200);      // Випадкова кількість кроків
    float randomSpeed = 1000; //random(400, 800);    // Випадкова швидкість
    
    stepper.setMaxSpeed(randomSpeed);
    stepper.move(randomSteps);                // Рух у позитивну сторону (вправо)
  }
  
  // Якщо жодна кнопка не натиснута — даємо команду плавно зупинятися
  else if (!leftPressed && !rightPressed) {
    stepper.stop(); 
  }

  // Цей метод повинен викликатися постійно, він крутить двигун
  stepper.run();
}