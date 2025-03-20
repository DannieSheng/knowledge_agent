from flask import Blueprint, jsonify
from fetch_data import fetch_all_ai_blogs_with_categories, fetch_all_ai_blogs

api = Blueprint('api', __name__)

@api.route('/api/news', methods=['GET'])
def get_news():
    """API Endpoint to get AI news"""
    blogs = fetch_all_ai_blogs_with_categories()
    # for blog in blogs:
    #     # Ensure summary & categories exist
    #     blog["categories"] = blog.get("categories", ["Uncategorized"])
    #     # blog["summary_en"] = blog.get("summary_en", "No summary available")
    #     # blog["summary_zh"] = blog.get("summary_zh", "暂无摘要")
    #     # print(f"DEBUG: (after) {blog.get("summary_en")}")
    #     # print(f"DEBUG: (after) {blog.get("summary_zh")}")
    # # print("DEBUG: API Response:", blogs)  # ✅ Debugging line
    return jsonify(blogs)

# @api.route('/api/blogs', methods=['GET'])
# def get_blogs():
#     """API Endpoint to get AI news"""
#     blogs = fetch_all_ai_blogs()
#     return jsonify(blogs)