import sys
import os
import time
import shutil
import subprocess

def main():
    if len(sys.argv) < 4:
        print("Usage: updater.exe <pid_to_kill> <src_path> <dst_path>")
        return

    pid_to_kill = int(sys.argv[1])
    src_path = sys.argv[2]
    dst_path = sys.argv[3]

    print(f"Waiting for process {pid_to_kill} to exit...")
    
    # 1. Kill the main process
    try:
        subprocess.run(['taskkill', '/F', '/PID', str(pid_to_kill)], capture_output=True)
    except:
        pass
    
    # Extra wait to ensure file handles are released
    time.sleep(2)

    # 2. Aggressive file replacement
    success = False
    for i in range(15):
        try:
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.move(src_path, dst_path)
            success = True
            break
        except Exception as e:
            print(f"Retry {i+1}: {e}")
            time.sleep(1)

    if success:
        print("Update successful! Restarting...")
        subprocess.Popen([dst_path], creationflags=subprocess.DETACHED_PROCESS)
    else:
        print("Update failed. Please manually replace the file.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
