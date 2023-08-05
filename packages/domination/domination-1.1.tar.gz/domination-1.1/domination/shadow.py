"""
Print to logging.INFO numbers from 1 to LEET (1337)
replace the number by "Sha" if it's a multiple of 3
replace the number by "Dow" if it's a multiple of 5
replace the number by "ShaDow" if it's a multiple of 3 and 5
"""
import logging


class ShaDow:
    """
    Categorize and returns 'Sha', 'Dow', 'Shadow', 'Incompatible' using worker method.
    """

    @staticmethod
    def evaluate(number: int) -> str:
        """Categorize input number"""
        if number % 15 == 0:
            return 'ShaDow'
        if number % 3 == 0:
            return 'Sha'
        if number % 5 == 0:
            return 'Dow'
        return str('Incompatible')

    def worker(self, i: int) -> str:
        """Run categorization and log result"""
        evaluate = self.evaluate(i)
        logging.info(evaluate)
        return evaluate

    def generator(self, limit: int):
        """generator"""
        for i in range(1, limit + 1):
            self.worker(i)
