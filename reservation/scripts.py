from datetime import time
from rooms.models import Schedule  # ajuste o import para seu app

# Limpa tabela se quiser começar do zero
# Schedule.objects.all().delete()

for hour in range(7, 22):  # 7 até 21
    entry = time(hour, 0)
    exit = time(hour + 1, 0)
    Schedule.objects.create(entryTime=entry, exitTime=exit)