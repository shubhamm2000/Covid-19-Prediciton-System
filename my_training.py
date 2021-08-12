import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle




if __name__ == "__main__":
    df = pd.read_csv('Coviddataset.csv')
    X = df.iloc[:,:-1].values
    y = df.iloc[:, -1].values

    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X = sc.fit_transform(X)

    from sklearn.model_selection import train_test_split

    X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 0.2, random_state = 42)

    lr = LogisticRegression()
    lr.fit(X_train,y_train)


    #open a file where you want to store the data
    file = open('model.pkl','wb')

    #dump information to that file
    pickle.dump(lr, file)
    file.close()



   