import request from '@/utils/request'

// 获取高校信息列表
export function listCollegeInfo(query) {
    return request({
        url: '/api/college_info/',
        method: 'get',
        params: query
    })
}

// 获取高校信息详情
export function getCollegeInfo(id) {
    return request({
        url: '/api/college_info/' + id,
        method: 'get'
    })
}

// 新增高校信息
export function addCollegeInfo(data) {
    return request({
        url: '/api/college_info/',
        method: 'post',
        data: data
    })
}

// 修改高校信息
export function updateCollegeInfo(id, data) {
    return request({
        url: '/api/college_info/' + id,
        method: 'put',
        data: data
    })
}

// 删除高校信息
export function delCollegeInfo(id) {
    return request({
        url: '/api/college_info/' + id,
        method: 'delete'
    })
}

// 获取生源看板数据
export function getStudentSource(query) {
    return request({
        url: '/api/college_student_source/',
        method: 'get',
        params: query
    })
}
