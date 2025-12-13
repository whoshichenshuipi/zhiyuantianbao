import request from '@/utils/request'

// 获取资讯列表
export function listNews(query) {
    return request({
        url: '/api/news/',
        method: 'get',
        params: query
    })
}

// 获取资讯详情
export function getNews(id) {
    return request({
        url: '/api/news/' + id,
        method: 'get'
    })
}

// 新增资讯
export function addNews(data) {
    return request({
        url: '/api/news/',
        method: 'post',
        data: data
    })
}

// 修改资讯
export function updateNews(id, data) {
    return request({
        url: '/api/news/' + id,
        method: 'put',
        data: data
    })
}

// 删除资讯
export function delNews(id) {
    return request({
        url: '/api/news/' + id,
        method: 'delete'
    })
}
