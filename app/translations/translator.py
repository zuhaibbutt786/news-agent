import logging
from googletrans import Translator as GoogleTranslator
import time

class Translator:
    def __init__(self):
        self.logger = logging.getLogger('translations.translator')
        self.translator = GoogleTranslator()
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def translate_to_urdu(self, text, src='en', dest='ur'):
        """Translate text to Urdu"""
        if not text:
            return ""
        
        # Split text into chunks to avoid translation limits
        chunks = self._split_text(text)
        translated_chunks = []
        
        for chunk in chunks:
            translated_chunk = self._translate_with_retry(chunk, src, dest)
            translated_chunks.append(translated_chunk)
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
        
        return ' '.join(translated_chunks)
    
    def _translate_with_retry(self, text, src='en', dest='ur'):
        """Translate text with retry mechanism"""
        for attempt in range(self.max_retries):
            try:
                translation = self.translator.translate(text, src=src, dest=dest)
                return translation.text
            except Exception as e:
                self.logger.warning(f"Translation attempt {attempt+1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error(f"Translation failed after {self.max_retries} attempts")
                    return text  # Return original text if translation fails
    
    def _split_text(self, text, max_chunk_size=1000):
        """Split text into chunks to avoid translation limits"""
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by sentences to avoid cutting in the middle of a sentence
        sentences = text.split('. ')
        
        for sentence in sentences:
            # Add period back if it was removed during split
            if not sentence.endswith('.'):
                sentence += '.'
            
            # If adding this sentence would exceed the chunk size, start a new chunk
            if len(current_chunk) + len(sentence) + 1 > max_chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += ' ' + sentence
                else:
                    current_chunk = sentence
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks