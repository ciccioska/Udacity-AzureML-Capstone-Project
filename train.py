from sklearn.linear_model import LogisticRegression
import argparse
import os
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory

web_path = "https://raw.githubusercontent.com/ciccioska/Udacity-AzureML-Capstone-Project/master/healthcare-dataset-stroke-data.csv"
ds = TabularDatasetFactory.from_delimited_files(web_path)

x_df = ds.to_pandas_dataframe().dropna()

x_df["work_type"] = x_df.work_type.apply(lambda s: 1 if s == "Private" else 0 if s == "Self-employed" else -1)
x_df["bmi"] = x_df.bmi.apply(lambda s: 0 if s == "N/A" else s)
x_df["gender"] = x_df.gender.apply(lambda s: 1 if s == "Male" else 0)
x_df["Residence_type"] = x_df.Residence_type.apply(lambda s: 1 if s == "Urban" else 0)
x_df["smoking_status"] = x_df.smoking_status.apply(lambda s: 1 if s == "smokes" else -1 if s == "never smoked" else 2 if s == "formerly smoked" else 0)

print(x_df)

y_df = x_df.pop("stroke")

print(y_df)

# Split data into train and test sets.
x_train, x_test, y_train, y_test = train_test_split(x_df, y_df, test_size = 0.3)

run = Run.get_context()

def main():

    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--C', type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")

    args = parser.parse_args()

    run.log("Regularization Strength:", np.float(args.C))
    run.log("Max iterations:", np.int(args.max_iter))

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    run.log("Accuracy", np.float(accuracy))

    os.makedirs('outputs', exist_ok=True)
    joblib.dump(model, 'outputs/hyper-drive-model.pkl')

if __name__ == '__main__':
    main()


