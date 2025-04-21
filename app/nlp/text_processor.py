import nltk
import re
import logging
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextProcessor:
    def __init__(self):
        self.logger = logging.getLogger('nlp.text_processor')
        self.stop_words = set(stopwords.words('english'))
    
    def process(self, text):
        """Process text: clean, rephrase, and optimize"""
        if not text:
            return ""
        
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        # Rephrase the text
        rephrased_text = self.rephrase_text(cleaned_text)
        
        return rephrased_text
    
    def clean_text(self, text):
        """Clean the text by removing unwanted elements"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'"]', '', text)
        
        return text.strip()
    
    def rephrase_text(self, text):
        """Rephrase the text to avoid plagiarism"""
        # This is a simple implementation
        # In a production system, you would use more sophisticated NLP techniques
        
        # Split text into sentences
        sentences = sent_tokenize(text)
        rephrased_sentences = []
        
        for sentence in sentences:
            # Simple rephrasing by changing word order or adding/removing words
            # This is just a placeholder for demonstration
            rephrased = self._simple_rephrase(sentence)
            rephrased_sentences.append(rephrased)
        
        return ' '.join(rephrased_sentences)
    
    def _simple_rephrase(self, sentence):
        """Simple rephrasing of a sentence"""
        # This is a very basic implementation
        # In a real system, you would use more sophisticated techniques
        
        # Remove some stop words
        words = sentence.split()
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        
        # If we removed too many words, keep the original
        if len(filtered_words) < len(words) * 0.7:
            return sentence
        
        # Add some transition words at the beginning
        transitions = [
            "Notably, ", "Interestingly, ", "According to reports, ", 
            "As per the news, ", "Sources indicate that ", "It appears that ",
            "Reports suggest that ", "It is reported that ", "Evidently, ",
            ""  # Empty string for no transition
        ]
        
        import random
        transition = random.choice(transitions)
        
        # Combine transition with filtered words
        rephrased = transition + ' '.join(filtered_words)
        
        # Ensure proper capitalization and ending punctuation
        rephrased = rephrased[0].upper() + rephrased[1:]
        if not rephrased.endswith(('.', '!', '?')):
            rephrased += '.'
        
        return rephrased
    
    def summarize(self, text, max_sentences=3):
        """Generate a summary of the text"""
        # Split text into sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Simple extractive summarization
        # In a real system, you would use more sophisticated techniques
        
        # Calculate word frequency
        word_freq = {}
        for sentence in sentences:
            for word in sentence.lower().split():
                if word not in self.stop_words:
                    if word not in word_freq:
                        word_freq[word] = 1
                    else:
                        word_freq[word] += 1
        
        # Calculate sentence scores based on word frequency
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            score = 0
            for word in sentence.lower().split():
                if word in word_freq:
                    score += word_freq[word]
            sentence_scores[i] = score / max(1, len(sentence.split()))
        
        # Get top sentences
        top_indices = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
        top_indices.sort()  # Sort by original order
        
        summary = ' '.join([sentences[i] for i in top_indices])
        return summary