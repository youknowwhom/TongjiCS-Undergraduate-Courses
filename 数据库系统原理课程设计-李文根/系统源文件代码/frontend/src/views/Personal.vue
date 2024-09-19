<script>
import serviceAxios from '@/axios/axios'
import { ElMessage } from 'element-plus'
import { provinceAndCityData } from 'element-china-area-data'
import axios from 'axios'

export default{
  data(){
    return{
        provinceAndCityData,
        username: '',
        birthday: '',
        gender: '',
        phone: '',
        district: '',
        form:{
            username: '',
            birthday: '',
            gender: '',
            phone: '',
            district: '',
        },
        dialogFormVisible: false,
        subscribedTyphoons:[]
    }
  },
  methods:{
    getDistrictArray(str) {
        let result = [];
        for (let i = 0; i < str.length; i += 2) {
            let prefix = str.substring(0, i + 2);
            let expanded = prefix.padEnd(6, '0');
            result.push(expanded);
        }
        return result;
    },
    getInfo(){
        serviceAxios.get(`/getPersonalInfo`)
        .then(response => {
          let data = response.data
          console.log(data)
          this.username = data.name
          this.birthday = new Date(data.birthday).toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'})
          this.gender = data.gender_literal
          this.phone = data.phone
          this.district = data.district

          this.form.name = data.name
          this.form.birthday = new Date(data.birthday).toISOString()
          this.form.gender = data.gender
          this.form.phone = data.phone
          this.form.district = this.getDistrictArray(data.district_id)
          console.log(this.form.district)
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    modify(){
        let district = this.form.district[this.form.district.length-1].substring(0, this.form.district.length*2)
        serviceAxios.post('/updatePersonalInfo',{
          name: this.form.name,
          password: this.form.password,
          gender: this.form.gender,
          birthday: this.form.birthday,
          phone: this.form.phone,
          district: district
        }).then(response => {
          this.getInfo()
          this.dialogFormVisible = false
          ElMessage({
          message: `用户信息更新成功`,
          type: 'success',
          })
        })
        .catch(error => {
          ElMessage({'message': error.response.data.error, 'type': 'error'})
        });
    },
    getTyphoons(){
      serviceAxios.get('/getAllTyphoonFav')
        .then(res=>{
          this.subscribedTyphoons = res.data
          console.log(this.subscribedTyphoons)
        })
    },
    unsetFav(typhoon_id){
      serviceAxios.get(`/unsetTyphoonFav/${typhoon_id}`)
      .then(response => {
        this.getTyphoons()
      })
    },
    checkPath(typhoon_id){
      this.$router.push({path: `/visualize/${typhoon_id}`})
    }
  },
  created(){
    this.getInfo();
    this.getTyphoons();
  }
}
</script>

<template>
  <el-container id="page">
    <el-header height="9%">
        <router-link to="/visualize/1">
        <el-container class="logo-container">
            <img class="logo" src="@/assets/logo.png">
            <el-container class="title-container">
            <h3>台风监测平台</h3>
            <p>made by 郑博远</p>
            </el-container>
        </el-container>
        </router-link>
    </el-header>



    <el-container class="main">
      <el-container class="main-card">
        <el-avatar :size="80">市民用户</el-avatar>

        <el-dialog v-model="dialogFormVisible" title="个人信息修改" width="800">
            <el-form-item label="用户名">
            <el-input v-model="form.name" placeholder="请输入您的用户名"/>
            </el-form-item>
            <el-form-item label="性别">
            <el-radio-group v-model="form.gender" class="ml-4">
                <el-radio value="M" size="large">男</el-radio>
                <el-radio value="F" size="large">女</el-radio>
            </el-radio-group>
            </el-form-item>
            <el-form-item label="生日">
            <el-date-picker class="date-picker"
                v-model="form.birthday" type="date"
                placeholder="请选择您的生日"
            />
            </el-form-item>
            <el-form-item label="电话">
            <el-input v-model="form.phone" placeholder="请输入您的电话"/>
            </el-form-item>
            <el-form-item label="城区">
            <el-cascader
                size="large"
                :options="provinceAndCityData"
                v-model="form.district"
                placeholder="请选择您所在的城区" 
                collapse-tags/>
            </el-form-item>
            <el-container class="form-footer">
                <el-button type="primary" @click="modify">
                    确认修改
                </el-button>
            </el-container>
        </el-dialog>

        <el-descriptions
            class="margin-top"
            title="个人信息"
            :column="1"
            size="large"
            :contentStyle="contentStyle"
            border
        >
            <template #extra>
                <el-button type="primary" @click="dialogFormVisible = true">编辑</el-button>
            </template>
            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                    <el-icon :style="iconStyle"><user /></el-icon>
                    用户名
                    </div>
                </template>
                {{username}}
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                    <el-icon :style="iconStyle">
                        <Male />
                    </el-icon>
                    性别
                    </div>
                </template>
                {{gender}}
            </el-descriptions-item>

            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                    <el-icon :style="iconStyle">
                        <calendar />
                    </el-icon>
                    生日
                    </div>
                </template>
                {{birthday}}
            </el-descriptions-item>

            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                    <el-icon :style="iconStyle">
                        <location />
                    </el-icon>
                    城区
                    </div>
                </template>
                {{ district }}
            </el-descriptions-item>

            <el-descriptions-item>
            <template #label>
                <div class="cell-item">
                <el-icon :style="iconStyle">
                    <phone />
                </el-icon>
                电话
                </div>
            </template>
            {{ phone }}
            </el-descriptions-item>
        </el-descriptions>
      </el-container>

      <el-container class="main-card">
        <h1>订阅台风列表</h1>
        <el-table :data="subscribedTyphoons" max-height="580px" style="width: 100%">
          <el-table-column prop="name" label="台风名称"/>
          <el-table-column sortable prop="max_category" label="最大等级" width="120"/>
          <el-table-column sortable prop="start_time" label="开始时间"/>
          <el-table-column sortable prop="end_time" label="结束时间"/>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button link type="primary" size="small" @click="checkPath(scope.row.id)">
                查看路径
              </el-button>
              <el-button link type="primary" size="small" @click="unsetFav(scope.row.id)">
                取消订阅
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-container>

    </el-container>

  </el-container>
</template>


<style>

.el-descriptions {
    width: 70%;
}

.el-dialog {
    border-radius: 15px;
    padding: 40px;
}

.form-footer{
    display: flex;
    flex-direction: row;
    justify-content: end;
}

body{
  margin: 0;
}

#app {
  font-family: 'HarmonyOS Sans SC';
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>

<style scoped>

.main{
    height: 91%;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center; 
    align-items: center
}

.main-card{
    flex-direction: column;
    justify-content: start; 
    align-items: center;
    width: 50%;
    flex-grow: 0;
    padding: 80px;
}

.main-card:nth-child(2){
  align-items: start;
}

.main-card:nth-child(1){
  background-color: rgb(241, 241, 241);
}

#page{
  position: absolute;
  height: 100%;
  width: 100%;
  margin: 0;
}

a{
    text-decoration: none;
    color: black;
}

.el-container{
  height: 100%;
  width: 100%;
  margin: 0;
}

.el-main{
  padding: 0;
}

.el-header{
  background-color: white;
  border-bottom: solid rgb(215, 215, 215) 1px;
}

.logo{
  width: 65px;
  margin-right: 5px;
}

.logo-container{
  flex-grow: 0;
  display: flex;
  height: 100%;
  justify-content: space-between; 
  align-items: center; 
}

.title-container{
  display: flex;
  height: 100%;
  flex-direction: column;
  justify-content: center; 
  align-items: start; 
}

h3{
  font-size: 18px;
  font-weight: 700;
  margin: 0;
}

p{
  font-size: 12px;
  color: gray;
  margin: 0;
}

</style>