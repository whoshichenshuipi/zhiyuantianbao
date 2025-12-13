import request from '@/utils/request'

// 获取院校专业列表
export function listCollegeMajor(query) {
    return request({
        url: '/api/college_major/',
        method: 'get',
        params: query
    })
}

// 获取院校专业详情
export function getCollegeMajor(id) {
    return request({
        url: '/api/college_major/' + id,
        method: 'get'
    })
}

// 新增院校专业
export function addCollegeMajor(data) {
    return request({
        url: '/api/college_major/',
        method: 'post',
        data: data
    })
}

// 修改院校专业
export function updateCollegeMajor(id, data) {
    return request({
        url: '/api/college_major/' + id,
        method: 'put',
        data: data
    })
}

// 删除院校专业
export function delCollegeMajor(id) {
    return request({
        url: '/api/college_major/' + id,
        method: 'delete'
    })
}
