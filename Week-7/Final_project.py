# ============================================================

# Mini Project: Sentiment Assistant with BERT Fine-Tuning

# ============================================================

# Install first in terminal if needed:

# pip3 install tensorflow tensorflow-datasets transformers accelerate evaluate

import platform
import tensorflow as tf
import tensorflow_datasets as tfds
from transformers import BertTokenizer, TFBertForSequenceClassification

# ============================================================

# 1. Imports & Hardware Check

# ============================================================

print("Python version      :", platform.python_version())
print("TensorFlow version  :", tf.__version__)
print("GPU devices detected:", tf.config.list_physical_devices("GPU"))

# 2. Load IMDB Reviews Dataset

(ds_train, ds_test), ds_info = tfds.load(
    "imdb_reviews",
    split=(tfds.Split.TRAIN, tfds.Split.TEST),
    as_supervised=True,
    with_info=True
)

print(ds_info)
for text, label in ds_train.take(2):
    print("Label:", "Positive" if label.numpy() else "Negative")
    print(text.numpy().decode()[:250], "...\n")

# 3. Tokenizer Setup & Data Pipeline


MAX_LENGTH = 256
BATCH_SIZE = 16
tokenizer = BertTokenizer.from_pretrained(
    "bert-base-uncased",
    do_lower_case=True
)

print("Tokenizer loaded:", tokenizer.name_or_path)
def encode_review(review_input):
    if isinstance(review_input, bytes):
        review_text = review_input.decode("utf-8")
    elif hasattr(review_input, "numpy"):
        review_text = review_input.numpy().decode("utf-8")
    else:
        review_text = str(review_input)
    return tokenizer.encode_plus(
        review_text,
        add_special_tokens=True,
        max_length=MAX_LENGTH,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_token_type_ids=True,
    )

def tf_encode(text, label):
    encoded = tf.py_function(
        func=lambda t: list(encode_review(t).values()),
        inp=[text],
        Tout=[tf.int32, tf.int32, tf.int32]
    )

    input_ids = encoded[0]
    attention_mask = encoded[1]
    token_type_ids = encoded[2]
    input_ids.set_shape([MAX_LENGTH])
    attention_mask.set_shape([MAX_LENGTH])
    token_type_ids.set_shape([MAX_LENGTH])
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "token_type_ids": token_type_ids
    }, label

def prepare_dataset(dataset, shuffle=True):
    dataset = dataset.map(tf_encode, num_parallel_calls=tf.data.AUTOTUNE)
    if shuffle:
        dataset = dataset.shuffle(2000)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    return dataset
train_ds = prepare_dataset(ds_train, shuffle=True)
test_ds = prepare_dataset(ds_test, shuffle=False)

# 4. Initialize Fine-Tuning Model

model = TFBertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2,
    use_safetensors=False
)

optimizer = tf.keras.optimizers.Adam(
    learning_rate=2e-5,
    epsilon=1e-8
)

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True
)
metrics = [
    tf.keras.metrics.SparseCategoricalAccuracy(name="accuracy")
]
model.compile(
    optimizer=optimizer,
    loss=loss_fn,
    metrics=metrics
)
model.summary()

# 5. Train and Monitor

EPOCHS = 2
history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=EPOCHS
)

# 6. Evaluate on the Test Set

eval_metrics = model.evaluate(test_ds)
print("\nEvaluation results:")
print("Test loss:", eval_metrics[0])
print("Test accuracy:", eval_metrics[1])

# 7. Reusable Inference Helper

def predict_sentiment(text: str):
    encoded = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=MAX_LENGTH,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_token_type_ids=True,
        return_tensors="tf"
    )
    outputs = model(encoded)
    probs = tf.nn.softmax(outputs.logits, axis=1).numpy()[0]
    predicted_class = probs.argmax()
    label = "Positive" if predicted_class == 1 else "Negative"
    confidence = float(probs.max())
    return label, confidence

custom_sentence = "The onboarding emails were confusing, but the agent fixed everything politely."
label, confidence = predict_sentiment(custom_sentence)
print("\nCustom sentence:")
print(custom_sentence)
print(f"Prediction: {label} (confidence={confidence:.3f})")

# 8. Reflection

print("\nReflection:")
print("""
The most important lever for improving results is usually fine-tuning the model for enough epochs while keeping a small learning rate.
Data cleaning can also improve performance because noisy or mislabeled reviews can confuse the model.
Before deploying this sentiment signal live, I would add guardrails such as human review for low-confidence predictions,
monitoring for biased outputs, and regular checks for data drift.
The stakeholders who benefit the most are the support lead, product manager, and compliance officer.
The support lead can prioritize angry customers, the product manager can identify recurring issues,
and the compliance officer can monitor risky or sensitive customer interactions.
""")