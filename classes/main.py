import abc
import json
import logging

logging.basicConfig(filename="info.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s", encoding="UTF-8")
logger = logging.getLogger("main")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

car_registry = {}


class InvalidCarError(Exception):
    def __init__(self, msg="Электромобиль содержит некорректные данные"):
        self.msg = msg
        super().__init__(msg)


class PermissionDeniedError(Exception):
    def __init__(self, msg="Нет прав доступа"):
        self.msg = msg
        super().__init__(msg)


class RentalNotFoundError(Exception):
    def __init__(self, msg="Аренда не найдена"):
        self.msg = msg
        super().__init__(msg)


def check_permissions(required_permission):
    """Декоратор для проверки доступа пользователя"""
    def decorator(func):
        def wrapper(self, user_permission, *args, **kwargs):
            if required_permission not in user_permission:
                logger.info(f"Доступ: {required_permission} отклонен")
                raise PermissionDeniedError
            logger.info(f"Доступ: {required_permission} разрешен")
            return func(self, user_permission, *args, **kwargs)
        return wrapper
    return decorator


class ElectricCarMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        if new_class is not ElectricCar:
            car_registry[new_class.__name__] = new_class
        return new_class


class ElectricCar(abc.ABC):
    __metaclass__ = ElectricCarMeta
    """
    Базовый класс ElectricCar
    Аттрибуты:
        car_id (int)
        model (str)
        battery_level (int)
        hourly_rate (int)
        is_available (bool
    """
    def __init__(self, car_id, model, battery_level, hourly_rate, is_available):
        self.__car_id = car_id
        self.__model = model
        self.__battery_level = battery_level
        self.__hourly_rate = hourly_rate
        self.__is_available = is_available

    @abc.abstractmethod
    def calculate_rental_cost(self):
        pass

    def __str__(self):
        return f"Электромобиль: {self.__model}, Заряд: {self.__battery_level}%"

    def __lt__(self, other):
        return self.__hourly_rate < other.hourly_rate

    def __gt__(self, other):
        return self.__hourly_rate > other.hourly_rate

    def __eq__(self, other):
        return self.__hourly_rate == other.hourly_rate

    @property
    def car_id(self):
        return self.__car_id

    @car_id.setter
    def car_id(self, car_id):
        self.__car_id = car_id

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    @property
    def battery_level(self):
        return self.__battery_level

    @battery_level.setter
    def battery_level(self, battery_level):
        self.__battery_level = battery_level

    @property
    def hourly_rate(self):
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, hourly_rate):
        self.__hourly_rate = hourly_rate

    @property
    def is_available(self):
        return self.__is_available

    @is_available.setter
    def is_available(self, is_available):
        self.__is_available = is_available


class CityCar(ElectricCar):
    """
    Дочерний класс CityCar. Наследуется от ElectricCar
    Аттрибуты:
        car_id (int)
        model (str)
        battery_level (int)
        hourly_rate (int)
        is_available (bool)
        max_speed (int)
    """
    def __init__(self, car_id, model, battery_level, hourly_rate, is_available, max_speed):
        super().__init__(car_id, model, battery_level, hourly_rate, is_available)
        self.__max_speed = max_speed

    def calculate_rental_cost(self):
        if self.hourly_rate > 5:
            return 100 * self.hourly_rate
        else:
            return 150 * self.hourly_rate

    def __str__(self):
        return f"Городской электромобиль: {self.model}, Макс. скорость: {self.max_speed} км/ч"

    @property
    def max_speed(self):
        return self.__max_speed

    @max_speed.setter
    def max_speed(self, max_speed):
        self.__max_speed = max_speed


class SUV(ElectricCar):
    """
    Дочерний класс SUV. Наследуется от ElectricCar
    Аттрибуты:
        car_id (int)
        model (str)
        battery_level (int)
        hourly_rate (int)
        is_available (bool)
        towing_capacity (int)
        """
    def __init__(self, car_id, model, battery_level, hourly_rate, is_available, towing_capacity):
        super().__init__(car_id, model, battery_level, hourly_rate, is_available)
        self.__towing_capacity = towing_capacity

    def calculate_rental_cost(self):
        if self.hourly_rate > 7:
            return 120 * self.hourly_rate
        else:
            return 170 * self.hourly_rate

    def __str__(self):
        return f"Внедорожный электромобиль: {self.model}, грузоподъемность: {self.towing_capacity} кг"

    @property
    def towing_capacity(self):
        return self.__towing_capacity

    @towing_capacity.setter
    def towing_capacity(self, towing_capacity):
        self.__towing_capacity = towing_capacity


class LuxuryCar(ElectricCar):
    """
    Дочерний класс SUV. Наследуется от ElectricCar
    Аттрибуты:
        car_id (int)
        model (str)
        battery_level (int)
        hourly_rate (int)
        is_available (bool)
        premium_features (int)
    """
    def __init__(self, car_id, model, battery_level, hourly_rate, is_available, premium_features):
        super().__init__(car_id, model, battery_level, hourly_rate, is_available)
        self.__premium_features = premium_features

    def calculate_rental_cost(self):
        if self.hourly_rate > 5:
            return 350 * self.hourly_rate
        else:
            return 500 * self.hourly_rate

    def __str__(self):
        return f"Городской электромобиль: {self.model}, список премиальных функций: {self.premium_features}"

    @property
    def premium_features(self):
        return self.__premium_features

    @premium_features.setter
    def premium_features(self, premium_features):
        self.__premium_features = premium_features


class Location:
    """
    Класс Location.
    Используется для определения переменной location в классе ChargingStation
    """
    def __init__(self, location_info):
        self.location_info = location_info


class Rentable(abc.ABC):
    """
    интерфейс Rentable для аренды автомобиля
    """
    @abc.abstractmethod
    def rent_car(self, car):
        pass


class Reportable(abc.ABC):
    """
    интерфейс Reportable для генерации отчетов об аренде
    """
    @abc.abstractmethod
    def generate_report(self):
        pass


class LoggingMixin:
    """
    Миксин LoggingMixin, который добавляет функциональность логирования действий с арендой и электромобилями
    """
    def log_action(self, text):
        logger.info(text)


class NotificationMixin:
    """
    Миксин NotificationMixin, который добавляет функциональность отправки уведомлений
    """
    def send_notification(self, text):
        print(text)


class ChargingStation(Rentable, Reportable, LoggingMixin, NotificationMixin):
    """
    Класс ChargingStation
    Атрибуты:
    station_id (int)
    capacity (int)
    location (class Location)
    """
    def __init__(self, station_id, capacity, location: Location):
        self.cars = []
        self.rented_cars = []
        self.station_id = station_id
        self.capacity = capacity
        self.location = location

    def add_car(self, car):
        if len(self.cars) < self.capacity:
            self.cars.append(car)
        else:
            print(f"Станция зарядки {self.station_id} Заполнена")

    def remove_car(self, car):
        if car in self.cars:
            self.cars.remove(car)
        else:
            print(f"В Станции зарядки {self.station_id} такой машины нет")

    def get_available_cars(self):
        return self.cars

    def search_by_model(self, model):
        for car in self.cars:
            if car.model == model:
                return car
        return None

    @check_permissions("verified user")
    def rent_car(self, user_permission, car):
        if car in self.cars:
            self.remove_car(car)
            self.rented_cars.append(car)
            self.log_action(f"Электромобиль {car.model} арендован")
            self.send_notification(f"Ваш электромобиль {car.model} готов к выдаче")
        else:
            self.send_notification("Аренда отменена")

    def generate_report(self):
        report = f"Отчет по аренде:\n" \
                 f"Всего машин: {len(self.cars)}\n" \
                 f"Арендованных машин: {len(self.rented_cars)}"
        logger.info(report)


class ElectricCarFactory:
    """
    Фабричный метод ElectricCarFactory
    """
    def __init__(self):
        self.car_types = {
            "city": CityCar,
            "suv": SUV,
            "luxury": LuxuryCar
        }

    def create_car(self, car_type):
        car_class = self.car_types.get(car_type)
        if car_class:
            return car_class
        else:
            raise ValueError(f"Неизвестный тип: {car_type}")


class Handler:
    """
    Базовый обработчик Handler
    """
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler

    def handle(self, request):
        raise NotImplementedError("Вы должны реализовать этот метод")


class StationOperator(Handler):
    """
    Базовый обработчик StationOperator
    """
    def handle(self, request):
        if request.change_type == "easy":
            print(f"Оператор станции выполнил: {request}")
        elif self.next_handler:
            self.next_handler.handle(request)
        else:
            print(f"Оператор станции не смог выполнить: {request}")


class Manager(Handler):
    """
    Обработчик Manager
    """
    def handle(self, request):
        if request.change_type == "middle":
            print(f"Менеджер выполнил: {request}")
        elif self.next_handler:
            self.next_handler.handle(request)
        else:
            print(f"Менеджер не смог выполнить: {request}")


class Admin(Handler):
    """
    Обработчик Admin
    """
    def handle(self, request):
        print(f"Админ выполнил: {request}")


class RentalProcess(abc.ABC):
    """
    Базовый шаблонный метод RentalProcess
    """
    @abc.abstractmethod
    def rent_car(self):
        pass


class OnlineRentalProcess(RentalProcess):
    """
    Дочерний шаблонный метод OnlineRentalProcess. Наследуется от RentalProcess
    """
    def rent_car(self):
        print("Оформляем онлайн")


class OfflineRentalProcess(RentalProcess):
    """
    Дочерний шаблонный метод OfflineRentalProcess. Наследуется от RentalProcess
    """
    def rent_car(self):
        print("Оформляем офлайн")


def to_dict(data):
    """
    Функция для сериализации data
    """
    return json.dumps(data)


def from_dict(json_data):
    """
    Функция для десериализация json_data
    """
    return json.loads(json_data)


def main():
    el_car_factory = ElectricCarFactory()
    car_1 = el_car_factory.create_car("city")
    car_2 = el_car_factory.create_car("suv")
    car_3 = el_car_factory.create_car("luxury")
    loc = Location("Moscow")
    station_1 = ChargingStation(1, 10, loc)
    station_1.add_car(car_1)
    station_1.add_car(car_2)
    station_1.add_car(car_3)
    station_1.generate_report()

    car_1.model = "Tesla"
    car_2.model = "Tesla X"
    print(car_1.model)
    station_1.remove_car(car_1)
    print(len(station_1.get_available_cars()))
    print(station_1.search_by_model("Tesla X"))
    user_permission_1 = ["verified user"]
    station_1.rent_car(user_permission_1, car_2)


if __name__ == "__main__":
    main()
