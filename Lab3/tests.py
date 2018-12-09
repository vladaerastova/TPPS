import unittest
from mock import mock

from main import City, BestLocationCalculator, Parser


class CityMethods(unittest.TestCase):
    def test__init__with_correct_data(self):
        dx, dy = 1, 2
        city = City(dx, dy)
        self.assertEquals(city.dx, dx)
        self.assertEquals(city.dy, dy)

    def test__init__in_extreme_max_case_data(self):
        dx, dy = City.MAX, City.MAX
        city = City(dx, dy)
        self.assertEquals(city.dx, dx)
        self.assertEquals(city.dy, dy)

    def test__init__in_extreme_min_case_data(self):
        dx, dy = City.MIN, City.MIN
        city = City(dx, dy)
        self.assertEquals(city.dx, dx)
        self.assertEquals(city.dy, dy)

    def test__init__with_lower_x_data(self):
        dx, dy = City.MIN - 1, 2
        with self.assertRaises(Exception) as e:
            city = City(dx, dy)
        error_msg = e.exception
        self.assertEquals(str(error_msg), City.INCORRECT_CITY_SIZE_ERROR_MSG)

    def test__init__with_upper_x_data(self):
        dx, dy = City.MAX + 1, 2
        with self.assertRaises(Exception) as e:
            city = City(dx, dy)
        error_msg = e.exception
        self.assertEquals(str(error_msg), City.INCORRECT_CITY_SIZE_ERROR_MSG)

    def test__init__with_lower_y_data(self):
        dx, dy = 2, City.MIN - 1
        with self.assertRaises(Exception) as e:
            city = City(dx, dy)
        error_msg = e.exception
        self.assertEquals(str(error_msg), City.INCORRECT_CITY_SIZE_ERROR_MSG)

    def test__init__with_upper_y_data(self):
        dx, dy = 2, City.MAX + 1
        with self.assertRaises(Exception) as e:
            city = City(dx, dy)
        error_msg = e.exception
        self.assertEquals(str(error_msg), City.INCORRECT_CITY_SIZE_ERROR_MSG)

    def test_calculate_shops(self):
        dx, dy = 5, 5
        city = City(dx, dy)
        city.set_coffee_shop(1, 1)
        city.set_coffee_shop(2, 4)

        city.calculate_shops(1, 1, 1)
        self.assertEquals(city.max_available_shops, 0)

        city.clear_shops()
        city.calculate_shops(1, 1, 2)
        self.assertEquals(city.max_available_shops, 2)

        city.clear_shops()
        city.calculate_shops(1, 1, 20)
        self.assertEquals(city.max_available_shops, 2)

        city.clear_shops()
        city.calculate_shops(2, 0, 1)
        self.assertEquals(city.max_available_shops, 0)

        city.clear_shops()
        city.calculate_shops(2, 0, 2)
        self.assertEquals(city.max_available_shops, 1)

        city.clear_shops()
        city.calculate_shops(2, 0, 3)
        self.assertEquals(city.max_available_shops, 1)

        city.clear_shops()
        city.calculate_shops(2, 0, 4)
        self.assertEquals(city.max_available_shops, 2)

    def test_get_optimal_location(self):
        dx, dy = 4, 4
        city = City(dx, dy)
        city.set_coffee_shop(1, 1)
        city.set_coffee_shop(1, 2)
        city.set_coffee_shop(3, 3)
        city.set_coffee_shop(4, 4)
        city.set_coffee_shop(2, 4)

        actual_max_shops, actual_best_x, actual_best_y = city.get_optimal_location(1)
        self.assertEqual(actual_max_shops, 3)
        self.assertEqual(actual_best_x, 3)
        self.assertEqual(actual_best_y, 4)

        actual_max_shops, actual_best_x, actual_best_y = city.get_optimal_location(2)
        self.assertEqual(actual_max_shops, 4)
        self.assertEqual(actual_best_x, 2)
        self.assertEqual(actual_best_y, 2)

        actual_max_shops, actual_best_x, actual_best_y = city.get_optimal_location(4)
        self.assertEqual(actual_max_shops, 5)
        self.assertEqual(actual_best_x, 3)
        self.assertEqual(actual_best_y, 1)

    def test_check_available_with_available_shops(self):
        dx, dy = 2, 2
        city = City(dx, dy)
        self.assertEquals(city.check_available(0, 0), True)
        self.assertEquals(city.check_available(dx - 1, dy - 1), True)

    def test_set_coffee_shop_with_correct_location(self):
        dx, dy = 2, 3
        city = City(dx, dy)
        city.set_coffee_shop(dx, 1)
        city.set_coffee_shop(1, dy)
        self.assertEquals(city.all_shops, 2)

    def test_check_available_with_unavailable_shops(self):
        dx, dy = 2, 2
        city = City(dx, dy)
        self.assertEquals(city.check_available(dx, dy - 1), False)
        self.assertEquals(city.check_available(dx - 1, dy), False)
        self.assertEquals(city.check_available(-1, dy - 1), False)
        self.assertEquals(city.check_available(dx - 1, -1), False)

    def test_set_coffee_shop_with_incorrect_x_location(self):
        dx, dy = 2, 3
        city = City(dx, dy)
        with self.assertRaises(Exception) as e:
            city.set_coffee_shop(dx + 1, dy)
        error_msg = e.exception
        self.assertEquals(str(error_msg), City.INCORRECT_SHOP_LOCATION_ERROR_MSG)

    def test_set_coffee_shop_with_incorrect_x_location2(self):
        dx, dy = 2, 3
        city = City(dx, dy)
        with self.assertRaises(Exception) as e:
            city.set_coffee_shop(-1, dy)
        error_msg = e.exception
        self.assertEquals(str(error_msg), City.INCORRECT_SHOP_LOCATION_ERROR_MSG)

    def test_set_coffee_shop_with_incorrect_y_location(self):
        dx, dy = 2, 3
        city = City(dx, dy)
        with self.assertRaises(Exception) as e:
            city.set_coffee_shop(dx, dy + 1)
        error_msg = e.exception
        self.assertEquals(str(error_msg), City.INCORRECT_SHOP_LOCATION_ERROR_MSG)

    def test_set_coffee_shop_with_incorrect_y_location2(self):
        dx, dy = 2, 3
        city = City(dx, dy)
        with self.assertRaises(Exception) as e:
            city.set_coffee_shop(dx, -1)
        error_msg = e.exception
        self.assertEquals(str(error_msg), City.INCORRECT_SHOP_LOCATION_ERROR_MSG)

    def test_set_coffee_shop_with_two_shops_with_the_same_location(self):
        dx, dy = 2, 3
        city = City(dx, dy)
        city.set_coffee_shop(dx, 1)
        city.set_coffee_shop(dx, 1)
        self.assertEquals(city.all_shops, 1)


class BestLocationCalculatorMethods(unittest.TestCase):
    def test_set_city(self):
        calculator = BestLocationCalculator()
        city = City(2, 2)
        calculator.set_city(city)
        self.assertEqual(calculator.city, city)

    def test_add_coffee_shop(self):
        calculator = BestLocationCalculator()
        calculator.add_coffee_shop(2, 2)
        self.assertEqual(calculator.coffee_shops.__len__(), 1)

    def test_add_query(self):
        calculator = BestLocationCalculator()
        calculator.add_query(1)
        self.assertEqual(calculator.queries.__len__(), 1)

    def test_build_result(self):
        calculator = BestLocationCalculator()
        calculator.build_result((1, 2, 3))
        calculator.build_result((2, 3, 3))
        self.assertEqual(calculator.result, '1(2,3)\n2(3,3)\n')

    def test_calculate(self):
        dx, dy = 4, 4
        city = City(dx, dy)

        calculator = BestLocationCalculator()
        calculator.set_city(city)
        calculator.add_coffee_shop(1, 1)
        calculator.add_coffee_shop(1, 2)
        calculator.add_coffee_shop(3, 3)
        calculator.add_coffee_shop(4, 4)
        calculator.add_coffee_shop(2, 4)
        calculator.add_query(1)
        calculator.add_query(2)
        calculator.add_query(4)
        calculator.calculate()
        self.assertEqual(calculator.result, '3(3,4)\n4(2,2)\n5(3,1)\n')


class ParserMethods(unittest.TestCase):
    CORRECT_INPUT_FILE = '4 4 5 3\n1 1\n1 2\n3 3\n4 4\n2 4\n1\n2\n4\n0 0 0 0'
    INCORRECT_INPUT_FILE = '4 4 3\n1 1\n1 2\n3 3\n4 4\n2 4\n1\n2\n4\n0 0 0 0'
    INCORRECT_NUMBER_OF_QUERIES_INPUT_FILE = '4 4 5 21\n1 1\n1 2\n3 3\n4 4\n2 4\n1\n2\n4\n0 0 0 0'

    def test_parse_with_incorrect_input_file(self):
        mock_open = mock.mock_open(read_data=self.INCORRECT_INPUT_FILE)
        with mock.patch('main.open', mock_open, create=True):
            with self.assertRaises(Exception) as e:
                parser = Parser()
                parser.parse('')
        error_msg = e.exception
        self.assertEquals(str(error_msg), Parser.INCORRECT_FORMAT_OF_FILE_ERROR_MSG)

    def test_parse_with_incorrect_number_of_queries(self):
        mock_open = mock.mock_open(read_data=self.INCORRECT_NUMBER_OF_QUERIES_INPUT_FILE)
        with mock.patch('main.open', mock_open, create=True):
            with self.assertRaises(Exception) as e:
                parser = Parser()
                parser.parse('')
        error_msg = e.exception
        self.assertEquals(str(error_msg), Parser.INCORRECT_NUMBER_OF_QUERIES_ERROR_MSG)

    def test_parse_correct_input_file(self):
        mock_open = mock.mock_open(read_data=self.CORRECT_INPUT_FILE)
        with mock.patch('main.open', mock_open, create=True):
            parser = Parser()
            parser.parse('')

        self.assertEqual(parser.cases_list.__len__(), 1)
        self.assertEqual(parser.cases_list[0].city.dx, 4)
        self.assertEqual(parser.cases_list[0].city.dy, 4)
        self.assertEquals(parser.cases_list[0].coffee_shops.__len__(), 5)
        self.assertIn((1, 1), parser.cases_list[0].coffee_shops)
        self.assertIn((1, 2), parser.cases_list[0].coffee_shops)
        self.assertIn((3, 3), parser.cases_list[0].coffee_shops)
        self.assertIn((4, 4), parser.cases_list[0].coffee_shops)
        self.assertIn((2, 4), parser.cases_list[0].coffee_shops)
        self.assertEquals(parser.cases_list[0].queries.__len__(), 3)
        self.assertIn(1, parser.cases_list[0].queries)
        self.assertIn(2, parser.cases_list[0].queries)
        self.assertIn(4, parser.cases_list[0].queries)

if __name__ == '__main__':
    unittest.main()