from datetime import datetime
def save_scan_report(target, target_ip, start_port, end_port, open_ports, elapsed_time):
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
            report.write("OPEN PORTS\n")
            report.write("-" * 40 + "\n")

            for port, service, banner, http_server in open_ports:
                report.write(f"Port {port}: {service}\n")

                if banner:
                    report.write(f"  Banner: {banner}\n")

                if http_server:
                    report.write(f"  Server: {http_server}\n")

                report.write("\n")

        else:
            report.write("No open TCP ports were found.\n")

    print(f"\nReport saved as: {filename}")