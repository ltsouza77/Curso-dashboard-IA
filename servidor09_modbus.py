from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
import random
import time
import threading

# Cria registradores com 100 posições
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

def atualizar_registradores():
    while True:
        valores = [
            int(random.uniform(2100, 2400)),  # tensão
            int(random.uniform(950, 1100)),   # corrente
            int(random.uniform(90, 100)),     # FP
            int(random.uniform(20, 40)),      # temperatura
            int(random.uniform(80, 150)),     # vazão
            int(random.uniform(600, 1000)),   # nível
            int(random.uniform(690, 740)),    # pH
            int(random.uniform(400, 800))     # umidade
        ]
        for i, val in enumerate(valores):
            context[0x00].setValues(3, i, [val])
        print("📤 Registradores atualizados:", valores)
        time.sleep(2)

# Roda o servidor em thread separada
threading.Thread(target=atualizar_registradores, daemon=True).start()

print("✅ Servidor pymodbus rodando na porta 5020")
StartTcpServer(context, address=("0.0.0.0", 5020))
