# Requirements and running tests

The application was developed as part of a master's thesis. It is used to compare the consumption of hardware resources during the execution of automated tests on a sample web application using Selenium, Playwright, and Splinter libraries.

This project is compatible with Python version 3.10.6.

1. It is worth to upgrade system tools firstly:

```bash
python3 -m pip install --upgrade pip
sudo apt update
sudo apt upgrade
```

2. Download the necessary dependencies:

```bash
python3 -m pip install -r requirements.txt
```

3. Choose and download the [ChromeDriver](https://chromedriver.chromium.org/downloads) (for Selenium and Splinter tests), with version depending on your operating system and the version of installed Chrome browser.

4. Install Playwright:

```bash
playwright install
```

5. You can run the test scripts individually to check if all dependencies have been installed correctly:

```bash
python3 selenium_test.py [HEADLESS_MODE]
python3 playwright_test.py [HEADLESS_MODE]
python3 splinter_test.py [HEADLESS_MODE]
```

Where `HEADLESS_MODE` is a value of `True` or `False` - it determines whether the test should be run in `headless` mode or not. `Headless` mode refers to running a web browser without displaying the graphical user interface.

6. To launch the application that executes (in both `headless` and `no headless` modes), measures and manages all the test scripts, run the following command:

```bash
python3 tests_performance_analyser.py
```

7. After executing each of the test scripts, the following files will be generated:
- screenshots of key moments during the test (in the `screenshot` directory and subdirectory with the name of the executed tool)
- logs providing information about successfully completed test cases or encountered errors (in the `logs` directory and subdirectory with the name of the executed tool)


8. After launching the application, which triggers and measures each of the three tools, the results will be generated and saved in a CSV file in directory `performance_logs`.

The following values are measured during the script execution:
- CPU usage before running test
- memory usage before running test
- CPU usage (measured every second)
- CPU context switches per second (measured every second)
- CPU interrupts (measured every second)
- memory usage (measured every second)
- memory resident set size (measured every second)
- disk IO read/write bytes during test execution
- duration time of test execution

9. There is an option to run a script that generates plots based on data from CSV files. However, for the script to work, you need to manually copy all the data into directory with name initialised in `ALL_RESULTS_DIRECTORY` variable in `test_settings.py` file.
