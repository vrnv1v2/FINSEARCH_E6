from mibian import BS
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Get user input for options
print("Select an option:")
print("1. dataset from 25-aug to 31-aug")
print("2. dataset from 25-aug to 7-sep")
print("3. dataset from 25-aug to 14-sep")
choice = input("Enter the NIFTY50 dataset")

# Perform actions based on user's choice
if choice == '1':
    file_path = '3.csv'  # Replace with your actual file path for Option 1
elif choice == '2':
    file_path = '2.csv'
elif choice == '3':
    file_path = '1.csv'  # Replace with your actual file path for Option 2
else:
    print("Invalid choice")
    exit()

# Read the selected file into a DataFrame
import pandas as pd
df = pd.read_csv(file_path)

#filter-out the data where Iv and ltp is not given
filtered_df = df[(df['LTP'] != '-') & (df['LTP.1'] != '-') & (df['IV']!='-') & (df['IV.1']!='-')]
filtered_df.reset_index(drop=True, inplace=True)

data=[]
data3=[]
a = filtered_df.shape[0]


#calculate Bs model for call price and put price
for i in range (0,a,1):
    S = 19265.80     # Current stock price (obtained from another source)
    K = float(filtered_df['STRIKE'][i].replace(',', '')) # Strike price
    T = 6     # Time to expiry in years
    r = 0.10     # Risk-free interest rate
    sigma = float(filtered_df['IV'][i]) 
    sigma2 = float(filtered_df['IV.1'][i]) # Volatility
    call_option = BS([S, K, r, T], volatility=sigma)
    put_option = BS([S,K,r,T], volatility=sigma2 )
    calculated_call_price = call_option.callPrice
    calculated_put_price = put_option.putPrice
    data.append(calculated_call_price)
    data3.append(calculated_put_price)

data2=[]
data4=[]

#loading data into data2 data4 array original
for j in range (0,a,1):
    w= float(filtered_df['LTP'][j].replace(',', ''))
    d= float(filtered_df['LTP.1'][j].replace(',', ''))
    data2.append(w)
    data4.append(d)


#calculation of mean error_call price
mean_error = np.mean(abs(np.array(data2) - np.array(data)))
squared_error = np.mean((np.array(data2) - np.array(data)) ** 2)

#calculation of mean error_put price
mean_error1  = np.mean(abs(np.array(data3) - np.array(data4)))
squared_error2= np.mean((np.array(data3) - np.array(data4)) ** 2)


#loading data into pd dataframe
data_dict = {'calc_call_price': data, 'given_call': data2, 'calc_put_price': data3, 'given_put': data4}



combined_df = pd.DataFrame(data_dict)
print(combined_df)

#printing the errors
print(f"Mean Error of call_price: {mean_error:.2f}")
print(f"Squared Error of call_price: {squared_error:.2f}")
print(f"Mean Error of put_price: {mean_error1:.2f}")
print(f"Squared Error of put_price: {squared_error2:.2f}")

#subplotting the calculated and given datasets
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.plot(filtered_df.index, data, label='Calculated Call Price')
plt.plot(filtered_df.index, data2, label='LTP')
plt.xlabel('Row Index')
plt.ylabel('Call Price')
plt.title('Comparison of Calculated Call Prices and LTP')
plt.legend()

#subplotting the calculated and given datasets
plt.subplot(1, 2, 2)
plt.plot(filtered_df.index, data3, label='calculated put price')
plt.plot(filtered_df.index, data4, label='LTP.1')
plt.xlabel('Row Index')
plt.ylabel('Put price')
plt.title('Comparison of Calculated Put Prices and LTP.1')
plt.legend()
plt.show()








