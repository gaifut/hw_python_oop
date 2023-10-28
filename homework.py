from dataclasses import dataclass, fields, asdict

READ_PACKAGE_MESSAGE_KEY = (
    '{} not found among keys of {} ,so no Training class value could be'
    ' retrieved.Add this argument to dictionary or modify argument.'
)
READ_PACKAGE_MESSAGE_VALUE = (
    'The number of arguments in {} doesnt match {}. Also check if {}'
    ' is correct input.'
)
GET_SPENT_CALORIES_MESSAGE = 'define in child class of Training'


@dataclass
class InfoMessage:
    """Informational message about the training."""

    training_type: int
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км; Ср. скорость:'
        ' {speed:.3f} км/ч; Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Basic class for training."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HR = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the mean speed im km/h."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories spent in kcal."""
        raise NotImplementedError(GET_SPENT_CALORIES_MESSAGE)

    def show_training_info(self) -> InfoMessage:
        """Return info message about the training completed."""
        return InfoMessage(
            type(self).__name__, self.duration,
            self.get_distance(), self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HR
        )


@dataclass
class SportsWalking(Training):
    CALORY_MULTIPLIER_1 = 0.035
    CALORY_MULTIPLIER_2 = 0.029
    SEC_IN_MIN = 60
    CM_IN_M = 100
    KM_H_TO_MT_SEC_RATIO = round(
        Training.M_IN_KM / (Training.MIN_IN_HR * SEC_IN_MIN), 3
    )

    height: float

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORY_MULTIPLIER_1 * self.weight
                + (
                    (
                        self.get_mean_speed() * self.KM_H_TO_MT_SEC_RATIO
                    )
                    ** 2 / (self.height / self.CM_IN_M)
                )
                * self.CALORY_MULTIPLIER_2 * self.weight
            )
            * self.duration * self.MIN_IN_HR
        )


@dataclass
class Swimming(Training):
    LEN_STEP = 1.38
    CALORIES_ADDED = 1.1
    CALORIES_MULTIPLIER = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (
                self.get_mean_speed() + self.CALORIES_ADDED
            )
            * self.CALORIES_MULTIPLIER * self.weight * self.duration
        )


TRAINING_CLASSES = {
    'SWM': [Swimming, len(fields(Swimming))],
    'RUN': [Running, len(fields(Running))],
    'WLK': [SportsWalking, len(fields(SportsWalking))]
}


def read_package(workout_type: str, data: list[int]) -> Training:
    """Read the sensor data."""
    if workout_type not in TRAINING_CLASSES:
        raise KeyError(
            READ_PACKAGE_MESSAGE_KEY.format(workout_type, TRAINING_CLASSES)
        )
    training_class, num_fields_data = TRAINING_CLASSES[workout_type]
    if len(data) != num_fields_data:
        raise ValueError(
            READ_PACKAGE_MESSAGE_VALUE.format(
                data, num_fields_data, workout_type
            )
        )
    return training_class(*data)


def main(training: Training) -> None:
    """Main function."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
