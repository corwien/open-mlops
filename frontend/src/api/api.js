import axios from 'axios'

axios.defaults.withCredentials = true // 配置为true
let base = 'http://127.0.0.1:5001'
export const test = 'http://127.0.0.1:5001'
export const delpoySocketIP = `http://0.0.0.0:5001`


export const requestLogin = params => {
    return axios.post(`${base}/login/userLogin`, params).then(res => res.data)
}

export const setpwd = params => {
    return axios.post(`${base}/setpwd`, params)
}

// 获取活动列表
export const getCampaigns = (headers, params) => {
    return axios.get(`${base}/api/campaigns`, 
                     { params: params, headers: headers 
                     }).then(res => res.data)
}
// 添加活动
export const addCampaign = (headers, params) => {
  return axios.post(`${base}/api/campaigns/add_campaign`, 
                    params, 
                    { headers 
                    }).then(res => res.data)
}