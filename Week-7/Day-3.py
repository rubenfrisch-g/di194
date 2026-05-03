import pandas as pd
from transformers import BertTokenizer, XLMRobertaTokenizer
from sklearn.model_selection import StratifiedKFold

# =========================
# 1. Load tokenizers
# =========================

bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
xlmr_tokenizer = XLMRobertaTokenizer.from_pretrained("xlm-roberta-base")

print("BERT vocab size:", bert_tokenizer.vocab_size)
print("XLM-R vocab size:", xlmr_tokenizer.vocab_size)

print("BERT special tokens:", bert_tokenizer.special_tokens_map)
print("XLM-R special tokens:", xlmr_tokenizer.special_tokens_map)


# =========================
# 2. Load dataset
# =========================

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

print(train_df.head())
print(test_df.head())

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)

print("Train columns:", train_df.columns)


# =========================
# 3. Tokenize one example
# =========================

premise = train_df.loc[0, "premise"]
hypothesis = train_df.loc[0, "hypothesis"]

encoded = xlmr_tokenizer(
    premise,
    hypothesis,
    add_special_tokens=True,
    max_length=128,
    padding="max_length",
    truncation=True,
    return_attention_mask=True
)

print("Input IDs:")
print(encoded["input_ids"])

print("Attention mask:")
print(encoded["attention_mask"])

print("Decoded text:")
print(xlmr_tokenizer.decode(encoded["input_ids"]))


# =========================
# 4. Explore labels
# =========================

print("Label distribution:")
print(train_df["label"].value_counts())

print("Language distribution:")
print(train_df["language"].value_counts())


# =========================
# 5. Create cross-validation folds
# =========================

X = train_df[["premise", "hypothesis"]]
y = train_df["label"]

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

train_splits = []
val_splits = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):

    train_fold = train_df.iloc[train_idx]
    val_fold = train_df.iloc[val_idx]

    train_splits.append(train_fold)
    val_splits.append(val_fold)

    print(f"\nFold {fold + 1}")
    print("Train size:", train_fold.shape)
    print("Validation size:", val_fold.shape)

    print("Train label distribution:")
    print(train_fold["label"].value_counts(normalize=True))

    print("Validation label distribution:")
    print(val_fold["label"].value_counts(normalize=True))