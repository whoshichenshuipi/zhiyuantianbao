"""
录取概率计算服务
基于历年分数线和位次计算录取概率
"""
from web.models.admission_data import AdmissionData
from web.models.volunteer_plan import VolunteerPlan


def calculate_admission_probability(plan_id):
    """
    计算单个志愿方案的录取概率
    
    Args:
        plan_id: 志愿方案ID
        
    Returns:
        dict: 包含概率、风险等级、分析数据
    """
    plan = VolunteerPlan.query.get(plan_id)
    if not plan:
        return None
    
    # 获取历年录取数据
    admission_records = AdmissionData.query.filter_by(
        college_id=plan.college_id,
        major_id=plan.major_id
    ).order_by(AdmissionData.year.desc()).limit(3).all()
    
    if not admission_records:
        return {
            'probability': 0.5,
            'risk_level': '未知',
            'analysis': '暂无历年录取数据，无法准确评估'
        }
    
    # 计算平均分数线
    avg_score = sum(r.score_line for r in admission_records if r.score_line) / len(admission_records)
    
    # TODO: 从 examiner_info 获取用户分数
    user_score = 550  # 临时值
    
    probability, risk_level = _calculate_prob(user_score, avg_score)
    
    analysis = f"近{len(admission_records)}年平均录取分数线: {avg_score:.0f}分。"
    if probability >= 0.7:
        analysis += "录取可能性较高，建议作为稳妥选择。"
    elif probability >= 0.4:
        analysis += "录取可能性中等，可作为冲刺目标。"
    else:
        analysis += "录取可能性较低，建议谨慎选择。"
    
    return {
        'probability': probability,
        'risk_level': risk_level,
        'analysis': analysis,
        'avg_score_line': avg_score,
        'years_analyzed': len(admission_records)
    }


def batch_calculate(user_id):
    """
    批量计算用户所有志愿方案的录取概率
    
    Args:
        user_id: 用户ID
        
    Returns:
        list: 所有方案的概率分析结果
    """
    plans = VolunteerPlan.query.filter_by(user_id=user_id).all()
    results = []
    
    for plan in plans:
        result = calculate_admission_probability(plan.plan_id)
        if result:
            result['plan_id'] = plan.plan_id
            result['college_id'] = plan.college_id
            result['major_id'] = plan.major_id
            results.append(result)
    
    return results


def _calculate_prob(score, score_line):
    """内部概率计算函数"""
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
