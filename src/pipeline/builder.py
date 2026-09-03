import subprocess
from src.utils.decorators import measure_time

class Builder:
    def __init__(self, nasm_code, output_file):
        self.nasm_code = nasm_code
        self.output_file = output_file

    @measure_time("Building executable...")
    def build_executable(self):
        subprocess.run(["nasm", "-f", "elf64", "-g", "-F", "dwarf", self.nasm_code, "-o", f"{self.output_file}.o"], check=True)
        subprocess.run(["gcc", "-no-pie", f"{self.output_file}.o", "-o", f"{self.output_file}", "-lc"], check=True)