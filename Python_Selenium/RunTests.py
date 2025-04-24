import unittest
from SubmissionSuccessValidation import SubmissionSuccessValidation
from ShoppingCartValidation import ShoppingCartValidation
from MandatoryFieldValidation import MandatoryFieldValidation

if __name__ == "__main__":
    # Load test cases
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(MandatoryFieldValidation))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SubmissionSuccessValidation))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ShoppingCartValidation))

    # Run tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
