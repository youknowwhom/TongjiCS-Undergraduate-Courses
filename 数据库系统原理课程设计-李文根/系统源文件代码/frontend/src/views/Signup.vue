<script>
import serviceAxios from '@/axios/axios';
import { provinceAndCityData } from 'element-china-area-data'
import { ElMessage } from 'element-plus'

export default{
  data(){
    return{
      provinceAndCityData,
      props : { multiple: true },
      form:{
        name: '',
        gender: '',
        password: '',
        birthday: '',
        type:'regular',
        phone:'',
        district:''
      }
    }
  },
  methods:{
    submit(){
      if(this.form.type==='regular'){
        let district = this.form.district[this.form.district.length-1].substring(0, this.form.district.length*2)
        serviceAxios.post('/signup/regular',{
          name: this.form.name,
          password: this.form.password,
          gender: this.form.gender,
          birthday: this.form.birthday,
          phone: this.form.phone,
          district: district
        }).then(response => {
          ElMessage({
          message: `用户${this.form.name}创建成功`,
          type: 'success',
          })
          this.$router.push({path: '/login'});
        })
        .catch(error => {
          ElMessage({'message': error.response.data.error, 'type': 'error'})
        });
      }
      else{
        let district = []
        for(let d of this.form.district){
          district.push(d[d.length-1].substring(0, d.length*2))
        }

        serviceAxios.post('/signup/station',{
          name: this.form.name,
          password: this.form.password,
          longitude: this.form.longitude,
          latitude: this.form.latitude,
          district: district
        }).then(response => {
          ElMessage({
          message: `用户${this.form.name}创建成功`,
          type: 'success',
          })
          this.$router.push({path: '/login'});
        })
        .catch(error => {
          ElMessage({'message': error.response.data.error, 'type': 'error'})
        });
      }
    }
  },
  created(){
    // provinceAndCityData.forEach(function(item) {
    //   if (item.label[item.label.length - 1] === '市') {
    //       item.children = [
    //           { value: item.value+'01', label: '市辖区' }
    //       ];
    //   }
    // });
  }
}
</script>

<template>
<el-container class="background">
  <img src="@/assets/background.jpg" />
</el-container>
<el-container class="front">
  <el-container class="signup_container">
    <el-container class="signup_title">
      <img src="@/assets/logo.png" class="logo">
      <h1>台风监测预警平台注册</h1>
    </el-container>
    <el-form :model="form">
      <el-form-item label="身份">
        <el-radio-group v-model="form.type" size="large">
          <el-radio-button label="市民用户" value="regular" />
          <el-radio-button label="气象站用户" value="station" />
        </el-radio-group>
      </el-form-item>
      <el-scrollbar>
        <el-form-item label="账户">
          <el-input v-model="form.name" placeholder="请输入您的用户名"/>
        </el-form-item>
        <el-form-item label="密码">
          <el-input show-password v-model="form.password" placeholder="请输入您的密码"/>
        </el-form-item>
        <el-form-item label="性别" v-if="form.type=='regular'">
          <el-radio-group v-model="form.gender" class="ml-4">
            <el-radio value="M" size="large">男</el-radio>
            <el-radio value="F" size="large">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="生日" v-if="form.type=='regular'">
          <el-date-picker class="date-picker"
            v-model="form.birthday" type="date"
            placeholder="请选择您的生日"
          />
        </el-form-item>
        <el-form-item label="电话" v-if="form.type=='regular'">
          <el-input v-model="form.phone" placeholder="请输入您的电话"/>
        </el-form-item>
        <el-container v-if="form.type=='station'" class="position-input">
          <el-form-item label="经度">
            <el-input-number 
            v-model="form.longitude" placeholder="东经（E）"
            :min="73" :max="136" :precision="2"/>
          </el-form-item>
          <el-form-item label="纬度">
            <el-input-number 
            v-model="form.latitude" placeholder="北纬（N）"
            :min="3" :max="54" :precision="2"/>
          </el-form-item>
        </el-container>
        <el-form-item label="城区">
          <el-cascader
            size="large"
            :options="provinceAndCityData"
            v-model="form.district"
            :placeholder="form.type==='regular' ? '请选择您所在的城区' : '请选择您所监测的城区'" 
            :props="form.type==='regular' ? {} : props"
            collapse-tags/>
        </el-form-item>
        
      </el-scrollbar>
      <router-link to="/login" class="login-prompt">
        <p>已有账号？点击登录</p>
      </router-link>
      <el-form-item>
        <el-button type="primary" class="button" @click="submit">注 册</el-button>
      </el-form-item>
    </el-form>
  </el-container>
</el-container>
</template>

<style>
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

.el-form{
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-grow: 0;
}

.el-form-item{
  width: 75%;
  margin: 12px 0;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.el-scrollbar .el-form-item{
  width: 100%;
  margin: 0;
  margin-bottom: 20px;
}

/deep/.el-cascader{
  width: 100%;
}

.position-input{
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%
}

.position-input .el-form-item{
  width: 48%;
}

/deep/.date-picker{
  height: 45px !important;
  width: 100% !important;
  font-family: 'HarmonyOS Sans SC';
}

.el-scrollbar{
  height: 200px;
  width: 75%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 0;
  margin: 25px 0;
}

/deep/.el-scrollbar__wrap{
  width: 100%;
}

/deep/.el-scrollbar__view{
  width: 100%;
}

.login-prompt{
  width: 75%;
  margin: 0;
  display: flex;
  flex-direction: row;
  justify-content: end;
  align-items: center;
}

.login-prompt p{
  margin: 0;
  font-size: 12px;
  text-decoration: underline;
  color: #409EFF;
}

.el-input{
  height: 45px;
  font-size: 15px;
}

/deep/.el-form-item__content{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.signup_title{
  width: 100%;
  display: flex;
  margin-top: 40px;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  flex-grow: 0;
}

.signup_title h1{
  font-size: 22px;
  line-height: 22px;
  margin: 0;
  margin-left: 5px;
  font-weight: 500;
}

.button{
  height: 50px;
  width: 100%;
  margin-top: 10px;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
}

.logo{
  width: 50px;
  height: 50px;
}

.signup_container{
  background-color: white;
  width: 550px;
  height: 550px;
  border-radius: 22px;
  flex-grow: 0;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  box-shadow: 0px 0px 20px 5px rgba(0, 65, 105, 0.05);
}

#page{
  height: 100%;
  width: 100%;
}

.background{
  height: 100%;
  width: 100%;
  z-index: -1;
  position: absolute;
}

.background img{
  width: 100%;
}

.front{
  height: 100%;
  width: 100%;
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: -1;
}


</style>