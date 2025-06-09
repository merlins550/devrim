"""Simple memory usage checker."""

import psutil
import os


def print_memory_usage():
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)
    print(f'Current memory usage: {mem_mb:.2f} MB')

if __name__ == '__main__':
    print_memory_usage()
