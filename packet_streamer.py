from nfstream import *

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
		#flow.udps.model_prediction = self.my_model.predict(to_predict)
		


ml_streamer = NFStreamer(source="eth0", udps=ModelPrediction(),statistical_analysis=True,active_timeout=5,idle_timeout=3)
for flow in ml_streamer:
	print(flow.udps.model_prediction)