# minimal notifier: prints and (optionally) uses platform notifications if available
import platform
import subprocess
import json


def send_local_notification(title, body):
    print(f"NOTIFICATION: {title} - {body}")
    system = platform.system()
    try:
        if system == 'Darwin':
            subprocess.run(['osascript','-e', f'display notification "{body}" with title "{title}"'])
        elif system == 'Linux':
            subprocess.run(['notify-send', title, body])
        elif system == 'Windows':
            # attempt win10toast if installed; else fallback to print
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, body, duration=5)
            except Exception:
                pass
    except Exception:
        pass