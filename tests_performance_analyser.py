from test_settings import *
from datetime import datetime as dt
import subprocess
import platform
import psutil
import time
import csv
import os


def get_operating_system_name(separator=" "):
    """
    Returns a string representing the current operating system's name and release.

    Args:
        :separator: (str) - A string used to separate the operating system name and release.
    """
    return f"{platform.system()}{separator}{platform.release()}"

def get_current_datetime():
    """
    Returns a string representing the current date and time in two formats -
    human readable and format prepared to use in the filename.

    Args:
        :separator: (str) - A string used to separate the date and time.
    """
    current_datetime = dt.now()
    return current_datetime.strftime(f"%Y-%m-%d %H:%M:%S"), current_datetime.strftime(f"%Y%m%d_%H%M%S")

def run_script(script_path, headless_mode):
    """
    Executes the specified script and monitors its resource usage in real-time.

    Args:
        :script_path: (str) - The path to the script to be executed.
        :headless_mode: (bool) - Specifies whether the script should run in headless mode.
    """
    cpu_percentages = []
    cpu_context_switches = []
    cpu_interrupts = []
    memory_percentages = []
    memory_resident_set_size_bytes = []
    disk_io_read_bytes = []
    disk_io_write_bytes = []
    cpu_usage_before = round(psutil.cpu_percent(interval=1), 1)
    memory_usage_before = round(psutil.virtual_memory().percent, 1)
    command = f"python3 {script_path} {headless_mode}"

    start_time = time.time()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    try:
        while process.poll() is None:
            current_cpu_percentage = round(psutil.cpu_percent(interval=1), 1)
            cpu_percentages.append(current_cpu_percentage)

            cpu_context_switches.append(psutil.cpu_stats().ctx_switches)

            cpu_interrupts.append(psutil.cpu_stats().interrupts)

            current_memory_percentage = round(psutil.virtual_memory().percent, 1)
            memory_percentages.append(current_memory_percentage)

            process_memory = psutil.Process(os.getpid())
            memory_resident_set_size_bytes.append(process_memory.memory_info().rss)

            disk_io_counters = psutil.disk_io_counters()
            disk_io_read_bytes.append(disk_io_counters.read_bytes)
            disk_io_write_bytes.append(disk_io_counters.write_bytes)
    except Exception as e:
        process.terminate()
        process.wait()
        print(f"Error: {e}")
        return
    end_time = time.time()

    execution_time = round(end_time - start_time, 1)
    disk_io_read_diff = disk_io_read_bytes[-1] - disk_io_read_bytes[0]
    disk_io_write_diff = disk_io_write_bytes[-1] - disk_io_write_bytes[0]

    return {
        "cpu_usage_before": cpu_usage_before,
        "memory_usage_before": memory_usage_before,
        "execution_time": execution_time,
        "cpu_percentage": cpu_percentages,
        "cpu_context_switches": cpu_context_switches,
        "cpu_interrupts": cpu_interrupts,
        "memory_percentage": memory_percentages,
        "memory_resident_set_size_bytes": memory_resident_set_size_bytes,
        "disk_io_read_bytes": disk_io_read_diff,
        "disk_io_write_bytes": disk_io_write_diff,
    }

def print_test_info(script, headless_mode, start_time):
    """
    Displays information before starting the test, such as the script name, headless mode, and start time.

    Args:
        :script: (str) - The name of the script.
        :headless_mode: (bool) - Specifies whether the script is executed in headless mode.
        :start_time: (str) - Start time of test execution.
    """
    separator_width = os.get_terminal_size().columns 
    print("-" * separator_width)

    print(f"Running script: {script}")
    print(f"{'with' if headless_mode else 'without'} headless mode\n")
    print(f"Operating System: {get_operating_system_name()}\n") 
    print(f"Start time: {start_time}\n")

def print_test_result(stats):
    """
    Displays the test results, including the monitored resuources.

    Args:
        :stats: (dict) - Resource usage statistics during the script's execution.
    """
    print(f"CPU usage before running test: {stats['cpu_usage_before']}%\n")
    print(f"Memory usage before running test: {stats['memory_usage_before']}%\n")

    print(f"Duration time: {stats['execution_time']} seconds\n")

    cpu_usage_formatted = ", ".join([f"{percentage}%" for percentage in stats["cpu_percentage"]])
    print(f"CPU usage (measured every second): {cpu_usage_formatted}\n")

    cpu_context_switches_formatted = ", ".join([str(value) for value in stats["cpu_context_switches"]])
    print(f"CPU context switches per second (measured every second): {cpu_context_switches_formatted}\n")

    cpu_interrupts_formatted = ", ".join([str(value) for value in stats["cpu_interrupts"]])
    print(f"CPU interrupts (measured every second): {cpu_interrupts_formatted}\n")

    memory_usage_formatted = ", ".join([f"{percentage}%" for percentage in stats["memory_percentage"]])
    print(f"Memory usage (measured every second): {memory_usage_formatted}\n")

    memory_resident_set_size_bytes_formatted = ", ".join([f"{value} bytes" for value in stats["memory_resident_set_size_bytes"]])
    print(f"Memory resident set size (measured every second): {memory_resident_set_size_bytes_formatted}\n")

    print(f"Disk IO read bytes difference: {stats['disk_io_read_bytes']} bytes\n")
    print(f"Disk IO write bytes difference: {stats['disk_io_write_bytes']} bytes\n")

def write_to_csv(script, headless_mode, start_time, stats):
    """
    Writes the test results to a CSV file.

    Args:
        :script: (str) - The name of the script.
        :headless_mode: (bool) - Specifies whether the script is executed in headless mode.
        :start_time: (str) - Start time of test execution.
        :stats: (dict) - Resource usage statistics during the script's execution.
    """
    csv_filename = (
        f"{PERFORMANCE_LOGS_DIRECTORY}/{script.replace('.py', '')}_"
        f"{HEADLESS if headless_mode else NOHEADLESS}_"
        f"{get_operating_system_name(separator='-')}_{start_time}.csv"
    )

    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')

        writer.writerow(["cpu_usage_before", stats["cpu_usage_before"]])
        writer.writerow(["memory_usage_before", stats["memory_usage_before"]])
        writer.writerow(["duration_time", stats["execution_time"]])

        writer.writerow(["cpu_percentages"] + stats["cpu_percentage"])
        writer.writerow(["cpu_context_switches"] + stats["cpu_context_switches"])
        writer.writerow(["cpu_interrupts"] + stats["cpu_interrupts"])

        writer.writerow(["memory_percentages"] + stats["memory_percentage"])
        writer.writerow(["memory_resident_set_size_bytes"] + stats["memory_resident_set_size_bytes"])

        writer.writerow(["disk_io_read_bytes", stats['disk_io_read_bytes']])
        writer.writerow(["disk_io_write_bytes", stats['disk_io_write_bytes']])

def performance_analyser(headless_mode):
    """
    Conducts performance analysis for all testing scripts (Selenium, Playwright, Splinter).

    Args:
        :headless_mode: (bool) - Specifies whether scripts should be executed in headless mode.
    """
    for script in SCRIPTS_FILENAMES:
        script_path = os.path.join(script)
        if os.path.exists(script_path):
            start_time_readable, start_time_filename = get_current_datetime()
            print_test_info(script, headless_mode, start_time_readable)
            stats = run_script(script_path, headless_mode)
            if stats:
                print_test_result(stats)
                write_to_csv(script, headless_mode, start_time_filename, stats)


if __name__ == "__main__":
    if not os.path.exists(PERFORMANCE_LOGS_DIRECTORY):
        os.makedirs(PERFORMANCE_LOGS_DIRECTORY)
    for headless_mode in [True, False]:
        performance_analyser(headless_mode)
