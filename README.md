# **Walmart Sales Prediction with Linear Regression**

This project predicts Walmart's weekly sales using a **Linear Regression** model. It includes exploratory data analysis (EDA), data preprocessing, feature engineering, and model training. The project is Dockerized for easy deployment and uses **MLflow** for tracking experiments.

---

## **Table of Contents**
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [Results](#results)
7. [Contributing](#contributing)
8. [License](#license)

---

## **Project Overview**
The goal of this project is to predict Walmart's weekly sales based on historical data. The dataset includes features like store information, holiday flags, temperature, fuel price, and more. The project follows these steps:
1. **Data Loading and Preprocessing**:
   - Fix date formats.
   - Handle missing values.
   - Encode categorical features.
   - Remove outliers using IQR.
2. **Exploratory Data Analysis (EDA)**:
   - Visualize distributions of numerical and categorical features.
   - Analyze relationships between features using pair plots.
3. **Model Training**:
   - Split data into training and testing sets.
   - Standardize features.
   - Train a Linear Regression model.
4. **Model Evaluation**:
   - Calculate metrics: R² score, Mean Absolute Error (MAE), and Mean Squared Error (MSE).
   - Log metrics and save the model using MLflow.

---

## **Features**
- **Data Preprocessing**:
  - Fix date formats and extract useful features (e.g., weekday, month, year).
  - Handle missing values and remove duplicates.
  - Encode categorical features using one-hot encoding.
  - Remove outliers using the Interquartile Range (IQR) method.
- **Exploratory Data Analysis (EDA)**:
  - Visualize distributions of numerical and categorical features.
  - Analyze relationships between features using pair plots.
- **Model Training and Evaluation**:
  - Train a Linear Regression model.
  - Evaluate the model using R² score, MAE, and MSE.
  - Log metrics and save the model using MLflow.

---

## **Technologies Used**
- **Python Libraries**:
  - `pandas`, `numpy`: Data manipulation.
  - `seaborn`, `matplotlib`: Data visualization.
  - `scikit-learn`: Model training and evaluation.
  - `mlflow`: Experiment tracking and model logging.
  - `dvc`: Data version control.
- **Other Tools**:
  - Docker: Containerization for easy deployment.
  - Git: Version control.

---

## **Setup and Installation**

### **Prerequisites**
- Python 3.12
- Docker (optional, for containerization)

### **Steps**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/WhiteboxHub/mlops.git
   cd mlops 

2.**Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3.**Run the script**
   ```python walmart_sales.py```


## **Usage**

### **Data Preprocessing**
The script automatically preprocesses the data by:
- Fixing date formats.
- Encoding categorical features.
- Removing outliers using the Interquartile Range (IQR) method.

### **Exploratory Data Analysis (EDA)**
The script generates visualizations for:
- **Target variable distribution**:
  - Histogram and KDE plot of weekly sales.
- **Categorical and numerical feature distributions**:
  - Count plots for categorical features.
  - Histograms and boxplots for numerical features.
- **Pair plots**:
  - Analyze relationships between features using pair plots.

### **Model Training and Evaluation**
- The script trains a **Linear Regression** model.
- The model is evaluated using the following metrics:
  - **R² Score**: [Value]
  - **Mean Absolute Error (MAE)**: [Value]
  - **Mean Squared Error (MSE)**: [Value]
- Metrics are logged using **MLflow**, and the model is saved locally.

### **MLflow Tracking**
To view logged metrics and artifacts:
1. Start the MLflow UI:
   ```bash
   mlflow ui
   ```
   
 
