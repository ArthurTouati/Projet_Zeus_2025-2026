import subprocess
import time

def get_power_mode():
    try:
        power = subprocess.run(["sudo","/usr/sbin/nvpmodel","-q"],capture_output=True,text=True,check=True)
        output = power.stdout.strip().split('\n')
        current_mode = [line for line in output if "NV Power Mode:" in line]
        if current_mode:
            parts = current_mode[0].split(':')
            if len(parts) > 1:
                mode_info = parts[1].strip().split(' ')
                mode_name = mode_info[0]
                mode_id = mode_info[-1]  # The last part is usually the ID
                return f"{mode_name} (ID: {mode_id})"
        return "Unknown"

    except subprocess.CalledProcessError as e:
        print(f"Error checking power mode: {e}")
        print(f"Stderr: {e.stderr}")
        return "Error"

    except FileNotFoundError:
        print("Error: nvpmodel command not found. Make sure it's installed and in your PATH.")
        return "Error"

get_power_mode()