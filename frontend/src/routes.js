const NotFound = () => import('./views/common/404.vue')
const Login = () => import('./views/common/Login.vue')
const forgetPassword = () => import('./views/common/forgetPassword.vue')
const Dashboard = () => import('./views/dashboard/dashboard.vue')
const Home = () => import('./views/Home.vue')

const CampaignListPage = () => import('./views/marketing-registry/CampaignListPage.vue')
const CampaignAbCasePage = () => import('./views/marketing-registry/CampaignAbCasePage.vue')

let routes = [
  {
    path: '/login',
    component: Login,
    name: '',
    hidden: true,
    projectHidden: true
  },
  {
    path: '/forgetPassword',
    component: forgetPassword,
    name: '',
    hidden: true,
    projectHidden: true
  },
  {
    path: '/404',
    component: NotFound,
    name: '',
    hidden: true,
    projectHidden: true
  },
    {
    path: '/',
    component: Home,
    name: '',
    iconCls: 'el-icon-data-line',
    projectHidden: true,
    leaf: true,
    children: [
        { path: '/dashboard', component: Dashboard, iconCls: 'fa fa-database', name: '基础看板' 
        }
    ]
    },
    {
    path: '/',
    component: Home,
    name: '',
    iconCls: 'fa fa-cart-plus',
    projectHidden: true,
    leaf: true,
    children: [
        { path: '/campaigns', 
         component: CampaignListPage, 
         iconCls: 'fa fa-cart-plus',
         name: '营销集市' 
        },
        { path: '/campaigns/campaign=:campaign_id', 
         component: CampaignAbCasePage, 
         name: '活动管理' 
        },
    ]
  }
]

export default routes
