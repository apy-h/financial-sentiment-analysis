from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class SentimentAnalyzer:
    """Sentiment analyzer using FinBERT model"""
    
    def __init__(self, model_name='ProsusAI/finbert'):
        """
        Initialize the sentiment analyzer with FinBERT model
        
        Args:
            model_name: HuggingFace model identifier (default: ProsusAI/finbert)
        """
        print(f"Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        self.labels = ['positive', 'negative', 'neutral']
        print("Model loaded successfully")
    
    def analyze(self, text):
        """
        Analyze sentiment of text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment label, score, and all scores
        """
        if not text or not text.strip():
            return {
                'label': 'neutral',
                'score': 0.0,
                'scores': {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34}
            }
        
        # Tokenize and prepare input
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predictions = predictions.cpu().numpy()[0]
        
        # Map predictions to labels
        scores = {
            self.labels[i]: float(predictions[i])
            for i in range(len(self.labels))
        }
        
        # Get the dominant sentiment
        max_idx = np.argmax(predictions)
        label = self.labels[max_idx]
        score = float(predictions[max_idx])
        
        return {
            'label': label,
            'score': score,
            'scores': scores
        }
    
    def analyze_batch(self, texts):
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment dictionaries
        """
        return [self.analyze(text) for text in texts]
