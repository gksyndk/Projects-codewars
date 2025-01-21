from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Example data: A time series dataset
import numpy as np
import pandas as pd

# Create a sample time series
np.random.seed(42)
data = pd.Series(np.random.randn(100).cumsum(), name="Value")

# Split into train and test sets
train, test = data[:-10], data[-10:]

# Fit the ETS model (additive trend and seasonality)
ets_model = ExponentialSmoothing(
    train,
    trend='add',
    seasonal=None,  # Set to 'add' or 'mul' for seasonality
    seasonal_periods=12  # Seasonal length (e.g., months in a year)
)
ets_fit = ets_model.fit()

# Forecasting
ets_forecast = ets_fit.forecast(steps=len(test))

# Evaluate
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(test, ets_forecast)
print(f"ETS Model MSE: {mse}")

# Plot results
import matplotlib.pyplot as plt
plt.plot(data, label="Original Data")
plt.plot(ets_forecast, label="ETS Forecast", color='red')
plt.legend()
plt.show()

#Hybrid with RNN
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

# Step 1: Decompose with ETS
# Create a sample time series
np.random.seed(42)
data = pd.Series(np.random.randn(100).cumsum(), name="Value")

# Split into train and test sets
train, test = data[:-10], data[-10:]

# Fit ETS model
ets_model = ExponentialSmoothing(
    train, trend='add', seasonal=None
)
ets_fit = ets_model.fit()

# Extract ETS forecast and residuals
ets_forecast = ets_fit.forecast(steps=len(test))
residuals = train - ets_fit.fittedvalues

# Step 2: Train RNN on Residuals
# Prepare data for RNN
scaler = MinMaxScaler()
residuals_scaled = scaler.fit_transform(residuals.values.reshape(-1, 1))

# Create sequences for RNN
def create_sequences(data, seq_length=10):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 10
X, y = create_sequences(residuals_scaled, seq_length)
X = X.reshape(X.shape[0], X.shape[1], 1)

# Build the RNN model
rnn_model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])
rnn_model.compile(optimizer='adam', loss='mean_squared_error')

# Train the RNN
rnn_model.fit(X, y, epochs=10, batch_size=16, verbose=1)

# Predict residuals for the test set
X_test, _ = create_sequences(scaler.transform(train[-seq_length:].values.reshape(-1, 1)), seq_length)
rnn_residual_forecast = rnn_model.predict(X_test)
rnn_residual_forecast = scaler.inverse_transform(rnn_residual_forecast)

# Step 3: Combine ETS and RNN Predictions
combined_forecast = ets_forecast.values + rnn_residual_forecast.flatten()

# Evaluate
mse_combined = mean_squared_error(test, combined_forecast)
print(f"Hybrid ETS-RNN MSE: {mse_combined}")

# Plot results
import matplotlib.pyplot as plt
plt.plot(data, label="Original Data")
plt.plot(range(len(train), len(train) + len(test)), combined_forecast, label="Hybrid Forecast", color='green')
plt.legend()
plt.show()
