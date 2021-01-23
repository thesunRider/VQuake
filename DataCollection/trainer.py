import numpy as np 
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler


def DataScaler(data):
    scaler = MinMaxScaler()
    data = scaler.fit_transform(data)
    return data 
    
# might run into mempry issue ,dunno 
class Trainer:
    def __init__(self,file_name):
        self.data= pandas.read_csv(file_name)
        self.training_data = self.data.loc[:,self.data.columns != "is_proxy"]
        self.testing_data = self.data["is_proxy"]
        self.solver = 'lbfgs'
        self.alpha = 1e-5
        self.hidden_layer_sizes=(5,2)
        self.random_state = 1
        self.classifier = MLPClassifier(solver = self.solver , alpha = self.alpha ,hidden_layer_sizes=self.hidden_layer_sizes ,random_state=self.random_state)
        self.predicted=0
        self.predict_step=400
        self.scaled = False
    def scale(self):
        self.training_data=DataScaler(self.training_data)
        self.testing_data=DataScaler(self.testing_data)
    def train(self):
        if  not self.scaled:
            self.scale()
        self.classifier.fit(self.training_data,self.testing_data)
    def predict(self,data):
        self.classifier.predict(data)
    
    
if __name__ == "__main__":
    trainer = Trainer('ipdata.csv')
    trainer.scale()
    trainer.train()
    trainer.predict()