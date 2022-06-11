import axios from 'axios'

axios.defaults.withCredentials = false // 配置为true
let base = 'http://127.0.0.1:5000'
export const test = 'http://127.0.0.1:5000'
export const delpoySocketIP = `http://0.0.0.0:5001`


export const requestLogin = params => {
  return axios.post(`${base}/login/userLogin`, params).then(res => res.data)
}

export const setpwd = params => {
  return axios.post(`${base}/setpwd`, params)
}