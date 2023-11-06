import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

columns = ['timer','x_diff','y_diff','health_diff','player1_id','health1','x_coord1','y_coord1','is_jumping1','is_crouching1','is_player_in_move1','Up1','Down1','Right1','Left1','Y1','B1','X1','A1','L1','R1','player_id2','health2','x_coord2','y_coord2','is_jumping2','is_crouching2','is_player_in_move2','move_id1','Up2','Down2','Right2','Left2','Y2','B2','X2','A2','L2','R2','move_id2']
misc = ['timer','x_diff','y_diff','health_diff','health1','x_coord1','y_coord1','health2','x_coord2','y_coord2','move_id1','move_id2']
controls1 = ['Up1','Down1','Right1','Left1','Y1','B1','X1','A1','L1','R1']
controls2 = ['Up2','Down2','Right2','Left2','Y2','B2','X2','A2','L2','R2']
traindata = pd.DataFrame(columns=columns)
traindata= pd.read_csv('traindata.csv', names = columns) 
traindata.dropna(subset=columns, inplace=True)
traindata[columns] = traindata[columns].astype(int)

traindata[misc] = traindata[misc]/100

Ndata = traindata[controls1]
concatenated = Ndata.apply(lambda x: ''.join([str(i) for i in x]), axis=1)
binary_numbers = concatenated.apply(lambda x: int(x, 2))
print(binary_numbers.unique())
traindata['Buttons1'] = binary_numbers
traindata = traindata.drop(controls1 , axis = 1)



Ndata = traindata[controls2]
concatenated = Ndata.apply(lambda x: ''.join([str(i) for i in x]), axis=1)
binary_numbers = concatenated.apply(lambda x: int(x, 2))
traindata['Buttons2'] = binary_numbers
traindata = traindata.drop(controls2 , axis = 1)


train = traindata.sample(frac=0.82, random_state=200)


#RANDOM FOREST REGRESSOR:

X = train.drop(['Buttons2'], axis=1)
y = train['Buttons2']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

y_pred = model.predict(X)
#print(y_pred)
#finding the mse of the given dataset

mse = mean_squared_error(y, y_pred)
print(f"Mean Squared Error: {mse}")

# Visualize the predicted vs actual values (optional)
import matplotlib.pyplot as plt

plt.plot(range(0,len(train['Buttons2'])), train['Buttons2'], label='Actual')
plt.plot(range(0,len(y_pred)), y_pred, label='Predicted')
plt.xlabel('Date')
plt.ylabel('Buttons2')
plt.title(f'Forest Regression (MSE = {mse:.2f})')
plt.legend()
plt.show()

