paragraph = input("Enter a Paragraph: ")

words = paragraph.split()

print("Total number of words:", len(words))

unique_words = set(words)
print("Number of unique words:", len(unique_words))

longest_word = max(words, key=len)
print("Longest word:", longest_word)

shortest_word = min(words, key=len)
print("Shortest word:", shortest_word)