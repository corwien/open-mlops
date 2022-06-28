<template>
    <div class="main-a">
        <div style="margin-top: 20px" align="right">
            <el-radio-group v-model="radio2" size="medium">
                <el-radio-button label="所有" ></el-radio-button>
                <el-radio-button label="近一个月"></el-radio-button>
                <el-radio-button label="近14天"></el-radio-button>
                <el-radio-button label="近7天"></el-radio-button>
                <el-radio-button label="今天"></el-radio-button>
            </el-radio-group>
        </div>

        <el-row :span="24" style="margin-top: 20px" align="right">
            <el-col :span="8" class='inline'>
                <el-card class="box-card"  shadow="always">
                    <!--<div slot="header"></div>-->
                    <div class="circle" align="center">
                        <el-progress type="circle" :percentage="100"></el-progress>
                        <h3>已注册的标签数：50</h3>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="7" class='inline'>
                <el-card class="box-card" shadow="always">
                    <!--<div slot="header"></div>-->
                    <div class="circle" align="center">
                        <el-progress type="circle" :percentage="50"></el-progress>
                        <h3>已完成的活动数：30</h3>
                    </div>
                </el-card>
            </el-col>
             <el-col :span="8" style="margin-right: 0px;margin-top: 10px;">
                <el-card class="box-card" shadow="always">
                    <!--<div slot="header"></div>-->
                    <div class="circle" align="center">
                        <el-progress type="circle" :percentage="75"></el-progress>
                        <h3>正在进行的活动数：18</h3>
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <div  style="margin-top: 40px">
            <h2>快速启动指南</h2>
            <el-collapse v-model="activeNames" @change="handleChange">
                <el-collapse-item title="标签创建" name="1">
                     <div>
                         <pre style="word-break: break-all;overflow:auto;overflow-x:hidden" v-highlightA>
                             <code class="python">test</code>
                         </pre> 
                      </div>
                </el-collapse-item>
                <el-collapse-item title="营销活动管理" name="2">
                     <div class="model-code">
                         <pre style="word-break: break-all;overflow:auto;overflow-x:hidden" v-highlightA>
                             <code class="python">model = algolink.create_model(lr, X[[0]], model_name='lr-model-1')

task = alink.get_or_create_task('Model-deploy', 'Model-task')
task.push_model(model)</code>
                         </pre> 
                      </div>
                </el-collapse-item>
                <el-collapse-item title="标签发布与治理" name="3">
                     <span >
                         <pre style="word-break: break-all;overflow:auto;overflow-x:hidden;margin:0px" v-highlightA>
                             <code class="python">from algolink.ext.flask.server import FlaskServer
image = alink.create_image(model, 'lr-model-image', server=FlaskServer(), builder_args={'force_overwrite': True})
instance = alink.create_instance(image, 'lr-model-instance', port_mapping={9000: 9011}).run(detach=True)
instance.is_running()</code>
                         </pre> 
                      </span>
                </el-collapse-item>
                <!--<el-collapse-item title="A/B 测试与模型监控" name="4">
                    <div>用户决策：根据场景可给予用户操作建议或安全提示，但不能代替用户进行决策；</div>
                    <div>结果可控：用户可以自由的进行操作，包括撤销、回退和终止当前操作等。</div>
                </el-collapse-item>-->
            </el-collapse>
        </div>

  

    </div>
</template>

<script>
import { getProjectDetail } from '@/api/api'
import moment from 'moment'
export default {
  data () {
    return {
        activeNames: ['1'],
        size:'',
      radio2: '所有',
      moment: moment,
      abceseCount: 1,
      type: '',
      version: '',
      updateDate: '',
      apiCount: 0,
      statusCount: 0,
      dynamicCount: 0,
      memberCount: 0,
      createDate: ''
    }
  },
  methods: {
    getProjectInfo () {
      var self = this
      let params = { project_id: this.$route.params.project_id }
      let headers = {
        'Content-Type': 'application/json',
        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
      }
      getProjectDetail(headers, params).then(_data => {
        let { msg, code, data } = _data
        console.log(data.dynamicCount, '_data')
        self.listLoading = false
        if (code === '999999') {
          self.type = data.proj_type
          self.version = data.version
          self.updateDate = data.LastUpdateTime
          self.apiCount = data.apiCount
          self.dynamicCount = data.dynamicCount
          self.memberCount = data.memberCount
          self.createDate = data.createTime
          self.abceseCount = data.abceseCount
        } else {
          self.$message.error({
            message: msg,
            center: true
          })
        }
      })
    }
  },
  mounted () {
    this.getProjectInfo()
  }
}
</script>

<style lang="scss" scoped>
    //@import url("//unpkg.com/element-ui@2.7.2/lib/theme-chalk/index.css");
    .box-card {
        width: 100%;
        height: 100%;
        display: block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;

    }
    .member {
        width: 7%;
    }
    .main-a {
        margin: 35px;
        margin-top: 10px;
    }
    .inline {
        margin: 10px;
        margin-left: 0px;
        margin-right: 10px;
    }
    .model-code{
    white-space: pre;
    padding: 0 !important;
    margin-top: -1.00em;
    position: relative;
    margin-bottom: 0px;

    display: block;
}
</style>
