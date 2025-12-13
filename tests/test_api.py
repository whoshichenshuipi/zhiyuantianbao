"""
接口层集成测试
测试所有业务 API 接口
"""
import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web import create_app, db


@pytest.fixture(scope='module')
def app():
    """创建测试应用"""
    app = create_app('dev')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    """创建测试客户端"""
    return app.test_client()


class TestExaminerAPI:
    """考生信息接口测试"""
    
    def test_get_examiner_list(self, client):
        """测试获取考生信息列表"""
        response = client.get('/api/examiner/info/1')
        # 由于需要登录，应返回401或相应错误
        assert response.status_code in [200, 401, 404]


class TestCollegeMajorAPI:
    """院校专业接口测试"""
    
    def test_get_college_major_list(self, client):
        """测试获取院校专业列表"""
        response = client.get('/api/college_major/')
        assert response.status_code in [200, 401]
        
    def test_response_format(self, client):
        """测试响应格式"""
        response = client.get('/api/college_major/')
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'code' in data
            assert 'msg' in data


class TestVolunteerPlanAPI:
    """志愿方案接口测试"""
    
    def test_get_volunteer_plans(self, client):
        """测试获取志愿方案列表"""
        response = client.get('/api/volunteer/plan')
        assert response.status_code in [200, 401]
    
    def test_recommend_endpoint(self, client):
        """测试智能推荐接口"""
        response = client.post('/api/volunteer/recommend',
                               data=json.dumps({'user_id': 1, 'score': 600}),
                               content_type='application/json')
        assert response.status_code in [200, 401]


class TestAdmissionDataAPI:
    """录取数据接口测试"""
    
    def test_get_admission_data_list(self, client):
        """测试获取录取数据列表"""
        response = client.get('/api/admission_data/')
        assert response.status_code in [200, 401]


class TestCommunityAPI:
    """社区接口测试"""
    
    def test_get_community_list(self, client):
        """测试获取社区内容列表"""
        response = client.get('/api/community/')
        assert response.status_code in [200, 401]


class TestNewsAPI:
    """资讯接口测试"""
    
    def test_get_news_list(self, client):
        """测试获取资讯列表"""
        response = client.get('/api/news/')
        assert response.status_code in [200, 401]


class TestFeedbackAPI:
    """反馈接口测试"""
    
    def test_get_feedback_list(self, client):
        """测试获取反馈列表"""
        response = client.get('/api/feedback/')
        assert response.status_code in [200, 401]


class TestCustomerServiceAPI:
    """客服接口测试"""
    
    def test_get_customer_service_list(self, client):
        """测试获取客服记录列表"""
        response = client.get('/api/customer_service/')
        assert response.status_code in [200, 401]


class TestCollegeInfoAPI:
    """高校信息接口测试"""
    
    def test_get_college_info_list(self, client):
        """测试获取高校信息列表"""
        response = client.get('/api/college_info/')
        assert response.status_code in [200, 401]


class TestCollegeStudentSourceAPI:
    """生源数据接口测试"""
    
    def test_get_student_source_list(self, client):
        """测试获取生源数据列表"""
        response = client.get('/api/college_student_source/')
        assert response.status_code in [200, 401]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
