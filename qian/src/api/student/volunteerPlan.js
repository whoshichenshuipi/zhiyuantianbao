import request from '@/utils/request'

// 获取志愿方案列表
export function listVolunteerPlan(query) {
    return request({
        url: '/api/volunteer/plan',
        method: 'get',
        params: query
    })
}

// 获取志愿方案详情
export function getVolunteerPlan(planId) {
    return request({
        url: '/api/volunteer/plan/' + planId,
        method: 'get'
    })
}

// 新增志愿方案
export function addVolunteerPlan(data) {
    return request({
        url: '/api/volunteer/plan',
        method: 'post',
        data: data
    })
}

// 修改志愿方案
export function updateVolunteerPlan(planId, data) {
    return request({
        url: '/api/volunteer/plan/' + planId,
        method: 'put',
        data: data
    })
}

// 删除志愿方案
export function delVolunteerPlan(planId) {
    return request({
        url: '/api/volunteer/plan/' + planId,
        method: 'delete'
    })
}

// 智能推荐
export function getRecommendations(data) {
    return request({
        url: '/api/volunteer/recommend',
        method: 'post',
        data: data
    })
}
