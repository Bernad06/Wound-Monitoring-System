from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'message': 'WoundCare AI API is running!',
        'status': 'success',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            'GET /',
            'GET /api/test', 
            'POST /api/analyze'
        ]
    })

@app.route('/api/test')
def test():
    """Test endpoint to verify API connectivity"""
    return jsonify({
        'test': 'API working perfectly!',
        'backend': 'Flask with OpenCV ready',
        'mobile': 'Mobile app compatible',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_wound():
    """Main wound analysis endpoint"""
    try:
        # Get image data from request
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        print(f"📷 Received image data: {len(image_data)} characters")
        print(f"🕐 Analysis timestamp: {timestamp}")
        
        # Simulate processing time for realistic demo
        import time
        time.sleep(2)  # 2 second delay to show "analyzing..." state
        
        # For hackathon demo - return realistic mock results
        # TODO: Replace with real OpenCV analysis
        mock_results = {
            'healing_score': round(75.8 + (hash(image_data) % 20), 1),  # Varies by image
            'wound_area_pixels': 1200 + (hash(image_data) % 500),       # Varies by image
            'inflammation_level': round(15.0 + (hash(image_data) % 15), 1),
            'tissue_health_score': round(78.5 + (hash(image_data) % 15), 1),
            'confidence': round(0.85 + (hash(image_data) % 10) / 100, 2),
            'timestamp': timestamp,
            'analysis_version': '1.0.0',
            'processing_time': '2.1s',
            'recommendation': generate_recommendation(),
            'status': 'analysis_complete',
            'patient_id': 'demo_patient_001',
            'image_quality': 'excellent'
        }
        
        print(f"🔬 Analysis complete: Healing Score {mock_results['healing_score']}%")
        
        return jsonify(mock_results)
        
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        print(f"❌ Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

def generate_recommendation():
    """Generate realistic medical recommendations"""
    recommendations = [
        "Wound shows positive healing progress. Continue current treatment protocol.",
        "Good granulation tissue development observed. Monitor for continued improvement.",
        "Healing progressing well. Consider reducing dressing change frequency.",
        "Excellent tissue regeneration. Patient responding well to treatment.",
        "Normal healing pattern detected. Maintain current care routine.",
        "Wound edges showing good approximation. Continue with prescribed therapy.",
    ]
    
    import random
    return random.choice(recommendations)

@app.route('/api/patient/<patient_id>/history')
def get_patient_history(patient_id):
    """Get patient wound analysis history (mock data for demo)"""
    try:
        # Mock historical data for demo
        mock_history = [
            {
                'date': '2024-01-15',
                'healing_score': 65.2,
                'wound_area': 1500,
                'inflammation': 28.5
            },
            {
                'date': '2024-01-18', 
                'healing_score': 72.1,
                'wound_area': 1350,
                'inflammation': 22.0
            },
            {
                'date': '2024-01-20',
                'healing_score': 75.8,
                'wound_area': 1200,
                'inflammation': 18.5
            }
        ]
        
        return jsonify({
            'patient_id': patient_id,
            'history': mock_history,
            'total_records': len(mock_history),
            'improvement_trend': 'positive'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_system_stats():
    """Get system statistics for admin dashboard"""
    try:
        return jsonify({
            'total_analyses': 247,
            'avg_healing_score': 73.2,
            'active_patients': 45,
            'system_uptime': '99.8%',
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'API endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

@app.before_request
def log_request():
    """Log all API requests"""
    if request.method == 'POST':
        print(f"📡 {request.method} {request.path} - Content-Length: {request.content_length}")
    else:
        print(f"📡 {request.method} {request.path}")

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Starting WoundCare AI Backend Server")
    print("=" * 50)
    print("📱 Mobile App Backend Ready")
    print("🔗 Frontend should connect to: http://localhost:5000")
    print("🏥 Healthcare API v1.0.0")
    print("=" * 50)
    
    # Start the Flask development server
    app.run(
        debug=True, 
        host='0.0.0.0',  # Accept connections from any IP (for mobile testing)
        port=5000,
        threaded=True    # Handle multiple requests simultaneously
    )