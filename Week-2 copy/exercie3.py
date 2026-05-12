class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics 

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)

happy_birthday = Song([
    "Happy birthday to you",
    "Happy birthday to you",
    "Happy birthday dear friend",
    "Happy birthday to you"
])

happy_birthday.sing_me_a_song()