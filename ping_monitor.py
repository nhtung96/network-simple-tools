
import subprocess
import time
import statistics
import os

def ping_monitor(ip_address, interval=1):
    """
    Monitors the reachability of an IP address and shows only current ping results with totals.

    Args:
        ip_address (str): The IP address to monitor.
        interval (int): Time interval (in seconds) between pings.
    """
    packets_sent = 0
    packets_received = 0
    rtt_list = []  # Store RTT values

    print(f"Monitoring IP: {ip_address}")
    print("=" * 50)

    try:
        while True:
            packets_sent += 1  # Increment sent packet count

            # Execute the ping command
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", ip_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Clear the terminal output
            os.system("clear")

            if result.returncode == 0:
                packets_received += 1  # Increment received packet count

                # Extract RTT value from ping output
                for line in result.stdout.splitlines():
                    if "time=" in line:
                        rtt_value = float(line.split("time=")[-1].split(" ")[0])
                        rtt_list.append(rtt_value)
                        break
                status = "Success"
            else:
                status = "Failed"

            # Calculate statistics
            loss_percent = 100 - (packets_received / packets_sent * 100)
            success_percent = (packets_received / packets_sent * 100)
            avg_rtt = f"{statistics.mean(rtt_list):.2f}" if rtt_list else "N/A"

            # Print the current result and totals
            print(f"Monitoring IP: {ip_address}")
            print("=" * 50)
            print(f"Current Status: {status}")
            if status == "Success":
                print(f"RTT (ms): {rtt_value:.2f}")
            print("-" * 50)
            print(f"Total Sent: {packets_sent}")
            print(f"Total Received: {packets_received}")
            print(f"Packet Loss (%): {loss_percent:.2f}")
            print(f"Average RTT (ms): {avg_rtt}")
            print("=" * 50)

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        print("=" * 50)
        print(f"Final Stats: Sent: {packets_sent}, Received: {packets_received}, Loss: {loss_percent:.2f}%, Avg RTT: {avg_rtt} ms")


if __name__ == "__main__":
    target_ip = input("Enter the IP address to monitor: ")
    ping_monitor(target_ip)
