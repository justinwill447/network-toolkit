import socket
import subprocess


def local_network_info():
    print("\n--- Local Network Information ---")

    hostname = socket.gethostname()
    print(f"Hostname: {hostname}")

    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"Local IP: {ip_address}")
    except socket.gaierror:
        print("Local IP: Unable to determine")

    print("\nNetwork Interfaces:")
    subprocess.run(["ip", "-brief", "address"])


def dns_lookup():
    print("\n--- DNS Lookup ---")

    domain = input("Enter a domain name: ").strip()

    try:
        ip_address = socket.gethostbyname(domain)
        print(f"\nDomain: {domain}")
        print(f"IP Address: {ip_address}")
    except socket.gaierror:
        print(f"\nCould not resolve: {domain}")


def ping_host():
    print("\n--- Ping Host ---")

    host = input("Enter a hostname or IP address: ").strip()

    try:
        result = subprocess.run(
            ["ping", "-c", "4", host],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"\n{host} is reachable.\n")
            print(result.stdout)
        else:
            print(f"\n{host} did not respond.")
            print(result.stderr)

    except Exception as error:
        print(f"\nAn error occurred: {error}")