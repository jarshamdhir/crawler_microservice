from flask import Blueprint, jsonify, request
from app.services.crawler import PunjabiCrawler

api_bp = Blueprint('api', __name__)


@api_bp.route("/crawl-single", methods=["POST"])
def crawl_single():
    """Crawl a single URL for Punjabi content."""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        crawler = PunjabiCrawler(delay=0.5, max_pages=10)
        result = crawler.crawl_single_url(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/crawl-website", methods=["POST"])
def crawl_website():
    """Crawl a website for Punjabi content."""
    data = request.json
    url = data.get('url')
    max_depth = data.get('max_depth', 1)
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        crawler = PunjabiCrawler(delay=1.0, max_pages=50)
        result = crawler.crawl_website(url, max_depth=max_depth)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/detect-punjabi", methods=["POST"])
def detect_punjabi():
    """Detect Punjabi content in provided text."""
    data = request.json
    text = data.get('text', '')
    
    try:
        crawler = PunjabiCrawler()
        is_punjabi = crawler.is_punjabi_content(text)
        return jsonify({"is_punjabi": is_punjabi, "text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Punjabi Crawler API!"})