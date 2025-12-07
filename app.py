from flask import Flask, request, jsonify

app = Flask(__name__)

def analyze_sentiment(text):
    """Simple sentiment analysis based on keywords"""
    text_lower = text.lower()
    
    # Positive keywords
    if any(word in text_lower for word in ['love', 'like', 'good', 'great', 'excellent', 'awesome', 'best']):
        return 'positive', 0.9
    
    # Negative keywords
    elif any(word in text_lower for word in ['hate', 'bad', 'terrible', 'awful', 'worst', 'horrible']):
        return 'negative', 0.9
    
    # Neutral keywords or default
    elif any(word in text_lower for word in ['okay', 'fine', 'average', 'decent']):
        return 'neutral', 0.7
    
    # Default to neutral
    else:
        return 'neutral', 0.6

@app.route('/')
def home():
    return jsonify({
        "service": "Sentiment Analysis API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "POST /predict": "Analyze sentiment"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if 'text' not in data:
            return jsonify({"error": "Missing 'text' field in JSON"}), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        sentiment, confidence = analyze_sentiment(text)
        
        return jsonify({
            "text": text,
            "sentiment": sentiment,
            "confidence": confidence,
            "success": True
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("SENTIMENT ANALYSIS API")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print()
    print("Test with these commands:")
    print("1. curl http://localhost:5000/")
    print("2. curl http://localhost:5000/health")
    print('3. curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"text\": \"I love this!\"}"')
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
