import random

from django.core.management.base import BaseCommand

from sensors.models import Measurement, Sensor, SensorTypes
from systems.models import HydroSystem
from users.models import User

SENSOR_DESCRIPTIONS = [
    "Middle sensor",
    "Right sensor",
    "Left sensor",
    "Redundant sensor",
    "Important sensor",
]


class Command(BaseCommand):
    help = "Populate database with sample data."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.help)

        # Create user
        user = self.create_superuser()

        # Populate hydro systems
        systems = self.populate_systems(user)

        # Populate sensors
        sensors = self.populate_sensors(systems)

        # Populate measurements
        self.populate_measurements(sensors)

    def create_superuser(self) -> User:
        self.stdout.write("Creating test user.")
        username = "test_user"
        user = User.objects.filter(username=username).first()
        if not user:
            user = User.objects.create_superuser(
                username=username, password="testpassword"
            )

        self.stdout.write("Test user created successfully.")
        return user

    def populate_systems(self, user: User) -> list[HydroSystem]:
        self.stdout.write("Creating 2 test systems.")
        system_1, created = HydroSystem.objects.get_or_create(
            owner=user,
            name="Important hydro system",
            defaults={"description": "Located in building 4 in area F"},
        )
        system_2, created = HydroSystem.objects.get_or_create(
            owner=user,
            name="Alpha system",
            defaults={"description": "Testing system located in basement."},
        )
        self.stdout.write("Hydro systems created successfully.")
        return [system_1, system_2]

    def populate_sensors(self, systems: list[HydroSystem]) -> list[Sensor]:
        self.stdout.write("Creating 5 sensors per hydro system.")
        sensors = []
        for system in systems:
            for i in range(5):
                sensor = Sensor.objects.create(
                    system=system,
                    sensor_type=random.choice(
                        [choice[0] for choice in SensorTypes.choices]
                    ),
                    description=random.choice(SENSOR_DESCRIPTIONS),
                )
                sensors.append(sensor)

        self.stdout.write("Sensors created successfully.")
        return sensors

    def populate_measurements(self, sensors: list[Sensor]):
        self.stdout.write("Creating 10 measurements per sensor.")
        for sensor in sensors:
            for i in range(10):
                Measurement.objects.create(
                    sensor=sensor, value=round(random.uniform(-100, 100), 2)
                )
        self.stdout.write("Measurements created successfully.")
