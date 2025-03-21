# controllers/image_controller.py
from flask import request, jsonify, Blueprint, send_from_directory
from services.image_service import ImageService
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

image_controller = Blueprint('image_controller', __name__)

@image_controller.route('/', methods=['POST'])
@jwt_required()
def upload_image():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'Không có phần tệp'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Không có tệp được chọn'}), 400
    
    if file and allowed_file(file.filename):
        try:
            image = ImageService.upload_image(
                file=file,
                title=request.form.get('title', 'Không có tiêu đề'),
                description=request.form.get('description', ''),
                user_id=user_id,
                is_public=request.form.get('is_public', 'true').lower() == 'true'
            )
            return jsonify({
                'id': str(image.id),
                'title': image.title,
                'url': f"/api/images/file/{image.file_path}"
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Loại tệp không được phép'}), 400

@image_controller.route('/file/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(ImageService.UPLOAD_FOLDER, filename)

@image_controller.route('/', methods=['GET'])
def get_public_images():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    images = ImageService.get_public_images(page, per_page)
    
    return jsonify({
        'images': [
            {
                'id': str(img.id),
                'title': img.title,
                'description': img.description,
                'url': f"/api/images/file/{img.file_path}",
                'created_at': img.created_at,
                'captions': img.captions
            } for img in images.items
        ],
        'total': images.total,
        'pages': images.pages,
        'page': images.page
    }), 200

@image_controller.route('/my-images', methods=['GET'])
@jwt_required()
def get_user_images():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    images = ImageService.get_user_images(user_id, page, per_page)
    
    return jsonify({
        'images': [
            {
                'id': str(img.id),
                'title': img.title,
                'description': img.description,
                'url': f"/api/images/file/{img.file_path}",
                'created_at': img.created_at,
                'is_public': img.is_public,
                'captions': img.captions
            } for img in images.items
        ],
        'total': images.total,
        'pages': images.pages,
        'page': images.page
    }), 200

@image_controller.route('/<image_id>', methods=['PUT'])
@jwt_required()
def update_image(image_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    updated = ImageService.update_image(image_id, user_id, data)
    if not updated:
        return jsonify({'error': 'Không thể cập nhật hình ảnh hoặc không được phép'}), 403
    
    return jsonify({'message': 'Cập nhật hình ảnh thành công'}), 200

@image_controller.route('/<image_id>/caption', methods=['POST'])
@jwt_required()
def add_caption(image_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'caption' not in data:
        return jsonify({'error': 'Chú thích là bắt buộc'}), 400
    
    success = ImageService.add_caption(image_id, user_id, data['caption'])
    if not success:
        return jsonify({'error': 'Không thể thêm chú thích hoặc không được phép'}), 403
    
    return jsonify({'message': 'Thêm chú thích thành công'}), 200

@image_controller.route('/<image_id>', methods=['DELETE'])
@jwt_required()
def delete_image(image_id):
    user_id = get_jwt_identity()
    
    success = ImageService.delete_image(image_id, user_id)
    if not success:
        return jsonify({'error': 'Không thể xóa hình ảnh hoặc không được phép'}), 403
    
    return jsonify({'message': 'Xóa hình ảnh thành công'}), 200

@image_controller.route('/<image_id>/report', methods=['POST'])
@jwt_required()
def report_image(image_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'reason' not in data:
        return jsonify({'error': 'Lý do báo cáo là bắt buộc'}), 400
    
    success = ImageService.report_image(image_id, user_id, data['reason'])
    if not success:
        return jsonify({'error': 'Không thể báo cáo hình ảnh'}), 400
    
    return jsonify({'message': 'Báo cáo hình ảnh thành công'}), 200

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
