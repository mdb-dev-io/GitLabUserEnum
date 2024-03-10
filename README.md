# GitLab User Enumeration Script

This Python script is designed to enumerate valid usernames on a GitLab instance by iterating over a list of potential usernames and checking for their existence. The script provides real-time feedback, including a dynamic count of attempts, a running list of found usernames, and the option to use proxies for requests. The output is styled using colors inspired by the Dracula color scheme for better readability.

## Features

- **Dynamic Progress Updates**: Displays a running count of usernames being tested.
- **Colorful Output**: Utilizes the Dracula color scheme for terminal output.
- **Proxy Support**: Allows traffic to be routed through specified proxies.
- **Result Persistence**: Saves found usernames to `gitlabUserEnumValidUsers.txt`.
- **Dracula Theme**: Terminal output follows the Dracula color scheme for improved readability.

## Usage

To use this script, you'll need Python 3 and the `requests` library installed. You can then run the script from the command line, providing the necessary arguments.

```bash
python3 gitlabUserEnum.py --url <GitLab_URL> --wordlist <path_to_wordlist> [--threads <num_threads>] [--timeout <request_timeout>] [--proxies <proxy_url>]
```

### Arguments

- `--url` - The URL of the GitLab instance to test against.
- `--wordlist` - Path to the file containing the list of usernames to test.
- `--threads` (optional) - Number of threads to use for concurrent requests (default is 10).
- `--timeout` (optional) - Timeout in seconds for each request (default is 10).
- `--proxies` (optional) - Proxy server to route traffic through (e.g., `http://127.0.0.1:8080`).

### Example

```bash
python3 gitlabUserEnum.py --url http://gitlab.example.com --wordlist ~/usernames.txt --proxies http://127.0.0.1:8080
```

## Acknowledgments

- This script was inspired by and originally based on the [GitLabUserEnum](https://github.com/dpgg101/GitLabUserEnum) project by dpgg101 which is inspired by [GitLab Community Edition (CE) 13.10.3 - User Enumeration
](https://www.exploit-db.com/exploits/49821) in Python3 for [Academy](http://academy.hackthebox.com/) for Module "Attacking Commoon Applications" and section "Attacking GitLab".

- Enhancements have been made to improve functionality, usability, and output aesthetics.

## Disclaimer

This tool is intended for security research and penetration testing engagements only. Please use responsibly and ensure you have permission to test the target system.

