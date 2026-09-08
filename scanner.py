import socket
import time
from reporting import save_scan_report

def get_service_name(port):
    common_services = {
        20: "FTP Data",
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        67: "DHCP",
        68: "DHCP",
        80: "HTTP",
        110: "POP3",
        123: "NTP",
        135: "MSRPC",
        139: "NetBIOS",
        143: "IMAP",
        161: "SNMP",
        389: "LDAP",
        443: "HTTPS",
        445: "SMB",
        587: "SMTP",
        636: "LDAPS",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        8080: "HTTP Alternate"
    }

    return common_services.get(port, "Unknown")


def grab_banner(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((target_ip, port))

        try:
            banner = sock.recv(1024).decode(errors="ignore").strip()
        except socket.timeout:
            banner = ""

        sock.close()
        return banner

    except Exception:
        return ""


def probe_http(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target_ip, port))

        request = (
            "HEAD / HTTP/1.1\r\n"
            f"Host: {target_ip}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        sock.sendall(request.encode())
        response = sock.recv(4096).decode(errors="ignore")
        sock.close()

        for line in response.splitlines():
            if line.lower().startswith("server:"):
                return line.split(":", 1)[1].strip()

        return "HTTP detected"

    except Exception:
        return ""

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
                service = get_service_name(port)
                banner = grab_banner(target_ip, port)
                http_server = ""

                if port in [80, 8080, 8000]:
                    http_server = probe_http(target_ip, port)

                print(f"[OPEN] Port {port:<5} {service}")

                if banner:
                    print(f"       Banner: {banner}")

                if http_server:
                    print(f"       Server: {http_server}")

                open_ports.append((port, service, banner, http_server))

            sock.close()

        elapsed_time = time.time() - start_time

        if not open_ports:
            print("No open TCP ports were found.")

        print(f"\nScan completed in {elapsed_time:.2f} seconds.")

        save_choice = input("\nSave results to a file? (y/n): ").strip().lower()

        if save_choice == "y":
            save_scan_report(
                target,
                target_ip,
                start_port,
                end_port,
                open_ports,
                elapsed_time
            )
    except ValueError:
            print("\nPlease enter valid port numbers.")

    except socket.gaierror:
            print("\nCould not resolve the target hostname.")

    except KeyboardInterrupt:
            print("\nScan cancelled.")