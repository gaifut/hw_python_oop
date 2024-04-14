# Модуль фитнес-трекера
Модуль написан на Python3.9 на Linux.

## Описание
Программа обрабатывает данные для трех видов тренировок: для бега, спортивной ходьбы и плавания, а именно:
- определяет вид тренировки
- рассчитывает результаты тренировки
- выводит информационное сообщение о результатах:
  - длительность
  - дистанция
  - средняя скорость
  - потраченные калории
 
## Установка и запуск
1. Склонируйте репозиторий ```git clone git@github.com:gaifut/hw_python_oop.git```
2. Установите виртуальное окружение и зависимости.
```
# Для Linux/MacOS
python3 -m venv venv

# Для Windows
python -m venv venv

# Активируйте виртуальное окружение:
source venv/bin/activate

# Обновите pip
python -m pip install --upgrade pip 

# Установите зависимости
pip install -r requirements.txt
```
3. Запустите проект. В папке с проектом в терминале наберите: ```python homework.py```
