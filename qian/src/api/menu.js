import request from '@/utils/request'
import { mockRouters } from '../mockRouters'

// 获取路由
export const getRouters = () => {
  return Promise.resolve(mockRouters)
  // return request({
  //   url: '/getRouters',
  //   method: 'get'
  // })
}