import request from '@/utils/request'

// Mock user data
const mockUsers = {
  'admin': {
    roles: ['admin'],
    permissions: ['*:*:*'],
    user: { userId: 1, userName: 'admin', nickName: '管理员', avatar: '' }
  },
  'student': {
    roles: ['student'],
    permissions: ['student:*:*'],
    user: { userId: 2, userName: 'student', nickName: '考生张三', avatar: '' }
  },
  'college': {
    roles: ['college'],
    permissions: ['college:*:*'],
    user: { userId: 3, userName: 'college', nickName: '北京大学招生办', avatar: '' }
  }
}

let currentUser = mockUsers['admin'] // Default

// 登录方法
export function login(username, password, code, uuid) {
  if (mockUsers[username]) {
    currentUser = mockUsers[username]
    return Promise.resolve({ token: 'mock-token-' + username })
  }
  return Promise.reject({ msg: '用户不存在/密码错误' })
}

// 注册方法
export function register(data) {
  return Promise.resolve({ msg: '注册成功(Mock)', code: 200 })
}

// 获取用户详细信息
export function getInfo() {
  return Promise.resolve(currentUser)
}

// 退出方法
export function logout() {
  return Promise.resolve({ msg: '退出成功', code: 200 })
}

// 获取验证码
export function getCodeImg() {
  return Promise.resolve({
    img: 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
    uuid: 'mock-uuid'
  })
}