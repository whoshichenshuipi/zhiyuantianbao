"""
模型层单元测试
测试所有业务模型的基本功能
"""
import pytest
import sys
import os

# 添加项目根目录到路径
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


class TestExaminerInfoModel:
    """考生信息模型测试"""
    
    def test_create_examiner_info(self, app):
        """测试创建考生信息"""
        from web.models.examiner_info import ExaminerInfo
        
        with app.app_context():
            examiner = ExaminerInfo(
                user_id=1,
                interest='计算机',
                region_pref='北京',
                subject_strength='数学',
                score=650
            )
            db.session.add(examiner)
            db.session.commit()
            
            assert examiner.examiner_id is not None
            assert examiner.score == 650
            
            # 清理
            db.session.delete(examiner)
            db.session.commit()


class TestCollegeMajorModel:
    """院校专业模型测试"""
    
    def test_create_college_major(self, app):
        """测试创建院校专业"""
        from web.models.college_major import CollegeMajor
        
        with app.app_context():
            major = CollegeMajor(
                college_id=1,
                major_id=101,
                region='北京',
                level='本科',
                category='工学'
            )
            db.session.add(major)
            db.session.commit()
            
            assert major.id is not None
            assert major.region == '北京'
            
            db.session.delete(major)
            db.session.commit()


class TestVolunteerPlanModel:
    """志愿方案模型测试"""
    
    def test_create_volunteer_plan(self, app):
        """测试创建志愿方案"""
        from web.models.volunteer_plan import VolunteerPlan
        
        with app.app_context():
            plan = VolunteerPlan(
                user_id=1,
                college_id=1,
                major_id=101,
                priority=1,
                status='draft'
            )
            db.session.add(plan)
            db.session.commit()
            
            assert plan.plan_id is not None
            assert plan.status == 'draft'
            
            db.session.delete(plan)
            db.session.commit()


class TestAdmissionDataModel:
    """录取数据模型测试"""
    
    def test_create_admission_data(self, app):
        """测试创建录取数据"""
        from web.models.admission_data import AdmissionData
        
        with app.app_context():
            data = AdmissionData(
                college_id=1,
                major_id=101,
                year=2024,
                province='北京',
                score_line=620,
                rank=5000
            )
            db.session.add(data)
            db.session.commit()
            
            assert data.admission_id is not None
            assert data.score_line == 620
            
            db.session.delete(data)
            db.session.commit()


class TestCommunityContentModel:
    """社区内容模型测试"""
    
    def test_create_community_content(self, app):
        """测试创建社区内容"""
        from web.models.community_content import CommunityContent
        
        with app.app_context():
            content = CommunityContent(
                user_id=1,
                title='测试帖子',
                body='这是测试内容',
                type='提问'
            )
            db.session.add(content)
            db.session.commit()
            
            assert content.content_id is not None
            assert content.title == '测试帖子'
            
            db.session.delete(content)
            db.session.commit()


class TestNewsPolicyModel:
    """资讯政策模型测试"""
    
    def test_create_news_policy(self, app):
        """测试创建资讯"""
        from web.models.news_policy import NewsPolicy
        
        with app.app_context():
            news = NewsPolicy(
                title='测试资讯',
                content='资讯内容',
                category='政策',
                status='published'
            )
            db.session.add(news)
            db.session.commit()
            
            assert news.news_id is not None
            assert news.category == '政策'
            
            db.session.delete(news)
            db.session.commit()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
