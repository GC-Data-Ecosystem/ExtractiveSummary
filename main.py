#Extractive Summerization
#python -m spacy download en_core_web_md
#python -m spacy download fr_core_news_md

import spacy
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Load spaCy models for English and French with word vectors
nlp_en = spacy.load("en_core_web_md")
nlp_fr = spacy.load("fr_core_news_md")

def summarize_text(text, num_sentences):
    # Tokenize the text into sentences using NLTK
    sentences = sent_tokenize(text)

    if len(sentences) < num_sentences:
        print("Error: The number of sentences requested is greater than the number of sentences in the text.")
        return

    # Use spaCy for language-specific text processing
    if text.startswith("Bonjour"):  # Detect if the text is in French
        doc = nlp_fr(text)
    else:
        doc = nlp_en(text)

    # Calculate sentence similarities and rank sentences
    sentence_similarities = []
    for sentence in sentences:
        similarity = doc.similarity(nlp_en(sentence)) if text.startswith("Bonjour") else doc.similarity(nlp_fr(sentence))
        sentence_similarities.append((sentence, similarity))

    # Sort sentences by similarity and select the top ones
    ranked_sentences = [sentence for sentence, similarity in sorted(sentence_similarities, key=lambda x: x[1], reverse=True)]

    # Select the desired number of sentences for the summary (between 3 and 7)
    num_sentences = max(min(num_sentences, 7), 3)
    summary = " ".join(ranked_sentences[:num_sentences])

    return summary

def main():
    filename = input("Enter the path to the text file: ")
    language = input("Enter the language (English or French): ")
    num_sentences = int(input("Enter the number of sentences for the summary (between 3 and 7): "))

    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()

        print(f"Summarizing {filename} ({num_sentences} sentences):")
        summary = summarize_text(text, num_sentences)
        print(summary)
    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
    except ValueError:
        print("Error: Invalid number of sentences. Please enter a number between 3 and 7.")

if __name__ == "__main__":
    main()
