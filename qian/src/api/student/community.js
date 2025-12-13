import request from '@/utils/request'

// 获取社区讨论列表
export function listCommunity(query) {
    return request({
        url: '/api/community/',
        method: 'get',
        params: query
    })
}

// 获取社区讨论详情
export function getCommunity(id) {
    return request({
        url: '/api/community/' + id,
        method: 'get'
    })
}

// 新增社区讨论
export function addCommunity(data) {
    return request({
        url: '/api/community/',
        method: 'post',
        data: data
    })
}

// 修改社区讨论
export function updateCommunity(id, data) {
    return request({
        url: '/api/community/' + id,
        method: 'put',
        data: data
    })
}

// 删除社区讨论
export function delCommunity(id) {
    return request({
        url: '/api/community/' + id,
        method: 'delete'
    })
}
