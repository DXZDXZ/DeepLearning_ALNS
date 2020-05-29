import os

from project_root_path import get_project_root_path

SEED = 456322

SIZE = 50
CAPACITY = 40
NUMBER_OF_DEPOTS = 1

NUMBER_OF_INSTANCES = 1

ITERATIONS = 1000
WEIGHTS = [1, 1, 1, 1]
OPERATOR_DECAY = 0.8
COLLECT_STATISTICS = True

DEGREE_OF_DESTRUCTION = 0.35
DETERMINISM = 18

START_TEMPERATURE_CONTROL = 0.05
COOLING_RATE = 0.99995
END_TEMPERATURE = 0.01

ROOT_PATH = get_project_root_path()
FILE_PATH = ROOT_PATH \
            + "/data/{0}inst_{1}nod_{2}cap_{3}dep_{4}iter_{5}decay_{6}destr_{7}determ.pickle" \
            .format(NUMBER_OF_INSTANCES, SIZE, CAPACITY, NUMBER_OF_DEPOTS,
                    ITERATIONS, OPERATOR_DECAY, DEGREE_OF_DESTRUCTION, DETERMINISM)
FILE_MODE = 'wb'
