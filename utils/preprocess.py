import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

# Download NLTK data on import
download_nltk_data()

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    Preprocess text for fake news detection
    
    Args:
        text (str): Input text to preprocess
    
    Returns:
        str: Preprocessed text
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Remove special characters and digits, keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        processed_tokens = []
        for token in tokens:
            if token not in stop_words and len(token) > 2:
                lemmatized_token = lemmatizer.lemmatize(token)
                processed_tokens.append(lemmatized_token)
        
        return ' '.join(processed_tokens)
    
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return text  # Return original text if preprocessing fails

def get_text_statistics(text):
    """
    Get basic statistics about the text
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Text statistics
    """
    if not isinstance(text, str):
        return {
            'char_count': 0,
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0,
            'unique_words': 0
        }
    
    try:
        words = text.split()
        sentences = [s for s in text.split('.') if s.strip()]
        
        return {
            'char_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'unique_words': len(set(words))
        }
    except Exception as e:
        print(f"Error getting text statistics: {e}")
        return {
            'char_count': 0,
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0,
            'unique_words': 0
        }