import pandas as pd
import numpy as np
from matplotlib import pyplot
import os
import joblib
from storagemodel.trainmodel import trainclassify


class storageclassify:

  def classifier(dataTrain, dataFeaturized, outputPath):
      pd.set_option('display.max_columns', None)
      f = pd.read_csv(dataTrain)
      pd.set_option('display.max_columns', None)
      f_featurized = pd.read_csv(dataFeaturized)
      model = trainclassify.train(f_featurized, outputPath)
      filename = outputPath
      #print(filename)
      #print(os.path.exists(filename))
      #f = '/dbfs/mnt/titanicv2'
      #files = os.listdir('/dbfs/mnt/titanicv2')  # Get all the files in that directory
      #print("Files in %r: %s" % (f, files))
      with open(filename, "wb") as f:
          joblib.dump(model, f)
      print("Training completed!")

#classifier('titanic_train.csv', 'titanic_featurized.csv', r"C:\Users\Yili")

