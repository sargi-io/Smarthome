from bmr import Bmr

bmr = Bmr("http://192.168.68.109/", "admin", "1234")

numCircuits = bmr.getNumCircuits()
# bmr.setManualTemp(0, 22)
for i in range(numCircuits):
        circuit = bmr.getCircuit(i)
        print(f"{circuit}")