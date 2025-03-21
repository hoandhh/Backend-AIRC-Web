# routes/image_controller.py
from flask import Blueprint
from controllers.image_controller import (
    upload_image, get_image, get_public_images, get_user_images, 
    update_image, add_caption, delete_image, report_image
)

image_routes = Blueprint('image_routes', __name__)

image_routes.route('/', methods=['POST'])(upload_image)
image_routes.route('/file/<filename>', methods=['GET'])(get_image)
image_routes.route('/', methods=['GET'])(get_public_images)
image_routes.route('/my-images', methods=['GET'])(get_user_images)
image_routes.route('/<image_id>', methods=['PUT'])(update_image)
image_routes.route('/<image_id>/caption', methods=['POST'])(add_caption)
image_routes.route('/<image_id>', methods=['DELETE'])(delete_image)
image_routes.route('/<image_id>/report', methods=['POST'])(report_image)
