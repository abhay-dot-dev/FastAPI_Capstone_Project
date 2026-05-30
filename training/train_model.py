import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from training.train_utils import DATA_FILE_PATH, MODEL_DIR, MODEL_PATH

df = (
    pd
    .read_csv(DATA_FILE_PATH)
    .drop_duplicates()
    .drop(columns = ['name', 'model', 'edition'])
)

X = df.drop(columns='selling_price')
y = df.selling_price.copy()

X_train, X_test , y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

num_cols = X_train.select_dtypes(include='number').columns.tolist()
cat_col = [col for col in X_train.columns if col not in num_cols]

num_pipe = Pipeline(
    steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]
)

cat_pipe = Pipeline(
    steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_pipe, num_cols),
        ('cat', cat_pipe, cat_col)
    ]
)

regressor = RandomForestRegressor(
    n_estimators=10,
    max_depth=5,
    random_state=42
)

rf_model = Pipeline(
    steps=[
        ('pre', preprocessor),
        ('reg', regressor)
    ]
)

rf_model.fit(X_train, y_train)

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(rf_model, MODEL_PATH)