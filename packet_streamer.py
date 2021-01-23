from nfstream import *
import sklearn
from sklearn.neural_network import  MLPClassifier
from sklearn.ensemble import  RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle 

#THE LACK OF DATASETS MAY CAUSE PROBLEMS WITH ACCURACY
class ClassifyPackets:
	
	def __init__(self):
		filename = 'rfreg.sav'
		self.model = pickle.load(open(filename,'rb'))
		
	def predict(self):
		return self.model.predict(self.data)
		
		
	def load_data(self,val_dict):
		#['total_fiat', 'total_biat','duration','mean_active','max_active','std_active','flowPktsPerSecond','flowBytesPerSecond']
		self.data=[[val_dict['total_fiat'],val_dict['total_biat']	,val_dict['duration'],val_dict['mean_active'],val_dict['max_active'],val_dict['std_active'],val_dict['flowPktsPerSecond'],val_dict['flowBytesPerSecond']]]
	
    
if __name__=='__main__':
    m =	ClassifyPackets()
    data = {'total_fiat':0, 'total_biat':0,'duration':0,'mean_active':0,'max_active':0,'std_active':0,'flowPktsPerSecond':0,'flowBytesPerSecond':0}
    m.load_data(data)
   
    print("output is " + str(m.predict()))

class ModelPrediction(NFPlugin):
	def on_init(self, packet, flow):
		flow.udps.model_prediction = 0
		flow.udps.model_pcksize = 0
		print('Started new flow')


	def on_update(self, packet, flow):
		flow.udps.model_pcksize += 10
		#print("Updated:",flow.udps.model_pcksize )


	def on_expire(self, flow):
		if flow.udps.model_pcksize > 50:
			print('expired')
			flow.udps.model_pcksize = 0


		#to_predict = numpy.array([flow.bidirectional_packets, flow.bidirectional_bytes]).reshape((1,-1))
		self.model.load_data(to_predict)
		flow.udps.model_prediction = str(self.model.predict())
		


ml_streamer = NFStreamer(source="eth0", udps=ModelPrediction(model=ClassifyPackets()),statistical_analysis=True,active_timeout=5,idle_timeout=3)
for flow in ml_streamer:
	print(flow.udps.model_prediction)