import psutil
import time
from termcolor import colored


while True:
    print("#"*80)
    # Get CPU usage
    cpu_usage = psutil.cpu_percent()
    print(cpu_usage)
    # Get memory usage
    memory_usage = psutil.virtual_memory()
    print(memory_usage)
    # Get percentage of used RAM
    used_ram_percent = psutil.virtual_memory().percent
    print(used_ram_percent)
    # Calculate percentage of available memory
    available_memory_percent = psutil.virtual_memory().available*100/psutil.virtual_memory().total
    if available_memory_percent < 10:
        print(colored(available_memory_percent, 'red'))
    else:
        print(available_memory_percent)
    time.sleep(5)
