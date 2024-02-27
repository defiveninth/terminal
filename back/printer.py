import subprocess

def get_printers_linux():
    try:
        result = subprocess.run(['lpstat', '-a'], capture_output=True, text=True, check=True)
        printers = result.stdout.split('\n')
        return [printer.split()[0] for printer in printers if printer.strip()]  # Extract printer names
    except subprocess.CalledProcessError:
        return []

printers = get_printers_linux()
print("Printers:", printers)