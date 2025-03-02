# pylint: skip-file
import random
class Song:
    def __init__(self, name, affinity):
        self.name = name
        self.affinity = affinity

songs = [
    Song(f"Song {i}", int(random.uniform(1, 5)))
    for i in range(1, 301)
]

for song in songs:
    print(f'Song("{song.name}"' + ' , ' + f'{song.affinity})')