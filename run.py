import pytest

if __name__ == "__main__":

    # Some colors for terminal output
    BLUE = '\033[1;34m'
    GREEN = '\033[1;32m'
    RED = '\033[1;31;48m'
    END = '\033[0;37m'

    # App name
    app_name = "EDM System Automated Tests"

    print(app_name)
    print(BLUE + '''
       EDM SYSTEM
       _--------_
      |[0]    [0]|
      |    ..    |
       \__====__/
          |  |
       AUTO TESTS
    ''' + END)

    # pytest_args = ['edmauto', '-v']
    pytest_args = ['edmauto', '-k not xbrutforce', '-v']
    pytest.main(pytest_args)
