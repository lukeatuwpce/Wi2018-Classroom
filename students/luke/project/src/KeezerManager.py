#!/usr/bin/env python3

"""
Keezer management project.  See README.md
"""

import sys
import os
import imp
import glob
import time
import logging
import logging.handlers

from KeezerSensor import KeezerSensor
from KeezerDisplay import KeezerDisplay

POLL_INTERVAL=10

DFLFMT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(DFLFMT)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)

# Concrete sensor and display classes are loaded dynamically.  There are
# a few approaches to this.  In addition to the goergevreilly one copied
# below, there's another example at:
# https://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-modules-or-classes/

# https://www.georgevreilly.com/blog/2016/03/02/PythonImportSubclassFromDynamicPath.html
def import_class(implementation_filename, base_class):
    """ Dynamically import class from filesystem using imp. """


    impl_dir, impl_filename = os.path.split(implementation_filename)
    module_name, _ = os.path.splitext(impl_filename)

    try:
        sys.path.insert(0, impl_dir)
        fp, filename, description = imp.find_module(module_name)
        module = imp.load_module(module_name, fp, filename, description)
        logging.debug(f"trying to import fp {fp} "
                      f" filename {filename} "
                      f" description {description} ")
        for name in dir(module):
            logging.debug(f"name {name}")
            obj = getattr(module, name)
            logging.debug(f"obj {obj}")
            try:
                if (type(obj) == type(base_class)
                        and issubclass(obj, base_class)
                        and obj != base_class):
                    return obj

            except TypeError as excpt:
                """ issubclass will throw TypeError for some imports """
                logging.debug(f"caught {excpt}")

        raise ValueError("No subclass of {0} in {1}".format(
            base_class.__name__, implementation_filename))

    finally:
        sys.path.pop(0)


class KeezerManager:
    """
    Driver class for keezer manager.

    - Load sensor and display modules dynamically.
    - Poll sensors.
    - Pass sensor data to displays.
    """

    def __init__(self):
        """ Load subclasses """
        logging.debug("called")
        self.sensors = []
        self.displays = []

        """ Populate sensors from sensors/ directory"""
        for file in glob.glob("sensors/*.py"):
            logging.debug(f"appending sensor: {file}")
            self.sensors.append(import_class(file, KeezerSensor)())

        """ Populate displays from displays/ directory"""
        for file in glob.glob("displays/*.py"):
            logging.debug(f"appending display: {file}")
            self.displays.append(import_class(file, KeezerDisplay)())


    def run(self):
        """ Main loop: poll sensors and feed to displays """
        logging.debug("called")
        while True:
            loop_start = time.clock()
            logging.debug(f"loop started at {loop_start}")

            for sensor in self.sensors:
                data = sensor.poll()

                for display in self.displays:
                    display.display(data)

            # sleep for remainder of polling interval
            loop_end = time.clock()
            logging.debug(f"loop ended at {loop_end}")
            time_delta = loop_end - loop_start
            sleep_for = POLL_INTERVAL - time_delta
            if sleep_for < 0:
                sleep_for = 0
            logging.debug(f"sleeping for {sleep_for}")
            time.sleep(sleep_for)


if __name__ == "__main__":
    # List registered sensors and displays
    km = KeezerManager()
    for sensor in km.sensors:
        print(f"sensor: {sensor}")
    for display in km.displays:
        print(f"display: {display}")

    km.run()
