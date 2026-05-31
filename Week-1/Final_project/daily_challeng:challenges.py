# ============================================================
# Challenge 1: Sorting
# ============================================================

words_input = input("Enter words separated by commas: ")
words_list  = words_input.split(",")
words_sorted = sorted(words_list)
result = ",".join(words_sorted)
print(result)

# Test
# Input:  without,hello,bag,world
# Output: bag,hello,without,world


# ============================================================
# Challenge 2: Longest Word
# ============================================================

def longest_word(sentence):
    words       = sentence.split()
    longest     = ""
    for word in words:
        if len(word) > len(longest):
            longest = word
    return longest


# Tests
print(longest_word("Margaret's toy is a pretty doll."))
# → Margaret's

print(longest_word("A thing of beauty is a joy forever."))
# → forever.

print(longest_word("Forgetfulness is by all means powerless!"))
# → Forgetfulness