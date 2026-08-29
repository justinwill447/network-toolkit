import socket
import subprocess
import time
from datetime import datetime


def show_banner():
    print("=" * 40)
    print("       NETWORK TOOLKIT v0.2")
    print("=" * 40)


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

def port_scanner():
    print("\n--- Port Scanner ---")

    target = input("Enter a hostname or IP address: ").strip()

    try:
        target_ip = socket.gethostbyname(target)

        start_port = int(input("Enter starting port: "))
        end_port = int(input("Enter ending port: "))

        if start_port < 1 or end_port > 65535 or start_port > end_port:
            print("\nInvalid port range.")
            return

        print(f"\nScanning {target} ({target_ip})")
        print(f"Ports {start_port}-{end_port}...\n")

        open_ports = []
        start_time = time.time()

        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)

            result = sock.connect_ex((target_ip, port))

            if result == 0:
                print(f"[OPEN] Port {port}")
                open_ports.append(port)

            sock.close()

        elapsed_time = time.time() - start_time

        if not open_ports:
            print("No open TCP ports were found.")

        print(f"\nScan completed in {elapsed_time:.2f} seconds.")

        save_choice = input("\nSave results to a file? (y/n): ").strip().lower()

        if save_choice == "y":
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"scan_{timestamp}.txt"

            with open(filename, "w") as report:
                report.write("NETWORK TOOLKIT PORT SCAN REPORT\n")
                report.write("=" * 40 + "\n")
                report.write(f"Target: {target}\n")
                report.write(f"IP Address: {target_ip}\n")
                report.write(f"Port Range: {start_port}-{end_port}\n")
                report.write(f"Scan Time: {elapsed_time:.2f} seconds\n\n")

                if open_ports:
                    report.write("Open TCP Ports:\n")

                    for port in open_ports:
                        report.write(f"- {port}\n")
                else:
                    report.write("No open TCP ports were found.\n")

            print(f"\nResults saved as: {filename}")

    except ValueError:
        print("\nPorts must be numbers.")

    except socket.gaierror:
        print("\nCould not resolve that hostname.")

    except KeyboardInterrupt:
        print("\nScan cancelled.")

def show_menu():
    print("\n[1] Local Network Information")
    print("[2] DNS Lookup")
    print("[3] Ping Host")
    print("[4] Port Scanner")
    print("[5] Exit")


while True:
    show_banner()
    show_menu()

    choice = input("\nSelect an option: ").strip()

    if choice == "1":
        local_network_info()

    elif choice == "2":
        dns_lookup()

    elif choice == "3":
        ping_host()

    elif choice == "4":
        port_scanner()

    elif choice == "5":
        print("\nGoodbye!")
        break

    else:
        print("\nThat option is not built yet.")

    input("\nPress Enter to return to the menu...")