#Goes together with visualiseNeuralLearning.py
import pickle
import matplotlib.pyplot as plt

gen = pickle.load(open("generationsSave","rb"))
bir = pickle.load(open("birthsSave","rb"))

for nam in gen:
    b = bir[nam]
    l = gen[nam]
    if len(l)>12:
        plt.plot(range(b,b+len(l)), l, label=nam.split()[0]+" taseme "+str(len(nam.split())-1)+" järglane, vanus: "+str(len(l)))
plt.legend()
plt.show()