# ============================================================
# Daily Challenge: Classification with Neural Networks
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split

print("TensorFlow version:", tf.__version__)

# ============================================================
# 1. Classification Types
# ============================================================
print("""
=== Classification Types ===

1. BINARY CLASSIFICATION
   - Output: 2 classes (0 or 1)
   - Example: Email = spam or not spam
   - Activation: sigmoid, Loss: binary_crossentropy

2. MULTI-CLASS CLASSIFICATION
   - Output: 3+ classes, one label per sample
   - Example: Handwritten digit = 0,1,2,...,9
   - Activation: softmax, Loss: categorical_crossentropy

3. MULTI-LABEL CLASSIFICATION
   - Output: multiple labels per sample simultaneously
   - Example: Movie genres = [Action, Comedy, Romance]
   - Activation: sigmoid on each output neuron
""")

# ============================================================
# 2. Create and visualize dataset
# ============================================================
samples = 1000
X, y = make_circles(samples, noise=0.03, random_state=42)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("Classes:", np.unique(y))

# Visualize
plt.figure(figsize=(7, 6))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, alpha=0.7, edgecolors='k', s=40)
plt.title("make_circles dataset", fontsize=14)
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.colorbar(label="Class")
plt.tight_layout()
plt.show()

# ============================================================
# 3. Basic model (1 dense layer)
# ============================================================
tf.random.set_seed(42)

model_basic = tf.keras.Sequential([
    tf.keras.layers.Dense(1, activation="sigmoid", input_shape=(2,))
], name="basic_model")

model_basic.compile(
    loss="binary_crossentropy",
    optimizer="sgd",
    metrics=["accuracy"]
)

model_basic.summary()

history_basic = model_basic.fit(X, y, epochs=100, verbose=0)

loss, acc = model_basic.evaluate(X, y, verbose=0)
print(f"\nBasic model — Loss: {loss:.4f} | Accuracy: {acc:.4f}")

# ============================================================
# 4. Improved model (more layers + Adam)
# ============================================================
model_improved = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation="relu", input_shape=(2,)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1,  activation="sigmoid")
], name="improved_model")

model_improved.compile(
    loss="binary_crossentropy",
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    metrics=["accuracy"]
)

history_improved = model_improved.fit(X, y, epochs=200, verbose=0)

loss, acc = model_improved.evaluate(X, y, verbose=0)
print(f"Improved model — Loss: {loss:.4f} | Accuracy: {acc:.4f}")

# ============================================================
# 5. Decision boundary visualization
# ============================================================
def plot_decision_boundary(model, X, y, title="Decision Boundary"):
    x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
    y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                         np.linspace(y_min, y_max, 300))
    grid = np.c_[xx.ravel(), yy.ravel()]
    preds = model.predict(grid, verbose=0).reshape(xx.shape)

    plt.figure(figsize=(7, 6))
    plt.contourf(xx, yy, preds, levels=50, cmap=plt.cm.RdYlBu, alpha=0.6)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu,
                edgecolors='k', s=30, alpha=0.8)
    plt.title(title, fontsize=14)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.tight_layout()
    plt.show()

plot_decision_boundary(model_basic,    X, y, "Basic model (1 layer, SGD)")
plot_decision_boundary(model_improved, X, y, "Improved model (3 layers, Adam)")

# ============================================================
# 6. Activation functions comparison
# ============================================================
def build_model(activation="relu", name="model"):
    m = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation=activation, input_shape=(2,)),
        tf.keras.layers.Dense(32, activation=activation),
        tf.keras.layers.Dense(1,  activation="sigmoid")
    ], name=name)
    m.compile(loss="binary_crossentropy",
              optimizer="adam", metrics=["accuracy"])
    return m

model_relu    = build_model("relu",    "relu_model")
model_sigmoid = build_model("sigmoid", "sigmoid_model")

model_relu.fit(X,    y, epochs=200, verbose=0)
model_sigmoid.fit(X, y, epochs=200, verbose=0)

for m in [model_relu, model_sigmoid]:
    l, a = m.evaluate(X, y, verbose=0)
    print(f"{m.name:20s} — Loss: {l:.4f} | Accuracy: {a:.4f}")

# ============================================================
# 7. Train/test split (80/20)
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTrain: {X_train.shape} | Test: {X_test.shape}")

# Final model
tf.random.set_seed(42)
model_final = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation="relu",    input_shape=(2,)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1,  activation="sigmoid")
], name="final_model")

model_final.compile(
    loss="binary_crossentropy",
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    metrics=["accuracy"]
)

history_final = model_final.fit(
    X_train, y_train,
    epochs=300,
    validation_data=(X_test, y_test),
    verbose=0
)

# ============================================================
# 8. Evaluate and visualize final model
# ============================================================
train_loss, train_acc = model_final.evaluate(X_train, y_train, verbose=0)
test_loss,  test_acc  = model_final.evaluate(X_test,  y_test,  verbose=0)
print(f"\nFinal model:")
print(f"  Train — Loss: {train_loss:.4f} | Accuracy: {train_acc:.4f}")
print(f"  Test  — Loss: {test_loss:.4f}  | Accuracy: {test_acc:.4f}")

# Loss / accuracy curves
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(history_final.history["loss"],     label="Train loss")
axes[0].plot(history_final.history["val_loss"], label="Val loss")
axes[0].set_title("Loss over epochs")
axes[0].set_xlabel("Epoch")
axes[0].legend()

axes[1].plot(history_final.history["accuracy"],     label="Train acc")
axes[1].plot(history_final.history["val_accuracy"], label="Val acc")
axes[1].set_title("Accuracy over epochs")
axes[1].set_xlabel("Epoch")
axes[1].legend()
plt.tight_layout()
plt.show()

# Decision boundaries — train vs test
plot_decision_boundary(model_final, X_train, y_train, "Final model — Training data")
plot_decision_boundary(model_final, X_test,  y_test,  "Final model — Test data")

# ============================================================
# 9. Summary
# ============================================================
print("""
=== Key Takeaways ===

1. A single dense layer (basic model) cannot learn the circular
   decision boundary — it stays linear → low accuracy (~50%).

2. Adding hidden layers with ReLU lets the network learn
   non-linear boundaries → accuracy jumps to ~99%.

3. Adam converges much faster than SGD on this dataset.

4. ReLU outperforms Sigmoid in hidden layers because it avoids
   the vanishing gradient problem.

5. Visualizing decision boundaries reveals HOW the model thinks,
   not just what accuracy it achieves.

6. Always use a train/test split to detect overfitting early.
""")