import pytest
import os


# if __name__ == '__main__':
#     pytest.main(['-sq', '--alluredir', './apitest/allure-results'])
#     os.system(r"allure generate ./apitest/allure-results -o ./apitest/allure-report --clean")
#     os.system(r'allure open ./apitest/allure-report')

def run(id, steps):
    dirs = os.path.abspath(os.path.dirname(__file__)) + '/allure-results/'
    for i in os.listdir(dirs):
        file = os.path.normpath(dirs + i)
        os.remove(file)
    pytest.main(['-sq', '--alluredir', f'./apitest/allure-results'])
    os.system(f"allure generate ./apitest/allure-results -o ./apitest/static/allure-report/{id} --clean")
    # os.system(r'allure open ./apitest/allure-report')


