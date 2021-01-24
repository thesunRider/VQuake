from nfstream import *
import sklearn,sqlite3
from sklearn.neural_network import  MLPClassifier
from sklearn.ensemble import  RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle 

#THE LACK OF DATASETS MAY CAUSE PROBLEMS WITH ACCURACY
class ClassifyPackets:
	
	def __init__(self):
		filename = 'DataCollection/rfreg.sav'
		self.model = pickle.load(open(filename,'rb'))
		
	def predict(self):
		return self.model.predict(self.data)
		
		
	def load_data(self,val_dict):
		#['total_fiat', 'total_biat','duration','mean_active','max_active','std_active','flowPktsPerSecond','flowBytesPerSecond']
		self.data=[[val_dict['total_fiat'],val_dict['total_biat']	,val_dict['duration'],val_dict['mean_active'],val_dict['max_active'],val_dict['std_active'],val_dict['flowPktsPerSecond'],val_dict['flowBytesPerSecond']]]
	

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
		try:
			data = {'total_fiat':flow.src2dst_mean_piat_ms, 'total_biat':flow.dst2src_mean_piat_ms,'duration':flow.bidirectional_duration_ms,'mean_active':(flow.bidirectional_max_piat_ms + flow.bidirectional_min_piat_ms)/2,'max_active':flow.bidirectional_max_piat_ms,'std_active':flow.bidirectional_stddev_piat_ms,'flowPktsPerSecond':flow.bidirectional_packets/flow.bidirectional_duration_ms,'flowBytesPerSecond':flow.bidirectional_bytes/flow.bidirectional_duration_ms}
			self.model.load_data(data)
			flow.udps.model_prediction = self.model.predict()
			if flow.udps.model_prediction > 0.8:
				conn = sqlite3.connect('db/filtered.db',check_same_thread=False)
				cursor = conn.cursor()
				cursor.execute("""INSERT INTO AI_filter (ip) VALUES (?);""",[str(flow.dst_ip)])
				conn.commit()
				conn.close()
		except Exception as e:
			print("Some error occured it seems")
			pass
		


ml_streamer = NFStreamer(source="eth0", udps=ModelPrediction(model=ClassifyPackets()),statistical_analysis=True,active_timeout=5,idle_timeout=3)
for flow in ml_streamer:
	print(flow.udps.model_prediction)