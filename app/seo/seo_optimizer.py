import logging
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Download necessary NLTK data
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class SEOOptimizer:
    def __init__(self):
        self.logger = logging.getLogger('seo.optimizer')
        self.stop_words = set(stopwords.words('english'))
    
    def optimize(self, title, content, category=None):
        """Generate SEO metadata for an article"""
        # Generate meta title
        meta_title = self._generate_meta_title(title, category)
        
        # Generate meta description
        meta_description = self._generate_meta_description(content)
        
        # Extract keywords
        keywords = self._extract_keywords(title, content, category)
        
        return {
            'meta_title': meta_title,
            'meta_description': meta_description,
            'keywords': keywords
        }
    
    def _generate_meta_title(self, title, category=None):
        """Generate an SEO-friendly meta title"""
        # Limit title length to 60 characters
        short_title = title[:57] + '...' if len(title) > 60 else title
        
        # Add category if provided
        if category:
            # Ensure the total length is still under 60 characters
            if len(short_title) + len(category) + 3 <= 60:
                return f"{short_title} | {category}"
        
        return short_title
    
    def _generate_meta_description(self, content, max_length=160):
        """Generate an SEO-friendly meta description"""
        # Clean the content
        clean_content = re.sub(r'\s+', ' ', content).strip()
        
        # Extract the first few sentences
        sentences = re.split(r'(?<=[.!?])\s+', clean_content)
        description = ""
        
        for sentence in sentences:
            if len(description) + len(sentence) + 1 <= max_length:
                if description:
                    description += " " + sentence
                else:
                    description = sentence
            else:
                break
        
        # If the description is still too long, truncate it
        if len(description) > max_length:
            description = description[:max_length-3] + "..."
        
        return description
    
    def _extract_keywords(self, title, content, category=None, max_keywords=5):
        """Extract relevant keywords from the article"""
        # Combine title and content
        text = f"{title} {content}"
        
        # Tokenize and convert to lowercase
        words = word_tokenize(text.lower())
        
        # Remove stop words and non-alphabetic tokens
        filtered_words = [word for word in words if word.isalpha() and word not in self.stop_words]
        
        # Count word frequencies
        word_freq = Counter(filtered_words)
        
        # Get the most common words
        common_words = [word for word, count in word_freq.most_common(max_keywords)]
        
        # Add category as a keyword if provided
        if category and category.lower() not in common_words:
            common_words = [category.lower()] + common_words[:max_keywords-1]
        
        return ", ".join(common_words)