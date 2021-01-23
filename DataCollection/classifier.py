import sklearn
from sklearn.neural_network import  MLPClassifier
from sklearn.ensemble import  RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle 

# I may have to improve the models , but this works , dunno if it classifies well(or at all) tho 
#usage instruction uncompress rfreg.zip
class model:
	
	def __init__(self):
		filename = 'rfreg.sav'
		self.model = pickle.load(open(filename,'rb'))
		
	def predict(self):
		return self.model.predict(self.data)
		
		
	def load_data(self,val_dict):
		#['total_fiat', 'total_biat','duration','mean_active','max_active','std_active','flowPktsPerSecond','flowBytesPerSecond']
		self.data=[[val_dict['total_fiat'],val_dict['total_biat']	,val_dict['duration'],val_dict['mean_active'],val_dict['max_active'],val_dict['std_active'],val_dict['flowPktsPerSecond'],val_dict['flowBytesPerSecond']]]
	
    
if __name__=='__main__':
    m =model()
    data = {'total_fiat':0, 'total_biat':0,'duration':0,'mean_active':0,'max_active':0,'std_active':0,'flowPktsPerSecond':0,'flowBytesPerSecond':0}
    m.load_data(data)
   
    print("output is " + str(m.predict()))