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
// 获取实验基础信息
export const getAbExps = (headers, params) => {
    return axios.get(`${base}/api/campaigns/abexps`, 
                     { params: params, headers: headers }).then(res => res.data)
}
// 创建实验
export const addAbExp = (headers, params) => {
  return axios.post(`${base}/api/campaigns/add_ab_exp`, params, 
                    { headers }).then(res => res.data)
}
// 获取ab测试结果
export const getTestResultList = (headers, params) => {
  return axios.get(`${base}/api/abtesting/report/alt_table_report`, { params: params, headers: headers }).then(res => res.data)
}

// 设定实验的获胜者
export const absetWinner = (headers, params) => {
  return axios.post(`${base}/api/abtesting/report/abset_winner`, 
                    params, 
                    { headers }).then(res => res.data)
}
//获取dashboard 信息
export const getDashboardDetail = (headers, params) => {
  return axios.get(`${base}/api/dashboard/get_dashboard_info`, 
                   { params: params, headers: headers }).then(res => res.data)
}

