"""
志愿推荐服务
基于考生分数、兴趣、地域偏好进行智能推荐
"""
from web.models.college_major import CollegeMajor
from web.models.admission_data import AdmissionData
from web.models.examiner_info import ExaminerInfo


def get_recommendations(user_id, score, region_pref=None, interest=None, limit=10):
    """
    获取志愿推荐列表
    
    Args:
        user_id: 用户ID
        score: 高考分数
        region_pref: 地域偏好（可选）
        interest: 兴趣爱好（可选）
        limit: 返回数量限制
        
    Returns:
        list: 推荐院校专业列表，包含概率和风险等级
    """
    recommendations = []
    
    # 查询符合条件的院校专业
    query = CollegeMajor.query
    if region_pref:
        query = query.filter(CollegeMajor.region.like(f'%{region_pref}%'))
    
    majors = query.limit(50).all()
    
    for major in majors:
        # 获取该专业的历年录取数据
        admission = AdmissionData.query.filter_by(
            college_id=major.college_id,
            major_id=major.major_id
        ).order_by(AdmissionData.year.desc()).first()
        
        if admission:
            # 计算录取概率
            probability, risk_level = calculate_probability(score, admission.score_line, admission.rank)
            
            recommendations.append({
                'college_id': major.college_id,
                'major_id': major.major_id,
                'region': major.region,
                'level': major.level,
                'category': major.category,
                'score_line': admission.score_line if admission else None,
                'probability': probability,
                'risk_level': risk_level
            })
    
    # 按概率排序，返回前N个
    recommendations.sort(key=lambda x: x['probability'], reverse=True)
    return recommendations[:limit]


def calculate_probability(score, score_line, rank):
    """
    计算录取概率
    
    Args:
        score: 考生分数
        score_line: 录取分数线
        rank: 位次
        
    Returns:
        tuple: (概率, 风险等级)
    """
    if not score_line:
        return 0.5, '未知'
    
    diff = score - score_line
    
    if diff >= 30:
        return 0.95, '低'
    elif diff >= 15:
        return 0.85, '低'
    elif diff >= 5:
        return 0.70, '中'
    elif diff >= 0:
        return 0.55, '中'
    elif diff >= -10:
        return 0.35, '高'
    else:
        return 0.15, '极高'
