
import keras
import numpy as np
import librosa
from keras.models import load_model
import pandas as pd
from keras.models import model_from_json
# import model.h5
# import model.json
import os

class triModel:
    def __init__(self):
        
        # model 1
        cur = os.path.join(os.getcwd(), 'backend')
        mode1 = os.path.join(cur, 'model1.h5')
        mode2 = os.path.join(cur, 'model2.h5')
        mode3 = os.path.join(cur, 'model.json')


        self.model1 = load_model(mode1)
        self.model1Labels = ['angry' ,'excited', 'frustrated','happy','nuture', 'sad']

        # model 2
        self.model2 = keras.models.load_model(mode2)
        self.model2Labels = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        # model 3
        self.json_file = open(mode3, 'r')
        self.loaded_model_json = self.json_file.read()
        self.json_file.close()
        self.model3 = model_from_json(self.loaded_model_json)
        mode3f = os.path.join(cur, 'model3.h5')
        self.model3.load_weights(mode3f)
        self.model3Labels = [
            "angry",
            "calm",
            "fearful",
            "happy", 
            "sad",
            "angry",
            "calm",
            "fearful",
            "happy",
            "sad"
        ]


    def predict1(self, filename):

        try:
            # music= "output10.wav"
            sound, s = librosa.load(filename, sr=16000, duration=8.0)  # Downsample 44.1kHz to 16kHz

            sound = librosa.util.pad_center(sound, size=128000, mode='symmetric')  # change type 'constant'
            ps = librosa.feature.melspectrogram(y=sound, sr=16000, n_fft=2048, hop_length=512)
            ps_db = librosa.power_to_db(ps ** 2, ref=np.median)  # np and mean not max
            ps_db = np.expand_dims(ps_db, axis=0)
            ps_db = np.expand_dims(ps_db, axis=3)

            # saved_model = load_model('resources/my_model.h5')
            prediction = self.model1.predict(ps_db)
            out = np.argmax(prediction, axis=1)

            return {"modelID" : 1, "emotion" : self.model1Labels[int(out)], "accuracy" : max(list(prediction[0]))}
        
        except Exception:
            pass
    


    def predict2(self, filename):

        try:
            data, sampling_rate = librosa.load(filename)
            mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
            x = np.expand_dims(mfccs, axis=1)
            x = np.expand_dims(x, axis=0)
            predictions = self.model2.predict(x)
            allPredictions = predictions
            predictions = np.argmax(predictions, axis=1)
            predictions = str(predictions[0])

            return {"modelID" : 2, "emotion" : self.model2Labels[predictions], "accuracy" : max(list(allPredictions[0]))}
        
        except Exception:
            pass
    

    def predict3(self, filename):

        try:
            X, sample_rate = librosa.load(filename, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
            sample_rate = np.array(sample_rate)
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
            featurelive = mfccs
            livedf2 = featurelive


            livedf2= pd.DataFrame(data=livedf2)

            livedf2 = livedf2.stack().to_frame().T

            twodim= np.expand_dims(livedf2, axis=2)

            livepreds = self.model3.predict(twodim, batch_size=32, verbose=1)

            livepreds1=livepreds.argmax(axis=1)

            return {"modelID" : 3, "emotion" : self.model3Labels[int(livepreds1)], "accuracy" : max(list(livepreds[0]))}
        
        except Exception:
            pass

    
    def main(self, filename):
        pred1 = self.predict1(filename)
        pred2 = self.predict2(filename)
        pred3 = self.predict3(filename)

        out = [i for i in [pred1, pred2, pred3] if i]
        
        return out


# obj = triModel()
# print(obj.main("test1.wav"))