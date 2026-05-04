import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


productos_ml = pd.read_sql("SELECT * FROM productos_clean", engine)
productos_ml['alto_riesgo'] = (tasa_devolucion.reindex(productos_ml['id']).fillna(0) > umbral).astype(int)
categoricas = pd.get_dummies(productos_ml[['talla', 'color', 'temporada']], drop_first=True)
numericas = productos_ml[['precio_venta', 'precio_costo', 'departamento_id']]
X = pd.concat([categoricas, numericas], axis=1)
y = productos_ml['alto_riesgo']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=5, min_samples_leaf=5)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

