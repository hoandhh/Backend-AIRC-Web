# routes/admin_controller.py
from flask import Blueprint
from controllers.admin_controller import (
    get_all_users, update_user, delete_user, get_all_images, 
    admin_delete_image, get_reports, update_report, get_stats
)

admin_routes = Blueprint('admin_routes', __name__)

admin_routes.route('/users', methods=['GET'])(get_all_users)
admin_routes.route('/users/<user_id>', methods=['PUT'])(update_user)
admin_routes.route('/users/<user_id>', methods=['DELETE'])(delete_user)
admin_routes.route('/images', methods=['GET'])(get_all_images)
admin_routes.route('/images/<image_id>', methods=['DELETE'])(admin_delete_image)
admin_routes.route('/reports', methods=['GET'])(get_reports)
admin_routes.route('/reports/<report_id>', methods=['PUT'])(update_report)
admin_routes.route('/stats', methods=['GET'])(get_stats)
