import sys
import os
import time
import shutil
import subprocess

def main():
    if len(sys.argv) < 4:
        return

    pid_to_kill = int(sys.argv[1])
    src_path = sys.argv[2]
    dst_path = sys.argv[3]

    # 1. Kill the main process silently
    CREATE_NO_WINDOW = 0x08000000
    try:
        subprocess.run(['taskkill', '/F', '/PID', str(pid_to_kill)], 
                       capture_output=True, 
                       creationflags=CREATE_NO_WINDOW)
    except:
        pass
    
    # Wait to ensure process is completely gone and file locks released
    time.sleep(3)

    # 2. Aggressive file replacement (retry up to 20 times = 20 seconds max)
    success = False
    for _ in range(20):
        try:
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.move(src_path, dst_path)
            success = True
            break
        except Exception:
            time.sleep(1)

    # 3. Restart the main application
    if success:
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen([dst_path], creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW)

if __name__ == "__main__":
    main()
