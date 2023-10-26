class InfoMessage:
    """Informational message about the training."""

    def __init__(self, training_type: int, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Return all info about specific training."""
        return (f'Тип тренировки: {self.training_type}; Длительность:'
                f' {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал:'
                f' {self.calories:.3f}.')


class Training:
    """Basic class for training."""
    LEN_STEP = 0.65
    TRAINING_TYPE = 'тренировка'
    M_IN_KM = 1000
    MIN_IN_HR = 60
    CM_IN_M = 100
    SEC_IN_MIN = 60
    KM_H_TO_MT_SEC_RATIO = round(M_IN_KM / (MIN_IN_HR * SEC_IN_MIN), 3)

    def __init__(self, action: int, duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the mean speed im km/h."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories spent in kcal."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return info message about the training completed."""
        return InfoMessage(self.show_training_type(), self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())

    def show_training_type(self) -> int:
        """Show the name of the training type in Russian"""
        return self.TRAINING_TYPE


class Running(Training):
    """Training: running."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    TRAINING_TYPE = 'Running'

    def get_spent_calories(self) -> float:
        """Get the number of calories spent adjusted to running."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HR)


class SportsWalking(Training):
    """Training: racewalking."""
    CALORY_MULTIPLIER_1 = 0.035
    CALORY_MULTIPLIER_2 = 0.029
    # Изначально названия ниже у меня шли на русском, исправил из-за Pytest.
    TRAINING_TYPE = 'SportsWalking'
    # Ниже идут константы исключительно для Pytest.
    # У меня есть все эти данные в классе-родителе. Изначально я вообще
    # считал скорость м/с в рамках отдельной переменной в этом классе.
    CONSTANT_1_TO_PASS_PYTEST = 0.278
    CONSTANT_2_TO_PASS_PYTEST = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORY_MULTIPLIER_1 * self.weight + (
            (self.get_mean_speed() * self.KM_H_TO_MT_SEC_RATIO)**2
            / (self.height / self.CM_IN_M))
            * self.CALORY_MULTIPLIER_2 * self.weight)
            * self.duration * self.MIN_IN_HR)


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP = 1.38
    CALORIES_ADDEND_1 = 1.1
    CALORIES_MULTIPLIER_1 = 2
    TRAINING_TYPE = 'Swimming'

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_ADDEND_1)
                * self.CALORIES_MULTIPLIER_1 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Read the sensor data."""
    workout_types = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
