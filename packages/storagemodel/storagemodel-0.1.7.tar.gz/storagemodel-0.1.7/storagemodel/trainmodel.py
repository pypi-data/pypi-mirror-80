from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


class trainclassify:

  def train(data, outputPath):
      x = data.drop('survived', axis = 1).values
      y = data['survived']
      X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state = 42)
      # Fit the model on training set
      model = LogisticRegression( max_iter = 300)
      model.fit(X_train, y_train)
      #filename = outputPath + '/titanicforwheelv1.pkl'
      return model