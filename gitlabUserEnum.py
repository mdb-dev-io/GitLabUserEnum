#!/usr/bin/env python3

# Import necessary modules
import requests  # For making HTTP requests
import argparse  # For parsing command line arguments
from threading import Thread, Lock  # For threading and thread synchronization
from queue import Queue  # For thread-safe queues
from sys import stdout  # For writing output to the terminal

# Global variables for shared state among threads
found_usernames = []  # List to store found valid usernames
total_attempts = 0  # Total number of username checks to perform
count_lock = Lock()  # Lock for synchronizing access to the total_attempts counter
found_lock = Lock()  # Lock for synchronizing access to the found_usernames list

def check_username(url, username, proxies, timeout=10):
    """
    Checks if a username exists on a given GitLab instance.

    Args:
        url (str): The URL of the GitLab instance.
        username (str): The username to check for existence.
        proxies (dict): Proxies to use for the request.
        timeout (int): Timeout for the request in seconds.
    """
    global found_usernames
    try:
        response = requests.head(f'{url}/{username}', proxies=proxies, timeout=timeout)
        if response.status_code == 200:  # HTTP 200 indicates the username exists
            with found_lock:  # Ensure thread-safe access to found_usernames
                found_usernames.append(username)
                # Print the list of found usernames with terminal color coding
                print(f'\r\033[K\033[35m[+] Found usernames:\033[0m \033[92m{", ".join(found_usernames)}\033[0m', flush=True)
    except requests.RequestException as e:  # Handle request errors
        print(f'\r\033[K\033[31m[!] Error checking username {username}:\033[0m \033[93m{str(e)}\033[0m', flush=True)

def worker(url, queue, proxies, timeout):
    """
    Worker function for processing usernames in a thread.

    Args:
        url (str): The URL of the GitLab instance.
        queue (Queue): The queue of usernames to check.
        proxies (dict): Proxies to use for the request.
        timeout (int): Timeout for the request in seconds.
    """
    global total_attempts
    while not queue.empty():
        with count_lock:  # Synchronize access to the queue size
            current_count = queue.qsize()
        username = queue.get()
        attempt_count = total_attempts - current_count + 1
        # Display the current attempt and username being checked
        message = f"\rAttempt {attempt_count} of {total_attempts}: Trying username '\033[96m{username}\033[0m'\033[K"
        stdout.write(message)
        stdout.flush()
        check_username(url, username, proxies, timeout)
        queue.task_done()

    # Clear the progress message after all attempts
    print('\r\033[K', end='')

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='GitLab User Enumeration with Enhanced Functionality')
    parser.add_argument('--url', '-u', required=True, help="The URL of the GitLab's instance")
    parser.add_argument('--wordlist', '-w', required=True, help='Path to the username wordlist')
    parser.add_argument('--threads', '-t', type=int, default=10, help='Number of threads to use')
    parser.add_argument('--timeout', '-T', type=int, default=10, help='Request timeout in seconds')
    parser.add_argument('--proxies', '-p', type=str, help='Proxy to use for requests, e.g., http://127.0.0.1:8080')
    args = parser.parse_args()

    # Set up proxies if provided
    proxies = {'http': args.proxies, 'https': args.proxies} if args.proxies else None

    # Load the username wordlist into a queue for processing
    queue = Queue()
    with open(args.wordlist, 'r') as f:
        for line in f:
            queue.put(line.strip())

    global total_attempts
    total_attempts = queue.qsize()  # Set the total number of attempts based on the queue size

    # Start threads for username checking
    threads = []
    for _ in range(args.threads):
        thread = Thread(target=worker, args=(args.url, queue, proxies, args.timeout))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print completion message and handle the case where no usernames were found
    if not found_usernames:  # Check if any usernames were found
        print('\033[31m[!]\033[0m No valid usernames were found.')
    else:
        print('\033[35m[+]\033[0m Script completed. Valid usernames saved to \033[92mgitlabUserEnumValidUsers.txt\033[0m')

    # Save the found usernames to a file
    with open('gitlabUserEnumValidUsers.txt', 'w') as f:
        for username in found_usernames:
            f.write(f'{username}\n')

if __name__ == '__main__':
    main()
