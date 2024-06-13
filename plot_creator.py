from test_settings import *
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
import statistics
import csv
import os

results = {
    SELENIUM: {
        HEADLESS: {
            WINDOWS: [],
            LINUX: [],
            MACOS: [],
        },
        NOHEADLESS: {
            WINDOWS: [],
            LINUX: [],
            MACOS: [],
        },
    },
    PLAYWRIGHT: {
        HEADLESS: {
            WINDOWS: [],
            LINUX: [],
            MACOS: [],
        },
        NOHEADLESS: {
            WINDOWS: [],
            LINUX: [],
            MACOS: [],
        },
    },
    SPLINTER: {
        HEADLESS: {
            WINDOWS: [],
            LINUX: [],
            MACOS: [],
        },
        NOHEADLESS: {
            WINDOWS: [],
            LINUX: [],
            MACOS: [],
        },
    },
}

def process_csv(file_path):
    """
    Processes a CSV file and stores its contents in the appropriate dictionary.

    The CSV file is identified based on its filename,
    which includes information about the tool, mode, and system.

    Args:
        :file_path: (str) - The path to the CSV file to be processed.
    """
    tool, mode, system = os.path.basename(file_path).split('-')[0].replace('_test', '').split('_')

    data = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            key = row[0]
            if len(row) == 2:
                value = row[1]
            else:
                value = row[1:]
            data[key] = value
    
    results[tool][mode][system].append(data)

def read_all_data():
    """
    Reads all CSV files in a single common directory and processes them.
    This method assumes that all CSV files are located in one common directory,
    because the filename contains the necessary information about the tool,
    mode, and system, so there can be in one directory.
    """
    for filename in os.listdir(ALL_RESULTS_DIRECTORY):
        if filename.endswith(".csv"):
            file_path = os.path.join(ALL_RESULTS_DIRECTORY, filename)
            process_csv(file_path)

    print("Total amount of read data:")

    for tool in [SELENIUM, PLAYWRIGHT, SPLINTER]:
        for mode in [HEADLESS, NOHEADLESS]:
            for platform in [WINDOWS, LINUX, MACOS]:
                print(
                    f"{tool} tests in {mode} mode run on {platform}: "
                    f"{len(results[tool][mode][platform])}"
                )

def create_plots_duration_time(mode, platform):
    print(f"Generating a plot comparing the duration of tests in {mode} mode on {platform}.")
    duration_time_selenium = [float(result['duration_time']) for result in results[SELENIUM][mode][platform]]
    duration_time_playwright = [float(result['duration_time']) for result in results[PLAYWRIGHT][mode][platform]]
    duration_time_splinter = [float(result['duration_time']) for result in results[SPLINTER][mode][platform]]

    x = range(1, 51)
    plt.figure(figsize=(15, 6))
    plt.scatter(x, duration_time_selenium, label='Selenium')
    plt.scatter(x, duration_time_playwright, label='Playwright')
    plt.scatter(x, duration_time_splinter, label='Splinter')
    plt.xlabel('Test number', fontsize=14) 
    plt.ylabel('Duration (seconds)', fontsize=14)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    plt.yticks(np.arange(0, 19, 2))
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    plt.grid(True)
    plt.show()

def create_plots_cpu_usage(mode, platform):
    print(
        f"Generating a plot comparing the CPU usage during tests in {mode} mode on {platform}."
    )
    results_selenium = [result['cpu_percentages'] for result in results[SELENIUM][mode][platform]]
    results_playwright = [result['cpu_percentages'] for result in results[PLAYWRIGHT][mode][platform]]
    results_splinter = [result['cpu_percentages'] for result in results[SPLINTER][mode][platform]]
    cpu_usage_selenium = [statistics.mean(list(map(float, result))) for result in results_selenium]
    cpu_usage_playwright = [statistics.mean(list(map(float, result))) for result in results_playwright]
    cpu_usage_splinter = [statistics.mean(list(map(float, result))) for result in results_splinter]

    plt.figure(figsize=(10, 6))
    plt.boxplot(
        [cpu_usage_selenium, cpu_usage_playwright, cpu_usage_splinter],
        labels=['Selenium', 'Playwright', 'Splinter'],
    )
    plt.ylabel('CPU usage (percentage)', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    plt.grid(True)
    plt.show()

def create_plots_initial_spike_cpu_usage(mode, platform):
    print(
        f"Generating a plot comparing the initial CPU usage spike during tests in {mode} mode on {platform}."
    )
    spike_cpu_selenium = [float(result['cpu_percentages'][0]) - float(result['cpu_usage_before']) for result in results[SELENIUM][mode][platform]]
    spike_cpu_playwright = [float(result['cpu_percentages'][0]) - float(result['cpu_usage_before']) for result in results[PLAYWRIGHT][mode][platform]]
    spike_cpu_splinter = [float(result['cpu_percentages'][0]) - float(result['cpu_usage_before']) for result in results[SPLINTER][mode][platform]]

    plt.figure(figsize=(10, 6))
    plt.boxplot([spike_cpu_selenium, spike_cpu_playwright, spike_cpu_splinter], labels=['Selenium', 'Playwright', 'Splinter'])
    plt.ylabel('Initial CPU usage spike (percentage)', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    plt.grid(True)
    plt.show()

def create_plots_context_switches(mode, platform):
    print(
        f"Generating a plot comparing the number of CPU context switches during tests in {mode} mode on {platform}."
    )
    results_selenium = [result['cpu_context_switches'] for result in results[SELENIUM][mode][platform]]
    results_playwright = [result['cpu_context_switches'] for result in results[PLAYWRIGHT][mode][platform]]
    results_splinter = [result['cpu_context_switches'] for result in results[SPLINTER][mode][platform]]
    context_switches_selenium = []
    context_switches_playwright = []
    context_switches_splinter = []
    for result in results_selenium:
        difference_result = [abs(int(result[i]) - int(result[i-1])) for i in range(1, len(result))]
        context_switches_selenium.append(statistics.mean(list(map(float, difference_result))))
    for result in results_playwright:
        difference_result = [abs(int(result[i]) - int(result[i-1])) for i in range(1, len(result))]
        context_switches_playwright.append(statistics.mean(list(map(float, difference_result))))
    for result in results_splinter:
        difference_result = [abs(int(result[i]) - int(result[i-1])) for i in range(1, len(result))]
        context_switches_splinter.append(statistics.mean(list(map(float, difference_result))))

    plt.figure(figsize=(10, 6))
    plt.boxplot([context_switches_selenium, context_switches_playwright, context_switches_splinter], labels=['Selenium', 'Playwright', 'Splinter'])
    plt.ylabel('Number of CPU context switches', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(True)
    plt.show()

def create_plots_cpu_interrupts(mode, platform):
    print(
        f"Generating a plot comparing the number of CPU interrupts during tests in {mode} mode on {platform}."
    )
    results_selenium = [result['cpu_interrupts'] for result in results[SELENIUM][mode][platform]]
    results_playwright = [result['cpu_interrupts'] for result in results[PLAYWRIGHT][mode][platform]]
    results_splinter = [result['cpu_interrupts'] for result in results[SPLINTER][mode][platform]]
    cpu_interrupts_selenium = []
    cpu_interrupts_playwright = []
    cpu_interrupts_splinter = []
    for result in results_selenium:
        difference_result = [abs(int(result[i]) - int(result[i-1])) for i in range(1, len(result))]
        cpu_interrupts_selenium.append(statistics.mean(list(map(float, difference_result))))
    for result in results_playwright:
        difference_result = [abs(int(result[i]) - int(result[i-1])) for i in range(1, len(result))]
        cpu_interrupts_playwright.append(statistics.mean(list(map(float, difference_result))))
    for result in results_splinter:
        difference_result = [abs(int(result[i]) - int(result[i-1])) for i in range(1, len(result))]
        cpu_interrupts_splinter.append(statistics.mean(list(map(float, difference_result))))

    plt.figure(figsize=(10, 6))
    plt.boxplot([cpu_interrupts_selenium, cpu_interrupts_playwright, cpu_interrupts_splinter], labels=['Selenium', 'Playwright', 'Splinter'])
    plt.ylabel('Number of CPU interrupts', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(True)
    plt.show()

def create_plots_memory_usage(mode, platform):
    print(
        f"Generating a plot comparing the memory usage during tests in {mode} mode on {platform}."
    )
    results_selenium = [result['memory_percentages'] for result in results[SELENIUM][mode][platform]]
    results_playwright = [result['memory_percentages'] for result in results[PLAYWRIGHT][mode][platform]]
    results_splinter = [result['memory_percentages'] for result in results[SPLINTER][mode][platform]]
    memory_usage_selenium = [statistics.mean(list(map(float, result))) for result in results_selenium]
    memory_usage_playwright = [statistics.mean(list(map(float, result))) for result in results_playwright]
    memory_usage_splinter = [statistics.mean(list(map(float, result))) for result in results_splinter]

    plt.figure(figsize=(10, 6))
    plt.boxplot([memory_usage_selenium, memory_usage_playwright, memory_usage_splinter], labels=['Selenium', 'Playwright', 'Splinter'])
    plt.ylabel('RAM usage (percentage)', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    plt.grid(True)
    plt.show()

def create_plots_initial_spike_memory_usage(mode, platform):
    print(
        f"Generating a plot comparing the initial memory usage spike during tests in {mode} mode on {platform}."
    )
    spike_memory_selenium = [float(result['memory_percentages'][0]) - float(result['memory_usage_before']) for result in results[SELENIUM][mode][platform]]
    spike_memory_playwright = [float(result['memory_percentages'][0]) - float(result['memory_usage_before']) for result in results[PLAYWRIGHT][mode][platform]]
    spike_memory_splinter = [float(result['memory_percentages'][0]) - float(result['memory_usage_before']) for result in results[SPLINTER][mode][platform]]

    plt.figure(figsize=(10, 6))
    plt.boxplot([spike_memory_selenium, spike_memory_playwright, spike_memory_splinter], labels=['Selenium', 'Playwright', 'Splinter'])
    plt.ylabel('Initial RAM usage spike (percentage)', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    plt.grid(True)
    plt.show()

def create_plots_rss_size(mode, platform):
    print(
        f"Generating a plot comparing the RAM usage by process during tests in {mode} mode on {platform}."
    )
    results_selenium = [result['memory_resident_set_size_bytes'] for result in results[SELENIUM][mode][platform]]
    results_playwright = [result['memory_resident_set_size_bytes'] for result in results[PLAYWRIGHT][mode][platform]]
    results_splinter = [result['memory_resident_set_size_bytes'] for result in results[SPLINTER][mode][platform]]
    rss_size_selenium = [statistics.mean(list(map(float, result))) for result in results_selenium]
    rss_size_playwright = [statistics.mean(list(map(float, result))) for result in results_playwright]
    rss_size_splinter = [statistics.mean(list(map(float, result))) for result in results_splinter]

    plt.figure(figsize=(10, 6))
    plt.boxplot([rss_size_selenium, rss_size_playwright, rss_size_splinter], labels=['Selenium', 'Playwright', 'Splinter'])
    plt.ylabel('RAM usage by process (bytes)', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    plt.gca().ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    plt.show()

def create_plots_disk_io_read(mode, platform):
    print(
        f"Generating a plot comparing the data read from disk during tests in {mode} mode on {platform}."
    )
    disk_io_read_selenium = [int(result['disk_io_read_bytes']) for result in results[SELENIUM][mode][platform]]
    disk_io_read_playwright = [int(result['disk_io_read_bytes']) for result in results[PLAYWRIGHT][mode][platform]]
    disk_io_read_splinter = [int(result['disk_io_read_bytes']) for result in results[SPLINTER][mode][platform]]

    plt.figure(figsize=(10, 6))
    plt.boxplot([disk_io_read_selenium, disk_io_read_playwright, disk_io_read_splinter], labels=['Selenium', 'Playwright', 'Splinter'])
    plt.yscale('symlog')
    plt.ylabel('Data read from disk (bytes)', fontsize=14)
    plt.yticks(np.logspace(0, 9, num=10))
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(True)
    plt.show()

def create_plots_disk_io_write(mode, platform):
    print(
        f"Generating a plot comparing the data written from disk during tests in {mode} mode on {platform}."
    )
    disk_io_write_selenium = [int(result['disk_io_write_bytes']) for result in results[SELENIUM][mode][platform]]
    disk_io_write_playwright = [int(result['disk_io_write_bytes']) for result in results[PLAYWRIGHT][mode][platform]]
    disk_io_write_splinter = [int(result['disk_io_write_bytes']) for result in results[SPLINTER][mode][platform]]

    plt.figure(figsize=(10, 6))
    plt.boxplot([disk_io_write_selenium, disk_io_write_playwright, disk_io_write_splinter], labels=['Selenium', 'Playwright', 'Splinter'])
    plt.yscale('symlog')
    plt.ylabel('Data written to disk (bytes)', fontsize=14)
    plt.yticks(np.logspace(0, 9, num=10))
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    read_all_data()

    modes = [HEADLESS, NOHEADLESS]
    platforms = [WINDOWS, LINUX, MACOS]

    """
    Duration time
    """
    # Duration time comparison
    for platform in platforms:
        for mode in modes:
            create_plots_duration_time(mode, platform)

    """
    CPU
    """

    # CPU usage comparison
    for platform in platforms:
        for mode in modes:
            create_plots_cpu_usage(mode, platform)

    # Initial spike in CPU usage comparison
    for platform in platforms:
        for mode in modes:
            create_plots_initial_spike_cpu_usage(mode, platform)

    # Context switches comparison
    for platform in platforms:
        for mode in modes:
            create_plots_context_switches(mode, platform)

    # CPU interrupts comparison
    for platform in platforms:
        for mode in modes:
            create_plots_cpu_interrupts(mode, platform)

    """
    Memory
    """

    # Memory usage comparison
    for platform in platforms:
        for mode in modes:
            create_plots_memory_usage(mode, platform)

    # Initial spike in memory usage comparison
    for platform in platforms:
        for mode in modes:
            create_plots_initial_spike_memory_usage(mode, platform)

    # RSS memory size comparison
    for platform in platforms:
        for mode in modes:
            create_plots_rss_size(mode, platform)

    """
    Disk
    """

    # Disk IO read bytes comparison
    for platform in platforms:
        for mode in modes:
            create_plots_disk_io_read(mode, platform)

    # Disk IO write bytes comparison
    for platform in platforms:
        for mode in modes:
            create_plots_disk_io_write(mode, platform)
