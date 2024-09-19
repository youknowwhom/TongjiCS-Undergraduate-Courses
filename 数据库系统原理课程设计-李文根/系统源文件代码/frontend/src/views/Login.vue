<script>
import serviceAxios from '@/axios/axios';
import { ElMessage } from 'element-plus'

export default{
  data(){
    return{
      form:{
        name: '',
        password: '',
        type:'regular'
      }
    }
  },
  methods:{
    submit(){
      console.log(this.form)
      if(this.form.type==='regular'){
        serviceAxios.post('/login/regular',{
          name: this.form.name,
          password: this.form.password,
        }).then(response => {
          console.log('store', response.data.token)
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('role', 'regular')
          ElMessage({'message': '登录成功！', 'type': 'success'})
          this.$router.push({path: '/visualize/1'});
        })
        .catch(response => {
          ElMessage({'message': response.response.data.error, 'type': 'error'})
        });
      }
      else{
        serviceAxios.post('/login/station',{
          name: this.form.name,
          password: this.form.password,
        }).then(response => {
          console.log('store', response.data.token)
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('role', 'station')
          ElMessage({'message': '登录成功！', 'type': 'success'})
          this.$router.push({path: '/station'});
        })
        .catch(response => {
          ElMessage({'message': response.response.data.error, 'type': 'error'})
        });
      }
    }
  }
}
</script>

<template>
<el-container class="background">
  <img src="@/assets/background.jpg" />
</el-container>
<el-container class="front">
  <el-container class="login_container">
    <el-container class="title">
      <img src="@/assets/logo.png" class="logo-pic">
      <h1>台风监测预警平台</h1>
    </el-container>
    <el-form :model="form">
      <el-form-item label="身份">
        <el-radio-group v-model="form.type" size="large">
          <el-radio-button label="市民用户" value="regular" />
          <el-radio-button label="气象站用户" value="station" />
        </el-radio-group>
      </el-form-item>
      <el-form-item label="账户">
        <el-input v-model="form.name" placeholder="请输入您的用户名"/>
      </el-form-item>
      <el-form-item label="密码">
        <el-input show-password v-model="form.password" placeholder="请输入您的密码"/>
      </el-form-item>
      <router-link to="/signup" class="signup-prompt">
        <p>没有账号？点击注册</p>
      </router-link>
      <el-form-item>
        <el-button type="primary" class="button" @click="submit">登 录</el-button>
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

/deep/.el-form-item__content{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.signup-prompt{
  width: 75%;
  margin: 0;
  display: flex;
  flex-direction: row;
  justify-content: end;
  align-items: center;
}

.signup-prompt p{
  margin: 0;
  font-size: 12px;
  text-decoration: underline;
  color: #409EFF;
}

.el-input{
  height: 45px;
  font-size: 15px;
}

.title{
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  flex-grow: 0;
}

.title h1{
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

.logo-pic{
  width: 50px;
  height: 50px;
}

.login_container{
  background-color: white;
  width: 510px;
  height: 450px;
  border-radius: 22px;
  flex-grow: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
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