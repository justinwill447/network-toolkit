import socket
import subprocess
import time
from datetime import datetime
from network_utils import local_network_info, dns_lookup, ping_host
from scanner import port_scanner

def show_banner():
    print("=" * 40)
    print("       NETWORK TOOLKIT v0.2")
    print("=" * 40)


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