from flask import Blueprint

# Main blueprint for the application
main_routes = Blueprint('base', __name__)

# Import all controller blueprints
from ..controller import (
    examiner_info,
    college_major,
    admission_data,
    admission_probability,
    community_content,
    news_policy,
    feedback_complaint,
    customer_service,
    college_info,
    college_student_source,
    # existing system controllers can be added here
)

# Register blueprints
main_routes.register_blueprint(examiner_info.examiner_bp)
main_routes.register_blueprint(college_major.college_major_bp)
main_routes.register_blueprint(admission_data.admission_data_bp)
main_routes.register_blueprint(admission_probability.admission_prob_bp)
main_routes.register_blueprint(community_content.community_bp)
main_routes.register_blueprint(news_policy.news_bp)
main_routes.register_blueprint(feedback_complaint.feedback_bp)
main_routes.register_blueprint(customer_service.cs_bp)
main_routes.register_blueprint(college_info.college_info_bp)
main_routes.register_blueprint(college_student_source.college_source_bp)