import request from '@/utils/request'

// 获取反馈列表
export function listFeedback(query) {
    return request({
        url: '/api/feedback/',
        method: 'get',
        params: query
    })
}

// 获取反馈详情
export function getFeedback(id) {
    return request({
        url: '/api/feedback/' + id,
        method: 'get'
    })
}

// 新增反馈
export function addFeedback(data) {
    return request({
        url: '/api/feedback/',
        method: 'post',
        data: data
    })
}

// 修改反馈
export function updateFeedback(id, data) {
    return request({
        url: '/api/feedback/' + id,
        method: 'put',
        data: data
    })
}

// 删除反馈
export function delFeedback(id) {
    return request({
        url: '/api/feedback/' + id,
        method: 'delete'
    })
}
