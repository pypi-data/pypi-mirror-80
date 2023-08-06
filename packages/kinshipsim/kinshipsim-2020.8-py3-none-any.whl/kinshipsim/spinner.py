"""
Kinship simulation, Spinner class:
A command line spinner that provides visual feedback for the execution of the tasks.
The original code was written by Ruslan Dautkhanov and it is available at
https://github.com/Tagar/stuff/blob/master/spinner.py

"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

import sys
import threading
import itertools
import time


class Spinner:

    def __init__(self, message: str, delay=0.2):
        """
        Initialize the settings of the spinner such as the prompted message and the delay time to update the spinner.

        :param str message : The message prompted when launching the spinner.
        :param float delay : The time delay to update the spinner.
        """

        self.spinner = itertools.cycle(['-', '\\', '|', '/'])  # spinner sequence symbols
        self.delay = delay
        self.busy = False
        self.spinner_visible = False
        sys.stdout.write(message)

    def write_next(self):
        """
        Update the spinner symbol to the next in the sequence.
        """

        with self._screen_lock:
            if not self.spinner_visible:
                sys.stdout.write(next(self.spinner))
                self.spinner_visible = True
                sys.stdout.flush()

    def remove_spinner(self, cleanup=False):
        """
        Remove the spinner from the screen.

        :param bool cleanup : Remove last shown symbol.
        """

        with self._screen_lock:
            if self.spinner_visible:
                sys.stdout.write('\b')
                self.spinner_visible = False
                if cleanup:
                    sys.stdout.write(' ')  # overwrite spinner with blank
                    #  sys.stdout.write('\r')
                sys.stdout.flush()

    def spinner_task(self):
        """
         Defines the task performed by the spinner, i.e. update symbol, pause, remove last symbol and loop.
        """

        while self.busy:
            self.write_next()
            time.sleep(self.delay)
            self.remove_spinner()

    def __enter__(self):
        """
        Start the spinner.
        """

        if sys.stdout.isatty():
            self._screen_lock = threading.Lock()
            self.busy = True
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def __exit__(self, exception, value, tb):
        """
        Stop the spinner.

        :param exception : Thread parameter for exceptions.
        :param value : Thread parameter.
        :param tb : Thread parameter.
        """
        if sys.stdout.isatty():
            self.busy = False
            self.remove_spinner(cleanup=True)
        else:
            sys.stdout.write('\b')
            sys.stdout.flush()
