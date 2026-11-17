"""Primeiro script dentro de um container: mostra onde ele está rodando."""

import os
import platform
import socket
from datetime import datetime

nome = os.environ.get("NOME", "ELLEN")

print(f"Olá, {nome}!")
print(f"Python: {platform.python_version()}")
print(f"Sistema: {platform.system()} {platform.release()}")
print(f"Nome da máquina (hostname): {socket.gethostname()}")
print(f"Horário: {datetime.now().isoformat(timespec='seconds')}")