##Necessary Library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy.stats import skew,kurtosis
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


##user data
data=pd.read_csv("C:\\Users\\mages\\Documents\\supermarket.csv")

##variables
columns = data.columns
n = len(columns)

##Assign Correct Data Type
def assign_datatype(df):

    columns = df.columns

    for col in columns:
        if pd.api.types.is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except ValueError:
                try:
                    df[col] = df[col].astype(float)
                    if df[col].dropna().apply(float.is_integer).all():
                        df[col] = df[col].astype(int)
                except ValueError:
                    df[col] = df[col].astype(str)
        
        elif pd.api.types.is_float_dtype(df[col]):
            if df[col].dropna().apply(float.is_integer).all():
                df[col] = df[col].astype(int)

    return df


#compute percentage of missing values in a every row
def find_missing_percentage(data):
    data["Missing_Percentage"] =  ((data.isnull().sum(axis=1))/n)* 100


    #removing row with missing values of percentage greater than 50
    data = data[data["Missing_Percentage"] <= 50]
    data = data.drop(['Missing_Percentage'] , axis=1)
    return data




#check for normal distrbution columns and replace with mean
def replace_with_mean(data):
    for column in columns:
        current_column = data[column]

        if pd.api.types.is_any_real_numeric_dtype(current_column):
            skewness = skew(current_column)
            kurt = kurtosis(current_column)

            if abs(skewness) < 0.5 and abs(kurt) < 3.0:
                mean = current_column.mean()
                data[column].fillna(mean,inplace=True)
    return data





##Random Forest ML Algorithm to input missing values
def RandomForest(df):

    df_imputed = df.copy()
    columns = df.columns

    
    num_cols = [col for col in columns if df[col].dtype in ['int64', 'float64']]
    cat_cols = [col for col in columns if df[col].dtype == 'object']

    
    if num_cols:
        imputer_num = IterativeImputer(estimator=RandomForestRegressor(), random_state=42)
        df_imputed[num_cols] = imputer_num.fit_transform(df_imputed[num_cols])

    
    for col in cat_cols:
        df_imputed[col].fillna(df_imputed[col].mode()[0], inplace=True)

    return df_imputed




##visualize numerical columns
def visualize_columns(data):
    df = data.copy()
    columns = df.columns
    
    if len(columns) % 3 == 0:
        n = len(columns)//3
    else:
        n = len(columns)//3
        n += 1

    fig, axes = plt.subplots(n, 3, figsize=(15, 6 * n))
    axes = axes.flatten() if n > 1 else [axes]

    for i, column in enumerate(columns):
        if pd.api.types.is_numeric_dtype(data[column]): ##Histogram Chart of Numerical Column
            mean = data[column].mean()
            sd = data[column].std() + 1e-6

            df[f'Z-Score-of-{column}'] = (df[column] - mean) / sd
            left_max = mean - (5 * sd)
            right_max = mean + (5 * sd)

            sns.histplot(data[column], kde=True, ax=axes[i] , binrange=(left_max , right_max) , bins=10)
            axes[i].set_xlabel("Interval of bin size with SD")
            axes[i].set_ylabel("Frequency")
            axes[i].set_title(f'Distribution of {column}')
            axes[i].axvline(x=mean, color="red", linestyle="--", linewidth=2)

        elif pd.api.types.is_datetime64_any_dtype(data[column]):
            continue

        elif pd.api.types.is_object_dtype(data[column]): ##Bar chart of Categorical Column
            sns.countplot(x=data[column], ax=axes[i])
            axes[i].set_xlabel(column)
            axes[i].set_ylabel("Count")
            axes[i].set_title(f'Frequency Plot of {column}')
            axes[i].tick_params(axis='x', rotation=45)


    plt.tight_layout()
    plt.show()


