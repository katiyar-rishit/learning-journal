from textblob import TextBlob

text = "I love my life"
blob = TextBlob(text)
print(blob.sentiment.polarity)

tutan = input("Enter:")
blobby = TextBlob(tutan)
print(blobby.sentiment.polarity)
