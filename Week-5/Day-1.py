import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    precision_score,
    recall_score,
    f1_score
)

# Exercise 1: Data Loading & Exploration

df = pd.read_csv("Week-5/diabetes_prediction_dataset.csv")

print(df.head())
print(df.info())

print("\nColonnes du dataset :")
print(df.columns)

if "Outcome" in df.columns:
    target_col = "Outcome"
elif "diabetes" in df.columns:
    target_col = "diabetes"
else:
    raise ValueError("Je ne trouve ni 'Outcome' ni 'diabetes' dans les colonnes.")

print("\nClass distribution:")
print(df[target_col].value_counts())

X = df.drop(target_col, axis=1)
y = df[target_col]

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nData split done.")
print("-" * 50)


# Exercise 2: Model & Standardization

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Data standardized.")
print("-" * 50)

# Exercise 3: Model Training

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Model trained.")
print("-" * 50)


# Exercise 4: Evaluation Metrics

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

metrics_names = ["Accuracy", "Precision", "Recall", "F1-score"]
metrics_values = [accuracy, precision, recall, f1]

plt.figure(figsize=(8, 4))
sns.barplot(x=metrics_names, y=metrics_values)
plt.ylim(0, 1)
plt.title("Model Evaluation Metrics")
plt.ylabel("Score")
plt.show()

print("-" * 50)

# Exercise 5: Decision Boundary (simplified)

if "Glucose" in df.columns and "BMI" in df.columns:
    feature_1 = "Glucose"
    feature_2 = "BMI"
elif "blood_glucose_level" in df.columns and "bmi" in df.columns:
    feature_1 = "blood_glucose_level"
    feature_2 = "bmi"
else:
    raise ValueError("Je ne trouve pas les colonnes nécessaires pour la décision boundary.")

X_vis = df[[feature_1, feature_2]]
y_vis = df[target_col]

scaler_vis = StandardScaler()
X_vis_scaled = scaler_vis.fit_transform(X_vis)

model_vis = LogisticRegression(max_iter=1000)
model_vis.fit(X_vis_scaled, y_vis)

x_min, x_max = X_vis_scaled[:, 0].min() - 1, X_vis_scaled[:, 0].max() + 1
y_min, y_max = X_vis_scaled[:, 1].min() - 1, X_vis_scaled[:, 1].max() + 1

xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 200),
    np.linspace(y_min, y_max, 200)
)

Z = model_vis.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap="coolwarm")
plt.scatter(X_vis_scaled[:, 0], X_vis_scaled[:, 1], c=y_vis, cmap="coolwarm", edgecolor="k", s=30)

plt.title(f"Decision Boundary (Accuracy ≈ {accuracy:.2f})")
plt.xlabel(f"{feature_1} (scaled)")
plt.ylabel(f"{feature_2} (scaled)")
plt.show()

print("-" * 50)

# Exercise 6: ROC Curve

y_prob = model.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")

plt.title("ROC Curve")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.show()