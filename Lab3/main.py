class City:
    MIN = 1
    MAX = 1000

    def __init__(self, dx, dy):
        if self.MIN > dx or dx > self.MAX or self.MIN > dy or dy > self.MAX:
            raise Exception('Incorrect city size')
        self.dx = dx
        self.dy = dy
        self.city = [[0 for j in range(dy)] for i in range(dx)]
        self.max_available_shops = 0
        self.all_shops = 0
        self.i = 0

    def set_coffee_shop(self, x, y):
        if self.MIN > x or x > self.dx or self.MIN > y or y > self.dy:
            raise Exception('Incorrect shop location')
        self.city[x - 1][y - 1] = -1  # mark that the cell is coffee shop
        self.all_shops += 1

    def get_optimal_location(self, query):
        for i in range(self.dx):
            for j in range(self.dy):
                if self.city[i][j] != -1:
                    self.calculate_shops(i, j, query)
                    self.city[i][j] = self.max_available_shops
                    self.clear_shops()
        return self.best_location()

    def best_location(self):
        max_shops = -1
        best_y = -1
        best_x = -1
        for i in range(self.dx):
            for j in range(self.dy):
                if self.city[i][j] > max_shops:
                    max_shops, best_x, best_y = self.city[i][j], i, j
                if self.city[i][j] == max_shops:
                    if j < best_y:
                        best_y, best_x = j, i
        return max_shops, best_x + 1, best_y + 1

    def calculate_shops(self, i, j, query):
        if self.max_available_shops == self.all_shops:  # prevent situation when query is big and city is small
            return
        if self.city[i][j] == -1:  # if the coffee shop is reached
            self.max_available_shops += 1
            self.city[i][j] = -2  # mark that the shop is counted
        if query == 0:  #
            return
        if self.check_available(i - 1, j):
            self.calculate_shops(i - 1, j, query - 1)
        if self.check_available(i + 1, j):
            self.calculate_shops(i + 1, j, query - 1)
        if self.check_available(i, j - 1):
            self.calculate_shops(i, j - 1, query - 1)
        if self.check_available(i, j + 1):
            self.calculate_shops(i, j + 1, query - 1)
        self.i +=1

    def check_available(self, i, j):
        if i < 0 or i >= self.dx or j < 0 or j >= self.dy:
            return False
        return True

    def clear_max_values(self):
        for i in range(self.dx):
            for j in range(self.dy):
                if self.city[i][j] > 0:
                    self.city[i][j] = 0

    def clear_shops(self):
        for i in range(self.dx):
            for j in range(self.dy):
                if self.city[i][j] == -2:
                    self.city[i][j] = -1
        self.max_available_shops = 0


class BestLocationCalculator:
    MIN_Q = 0
    MAX_Q = 106

    def __init__(self):
        self.city = None
        self.coffee_shops = []
        self.queries = []
        self.result = ''

    def build_result(self, *args):
        max_value, x, y = args[0]
        self.result += '{}({},{})\n'.format(max_value, x, y)

    def get_result(self):
        return self.result

    def set_city(self, city):
        self.city = city

    def add_coffee_shop(self, x, y):
        self.coffee_shops.append(tuple((x, y)))

    def set_coffee_shops(self):
        for shop in self.coffee_shops:
            self.city.set_coffee_shop(shop[0], shop[1])

    def add_query(self, query):
        if self.MIN_Q > query > self.MAX_Q:
            raise Exception
        self.queries.append(query)

    def calculate(self):
        self.set_coffee_shops()
        for i in self.queries:
            self.build_result(self.city.get_optimal_location(i))
            self.city.clear_max_values()

    def __str__(self):
        return self.result


class Parser:
    def __init__(self):
        self.MIN_N = 0
        self.MAX_N = 105
        self.MIN_Q = 1
        self.MAX_Q = 20
        self.cases_list = []

    def parse(self, file):
        with open(file, 'r') as file:
            while True:
                first_line = list(map(int, file.readline().split(' ')))
                if len(first_line) != 4:
                    raise Exception('Incorrect format of the input file')
                if first_line == [0] * 4:
                    return self.cases_list
                calculator = BestLocationCalculator()
                calculator.set_city(City(first_line[0], first_line[1]))
                if not (self.MIN_N < first_line[2] < self.MAX_N):
                    raise Exception('Incorrect number of cofee shops')
                if not (self.MIN_Q < first_line[3] < self.MAX_Q):
                    raise Exception('Incorrect number of queries')

                for i in range(first_line[2]):
                    shop_location = list(map(int, file.readline().split(' ')))
                    if len(shop_location) != 2:
                        raise Exception('Shop location should consist of two integers')
                    calculator.add_coffee_shop(shop_location[0], shop_location[1])

                for i in range(first_line[3]):
                    query = list(map(int, file.readline().split(' ')))
                    if len(query) != 1:
                        raise Exception('Incorrect query')
                    calculator.add_query(query[0])

                self.cases_list.append(calculator)


def main():
    try:
        parser = Parser()
        cases_list = parser.parse('1.txt')
        case_number = 1
        for calc in cases_list:
            calc.calculate()
            print('Case namber: {}\n'.format(case_number))
            print(calc.get_result())
            case_number += 1
    except ValueError:
        print('Incorrect format of input file')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
