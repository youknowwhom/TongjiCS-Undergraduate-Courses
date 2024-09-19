<script>
import serviceAxios from '@/axios/axios'
import { ElMessage } from 'element-plus'
import { provinceAndCityData } from 'element-china-area-data'
import axios from 'axios'

export default{
  data(){
    return{
        messages: []
    }
  },
  methods:{
    getMessage(){
        serviceAxios.get('getMessage')
            .then(res=>{
                this.messages = res.data
            })
    },
    collapseChange(i){
        let index = parseInt(i)
        if(!this.messages[index].checked){
            serviceAxios.get(`/setMessageRead/${this.messages[index].id}`)
                .then(res=>{
                    this.messages[index].checked = true
                })
        }
    }
  },
  created(){
    this.getMessage();
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
            <el-container class="h1-container">
                <h1>台风路径信息</h1>
            </el-container>
            <el-scrollbar style="width:100%;">
                <el-empty v-if="messages.length == 0" description="暂无信息" />
                <el-collapse style="width:100%" accordion @change="collapseChange">
                    <div v-for="(message, index) in messages" >
                        <el-collapse-item :name="index">
                            <template #title>
                                <el-badge is-dot :hidden="message.checked" :offset="[15, 24]">
                                    {{ '台风 ' + message.typhoon + ' 路径信息更新（' + message.time + '）'}}
                                </el-badge>
                            </template>
                            <div>
                            {{message.station}}
                            </div>
                            <div>
                            台风位置:东经{{message.longitude}}°，北纬{{message.latitude}}°
                            </div>
                            <div>
                            台风等级:{{ message.category }} &nbsp&nbsp 风速:{{ message.wind_speed }}m/s &nbsp&nbsp 中心气压:{{ message.pressure }}hPa
                            </div>
                        </el-collapse-item>
                    </div>
                </el-collapse>
            </el-scrollbar>
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

#page{
  position: absolute;
  height: 100%;
  width: 100%;
  margin: 0;
}

.main{
    height: 91%;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center; 
    align-items: center;
    background-color: rgb(241, 241, 241);
}

.main-card{
    flex-direction: column;
    justify-content: start; 
    align-items: center;
    width: 80%;
    height: 100%;
    flex-grow: 0;
    background-color: white;
    padding: 80px;
}

/deep/ .el-collapse-item__header{
  font-size: 16px;
  font-weight: 700;
  color: rgb(51, 53, 61);
}

/deep/ .el-collapse-item__content{
  font-size: 15px;
  color: rgb(102, 102, 102);
}

a{
    text-decoration: none;
    color: black;
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

h1{
    font-size: 20px;
}

.h1-container{
  flex-grow: 0;
  margin-top: -30px;
  width: 100%;
  display: flex;
  justify-content: start;
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