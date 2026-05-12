class Text:
    def __init__(self, text):
        self.text = text
    
    def word_frequency(self, word):
        words = self.text.split()  # Step 1: split into list
        
        count = words.count(word)  # Step 2: count occurrences
        
        if count == 0:
            return None  # or return "Word not found"
        
        return count
    
    def most_common_word(self):
        words = self.text.split()
        words_frequencies = {}
        for word in words:
            if word not in words :
                words_frequencies[word] == 1
            else:
                words_frequencies[word] += 1
        
        most_common = None
        highest_count = 0

        for word, count in words_frequencies.items():
            if count > highest_count:
                highest_count = count
                most_common = word

        return most_common

    def unique_words(self):
        words = self.text.split()
        unique = set(words)
        return list(unique)
    
    def from_file(self, file_path):
        with open(file_path, "r") as f:
            content = f.read()

       
           

       
