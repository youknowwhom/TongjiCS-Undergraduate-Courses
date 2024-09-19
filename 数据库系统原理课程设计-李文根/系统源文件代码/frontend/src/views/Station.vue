<script>
import serviceAxios from '@/axios/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { provinceAndCityData } from 'element-china-area-data'
import axios from 'axios'

export default{
  data(){
    return{
        provinceAndCityData,
        username: null,
        longitude: null,
        latitude: null,
        district: [],
        form:{
          username: null,
          longitude: null,
          latitude: null,
          district: null,
        },
        createTyphoonForm:{
          name: '',
          longitude: null,
          latitude: null,
          category: null,
          time: null,
          pressure: null,
          windspeed: null
        },
        satelliteForm:{
          name: null,
          longitude: null,
          latitude: null,
          category: null,
          time: null
        },
        alertForm:{
          time: null,
          level: null
        },
        selectTyphoonID: null,
        selectSatelliteID: null,
        options: [],  // 搜索的台风
        satelliteOptions: [],
        menu: 1,
        dialogFormVisible: false,
        props : { multiple: true },
        colors : [
          { value: '#E63415', label: '红色' },
          { value: '#FF6600', label: '橙色' },
          { value: '#FFDE0A', label: '黄色' },
          { value: '#4167F0', label: '蓝色' },
        ],
        satelliteType : [
          { value: 0, label: '极轨气象卫星' },
          { value: 1, label: '同步气象卫星' },
        ],
        satellites: []
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
        serviceAxios.get(`/getStationInfo`)
        .then(response => {
          let data = response.data
          this.longitude = `${data.longitude}°E`
          this.latitude = `${data.latitude}°N`
          this.username = data.name

          this.form.name = data.name
          this.form.longitude = data.longitude
          this.form.latitude = data.latitude
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    modify(){
      let district = []
        for(let d of this.form.district){
          district.push(d[d.length-1].substring(0, d.length*2))
        }

      serviceAxios.post('/updateStationInfo',{
        name: this.form.name,
        longitude: this.form.longitude,
        latitude: this.form.latitude,
      }).then(response => {
        this.getInfo()
        serviceAxios.post('/updateStationDistricts',{
          districts: district
        }).then(response => {
          this.getDistricts()
          this.dialogFormVisible = false
          ElMessage({
          message: `气象站信息更新成功`,
          type: 'success',
          })
        }).catch(error => {
        ElMessage({'message': error.response.data.error, 'type': 'error'})
      });
      })
      .catch(error => {
        ElMessage({'message': error.response.data.error, 'type': 'error'})
      });
    },
    getDistricts(){
      serviceAxios.get('/getStationDistricts')
        .then(res=>{
          this.district = res.data.districts
          this.form.district = res.data.districts_id
        })
    },
    selectMenu(menu, menuPath){
      this.menu = menu
      this.selectTyphoonID = null
      this.alertForm.level = null
      this.satelliteForm.category = null
    },
    createTyphoon(){
      serviceAxios.post('/createTyphoon',{
          name: this.createTyphoonForm.name,
          longitude: this.createTyphoonForm.longitude,
          latitude: this.createTyphoonForm.latitude,
          wind_speed: this.createTyphoonForm.windspeed,
          pressure: this.createTyphoonForm.pressure,
          category: this.createTyphoonForm.category,
          time: this.createTyphoonForm.time
        })
        .then(res=>{
          ElMessage({
            message: `台风${this.createTyphoonForm.name}创建成功`,
            type: 'success',
          })
        })
        .catch(error=>{
          ElMessage({
            message: error.response.data.error,
            type: 'error',
          })
        })
    },
    createSatellite(){
      serviceAxios.post('/createSatellite',{
          name: this.satelliteForm.name,
          category: this.satelliteForm.category,
          time: this.satelliteForm.time,
          longitude: this.satelliteForm.longitude,
          latitude: this.satelliteForm.latitude
        })
        .then(res=>{
          ElMessage({
            message: `卫星创建成功`,
            type: 'success',
          })
        })
        .catch(error=>{
          ElMessage({
            message: error.response.data.error,
            type: 'error',
          })
        })
    },
    createTyphoonPath(){
      if(!this.selectTyphoonID){
        ElMessage({
            message: '未选择待更新台风！',
            type: 'error',
          })
        return;
      }
      serviceAxios.post(`/createTyphoonPath/${this.selectTyphoonID}`,{
          longitude: this.createTyphoonForm.longitude,
          latitude: this.createTyphoonForm.latitude,
          wind_speed: this.createTyphoonForm.windspeed,
          pressure: this.createTyphoonForm.pressure,
          category: this.createTyphoonForm.category,
          time: this.createTyphoonForm.time
        })
        .then(res=>{
          ElMessage({
            message: `台风路径更新成功`,
            type: 'success',
          })
        })
        .catch(error=>{
          ElMessage({
            message: error.response.data.error,
            type: 'error',
          })
        })
    },
    endTyphoon(){
      if(!this.selectTyphoonID){
        ElMessage({
            message: '未选择待消亡台风！',
            type: 'error',
          })
        return;
      }
      serviceAxios.post(`/endTyphoon/${this.selectTyphoonID}`,{})
        .then(res=>{
          ElMessage({
            message: `台风消亡成功`,
            type: 'success',
          })
        })
        .catch(error=>{
          ElMessage({
            message: error.response.data.error,
            type: 'error',
          })
        })
    },
    createAlert(){
      if(!this.selectTyphoonID){
        ElMessage({
            message: '未选择待发布预警的台风！',
            type: 'error',
          })
        return;
      }
      serviceAxios.post('/createAlert',{
        typhoon_id : this.selectTyphoonID,
        level: this.alertForm.level,
        time: this.alertForm.time
      })
        .then(res=>{
          ElMessage({
            message: `台风预警发布成功`,
            type: 'success',
          })
        })
        .catch(error=>{
          ElMessage({
            message: error.response.data.error,
            type: 'error',
          })
        })
    },
    searchByStr(str){
      if(str==''){
        this.options=[]
        return;
      }
      serviceAxios.get(`/searchNotEndedTyphoonByStr/${str}`)
        .then(response => {
          let data = response.data;
          let options = [];
          data['typhoon'].forEach(function(item) {
            let time = new Date(item.start_time)
            options.push({
              value: item.id,
              label: item.name.toUpperCase()+' '+String(time.getFullYear())})
          });
          this.options = options
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          this.options=[]
        });
    },
    searchSatelliteByStr(str){
      if(str==''){
        this.options=[]
        return;
      }
      serviceAxios.get(`/searchSatelliteByStr/${str}`)
        .then(response => {
          let data = response.data;
          let options = [];
          data['satellite'].forEach(function(item) {
            options.push({
              value: item.id,
              label: item.name.toUpperCase()})
          });
          this.satelliteOptions = options
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          this.satelliteOptions=[]
        });
    },
    subscribeSatellite(){
      if (!this.selectSatelliteID){
        ElMessage({
            message: '未选择卫星！',
            type: 'error',
          })
        return;
      }
      serviceAxios.post(`/createSatelliteConnect/${this.selectSatelliteID}`, {})
        .then(response => {
          ElMessage({
            message: `订阅成功`,
            type: 'success',
          })
          this.getSatelliteConnect()
          this.selectSatelliteID = null
        })
        .catch(error=>{
          ElMessage({
            message: error.response.data.error,
            type: 'error',
          })
          this.selectSatelliteID = null
        })
    },
    getSatelliteConnect(){
      serviceAxios.get(`/getSatelliteConnect`)
        .then(response => {
          let data = response.data;
          this.satellites = data
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          this.satelliteConnectOptions=[]
        });
    },
    unconnect(index){
      ElMessageBox.confirm('确认取消订阅该卫星吗？')
      .then(() => {
        serviceAxios.post(`/cancelSatelliteConnect/${this.satellites[index].id}`, {})
          .then(response => {
            ElMessage({
              message: `取消订阅成功`,
              type: 'success',
            })
            this.satellites = this.satellites.filter((element, i) => i !== index);
          })
          .catch(error=>{
            ElMessage({
              message: error.response.data.error,
              type: 'error',
            })
          })
      })
      .catch(() => {
      })
    }
  },
  created(){
    this.getInfo();
    this.getDistricts();
    this.getSatelliteConnect();
  }
}
</script>

<template>
  <el-container id="page">
    <el-header height="9%">
      <el-container class="logo-container">
          <img class="logo" src="@/assets/logo.png">
          <el-container class="title-container">
          <h3>台风监测平台</h3>
          <p>made by 郑博远</p>
          </el-container>
      </el-container>
    </el-header>

    <el-container style="height:91%;">
      <el-aside width="400px">
        <el-menu
          default-active="1"
          @select="selectMenu"
        >
          <el-menu-item index="1">
            <el-icon><edit /></el-icon>
            <span>气象站基本信息</span>
          </el-menu-item>

          <el-sub-menu index="2">
            <template #title>
              <el-icon><promotion /></el-icon>
              <span>路径信息更新</span>
            </template>
            <el-menu-item index="2-1">台风发布</el-menu-item>
            <el-menu-item index="2-2">路径更新</el-menu-item>
            <el-menu-item index="2-3">台风消亡</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="3">
            <el-icon><warnTriangleFilled /></el-icon>
            <span>预警信息发布</span>
          </el-menu-item>

          <el-sub-menu index="4">
            <template #title>
              <el-icon><place /></el-icon>
              <span>卫星信息查询</span>
            </template>
            <el-menu-item index="4-1">创建卫星</el-menu-item>
            <el-menu-item index="4-2">查看卫星</el-menu-item>
          </el-sub-menu>   

        </el-menu>
      </el-aside>

      <el-container v-if="menu=='1'" class="main">
        <el-avatar :size="80" style="flex-shrink: 0;">气象站用户</el-avatar>

        <el-dialog v-model="dialogFormVisible" title="气象站信息修改" width="800">
            <el-form-item label="气象站名">
            <el-input v-model="form.name" placeholder="请输入您的用户名"/>
            </el-form-item>
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
            <el-form-item label="城区">
            <el-cascader
                size="large"
                :options="provinceAndCityData"
                v-model="form.district"
                placeholder="请选择您所监测的城区"
                :props="props"
                collapse-tags/>
            </el-form-item>
            <el-container class="form-footer">
                <el-button type="primary" @click="modify">
                    确认修改
                </el-button>
            </el-container>
        </el-dialog>

        <el-descriptions
            style="flex-shrink: 0;"
            title="气象站信息"
            :column="1"
            size="large"
            border
        >
            <template #extra>
                <el-button type="primary" @click="dialogFormVisible = true">编辑</el-button>
            </template>
            <el-descriptions-item :column>
                <template #label>
                    <div class="cell-item">
                    <el-icon :style="iconStyle"><user /></el-icon>
                    气象站名
                    </div>
                </template>
                {{username}}
            </el-descriptions-item>

            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                    <el-icon :style="iconStyle">
                        <AddLocation />
                    </el-icon>
                    经度
                    </div>
                </template>
                {{longitude}}
            </el-descriptions-item>

            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                    <el-icon :style="iconStyle">
                        <DeleteLocation />
                    </el-icon>
                    纬度
                    </div>
                </template>
                {{latitude}}
            </el-descriptions-item>
        </el-descriptions>

        <el-container class="district-container">
          <h1>监测城区</h1>
        </el-container>
        <el-table :data="district" style="flex-shrink: 0; margin-top: -25px; height: 300px; width: 70%">
            <el-table-column prop="name" label="城区" />
          </el-table>
      </el-container>


      <el-container v-if="menu=='2-1'" class="main">
        <el-container class="inner-container">
          <h1>发布台风</h1>
          <el-form :model="createTyphoonForm" label-width="auto" style="width:100%;" label-position="top" size="large">
            <el-form-item label="台风名称">
              <el-input v-model="createTyphoonForm.name" />
            </el-form-item>
            <el-container class="position-input">
              <el-form-item label="生成时间">
                <el-date-picker
                  v-model="createTyphoonForm.time"
                  type="datetime"
                  placeholder="选择台风生成时间"
                />
              </el-form-item>
              <el-form-item label="当前经度">
                <el-input-number 
                v-model="createTyphoonForm.longitude" placeholder="东经（E）"
                :min="0" :max="180" :precision="2"/>
              </el-form-item>
              <el-form-item label="当前纬度">
                <el-input-number 
                v-model="createTyphoonForm.latitude" placeholder="北纬（N）"
                :min="0" :max="90" :precision="2"/>
              </el-form-item>
            </el-container>
            <el-container class="position-input">
              <el-form-item label="当前级别">
                <el-input-number 
                v-model="createTyphoonForm.category" placeholder="0~6级"
                :min="0" :max="6"/>
              </el-form-item>
              <el-form-item label="当前气压">
                <el-input-number 
                v-model="createTyphoonForm.pressure" placeholder="hPa"
                :min="0" :max="2000" :precision="2"/>
              </el-form-item>
              <el-form-item label="当前风速">
                <el-input-number 
                v-model="createTyphoonForm.windspeed" placeholder="m/s"
                :min="0" :max="100" :precision="2"/>
              </el-form-item>
            </el-container>
          </el-form>
          <el-container style="width: 100%; display: flex; justify-content: end;">
            <el-button size="large" type="primary" @click="createTyphoon">发布台风</el-button>
          </el-container>
        </el-container>
      </el-container>

      <el-container v-if="menu=='2-2'" class="main">
        <el-container class="inner-container">
          <h1>选择台风</h1>
          <el-select
            placeholder="搜索当前还未消亡的台风"
            v-model="selectTyphoonID"
            size="large"
            remote filterable
            :remote-method="searchByStr"
            reserve-keyword
          >
            <template #prefix>
              <el-icon class="el-input__icon" style="margin-right: 5px;"><search /></el-icon>
            </template>
            <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>

          <h1>路径信息</h1>
          <el-form :model="createTyphoonForm" label-width="auto" style="width:100%;" label-position="top" size="large">
            <el-container class="position-input">
              <el-form-item label="当前时间">
                <el-date-picker
                  v-model="createTyphoonForm.time"
                  type="datetime"
                  placeholder="选择路径监测时间"
                />
              </el-form-item>
              <el-form-item label="当前经度">
                <el-input-number 
                v-model="createTyphoonForm.longitude" placeholder="东经（E）"
                :min="0" :max="180" :precision="2"/>
              </el-form-item>
              <el-form-item label="当前纬度">
                <el-input-number 
                v-model="createTyphoonForm.latitude" placeholder="北纬（N）"
                :min="0" :max="90" :precision="2"/>
              </el-form-item>
            </el-container>
            <el-container class="position-input">
              <el-form-item label="当前级别">
                <el-input-number 
                v-model="createTyphoonForm.category" placeholder="0~6级"
                :min="0" :max="6"/>
              </el-form-item>
              <el-form-item label="当前气压">
                <el-input-number 
                v-model="createTyphoonForm.pressure" placeholder="hPa"
                :min="0" :max="2000" :precision="2"/>
              </el-form-item>
              <el-form-item label="当前风速">
                <el-input-number 
                v-model="createTyphoonForm.windspeed" placeholder="m/s"
                :min="0" :max="100" :precision="2"/>
              </el-form-item>
            </el-container>
          </el-form>
          <el-container style="width: 100%; display: flex; justify-content: end;">
            <el-button size="large" type="primary" @click="createTyphoonPath">更新路径</el-button>
          </el-container>
        </el-container>
      </el-container>


      <el-container v-if="menu=='2-3'" class="main">
        <el-container class="inner-container">
          <h1>选择台风</h1>
          <el-select
            placeholder="搜索当前还未消亡的台风"
            v-model="selectTyphoonID"
            size="large"
            remote filterable
            :remote-method="searchByStr"
            reserve-keyword
          >
            <template #prefix>
              <el-icon class="el-input__icon" style="margin-right: 5px;"><search /></el-icon>
            </template>
            <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
          <el-container style="width: 100%; display: flex; justify-content: end; margin-top: 20px;">
            <el-button size="large" type="primary" @click="endTyphoon">消亡台风</el-button>
          </el-container>
        </el-container>
      </el-container>

      <el-container v-if="menu=='3'" class="main">
        <el-container class="inner-container">
          <h1>选择台风</h1>
          <el-select
            placeholder="搜索当前还未消亡的台风"
            v-model="selectTyphoonID"
            size="large"
            remote filterable
            :remote-method="searchByStr"
            reserve-keyword
          >
            <template #prefix>
              <el-icon class="el-input__icon" style="margin-right: 5px;"><search /></el-icon>
            </template>
            <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>

          <h1>预警信息</h1>
          
          <el-form :model="alertForm" label-width="auto" style="width:100%;" size="large">
            <el-form-item label="预警时间">
              <el-date-picker
                v-model="alertForm.time"
                type="datetime"
                placeholder="选择路径监测时间"
              />
            </el-form-item>
            
            <el-form-item label="预警等级">
              <el-select v-model="alertForm.level" placeholder="选择预警等级" style="width: 240px">
                <el-option
                  v-for="item in colors"
                  :key="item.value"
                  :label="item.label"
                  :value="item.label"
                >
                  <div>
                    <el-tag :color="item.value" style="width: 20px; margin-right: 8px" size="small" />
                    <span :style="{ color: item.value }">{{ item.label }}</span>
                  </div>
                </el-option>
                <template #tag>
                  <el-tag v-for="color in value" :key="color" :color="color" />
                </template>
              </el-select>
            </el-form-item>
          </el-form>

          <el-container style="width: 100%; display: flex; justify-content: end; margin-top: 20px;">
            <el-button size="large" type="primary" @click="createAlert">发布预警</el-button>
          </el-container>
        </el-container>
      </el-container>


      <el-container v-if="menu=='4-1'" class="main">
        <el-container class="inner-container">
          <h1>创建卫星</h1>
          <el-form :model="satelliteForm" label-width="auto" style="width:100%;" label-position="top" size="large">
            <el-form-item label="卫星名称">
              <el-input v-model="satelliteForm.name" />
            </el-form-item>
            <el-container class="position-input">
              <el-form-item label="发射时间">
                <el-date-picker
                  v-model="satelliteForm.time"
                  type="datetime"
                  placeholder="选择卫星发射时间"
                />
              </el-form-item>
              <el-form-item label="当前经度">
                <el-input-number 
                v-model="satelliteForm.longitude" placeholder="东经（E）"
                :min="0" :max="180" :precision="2"/>
              </el-form-item>
              <el-form-item label="当前纬度">
                <el-input-number 
                v-model="satelliteForm.latitude" placeholder="北纬（N）"
                :min="0" :max="90" :precision="2"/>
              </el-form-item>
            </el-container>

            <el-form-item label="卫星类型">
              <el-select v-model="satelliteForm.category" placeholder="选择卫星类型" style="width: 240px">
                <el-option
                  v-for="item in satelliteType"
                  :key="item.value"
                  :label="item.label"
                  :value="item.label"
                >
                </el-option>
              </el-select>
            </el-form-item>

          </el-form>
          <el-container style="width: 100%; display: flex; justify-content: end;">
            <el-button size="large" type="primary" @click="createSatellite">创建卫星</el-button>
          </el-container>
        </el-container>
      </el-container>


      <el-container v-if="menu=='4-2'" class="main">
        <el-container class="inner-container">
          <h1>卫星订阅</h1>
          <el-select
            placeholder="搜索卫星"
            v-model="selectSatelliteID"
            size="large"
            remote filterable
            :remote-method="searchSatelliteByStr"
            reserve-keyword
          >
            <template #prefix>
              <el-icon class="el-input__icon" style="margin-right: 5px;"><search /></el-icon>
            </template>
            <el-option
                v-for="item in satelliteOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>

          <el-container style="width: 100%; display: flex; justify-content: end; flex-grow: 0; margin-top:20px;">
            <el-button size="large" type="primary" @click="subscribeSatellite">订阅卫星</el-button>
          </el-container>

          <h1>卫星查询</h1>
          <el-container class="card-container">
            <el-card shadow="hover" v-for="(satellite, index) in satellites" style="width: 300px; height: 160px; margin-right: 10px; margin-bottom: 10px;">
              <template #header>
                <div class="card-header">
                  <span>{{ satellite.name }}</span>
                  <el-icon style="opacity: 0.8; cursor:pointer;" @click="unconnect(index)"><CircleCloseFilled /></el-icon>
                </div>
              </template>
              <p>{{ satellite.type }}</p>
              <p>发射时间：{{ satellite.launch_date }}</p>
              <p>东经{{ satellite.current_longtitude }}°E 北纬{{ satellite.current_latitude }}°N</p>
            </el-card>
          </el-container>
        </el-container>
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

.el-aside{
  background-color: white;
  border-right: solid rgb(215, 215, 215) 1px;
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
  height: 100%;
  width: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;;
  justify-content: start; 
  align-items: center;
  padding: 80px;
  background-color: rgb(241, 241, 241);
}

.card-header{
  display: flex;
  justify-content: space-between;
}

.district-container{
  height: 100px;
  margin-top: 20px;
  flex-grow: 0;
  flex-shrink: 0;
  width: 70%;
  display: flex;
  flex-direction: column;
  justify-content: start; 
  align-items: start;
}

.inner-container{
  height: 100%;
  width: 100%;
  margin-top: -40px;
  flex-grow: 0;
  flex-shrink: 0;
  width: 70%;
  display: flex;
  flex-direction: column;
  justify-content: start; 
  align-items: start;
}

.card-container{
  width: 100%;
  overflow-y: scroll;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.el-form-item{
  margin-bottom: 20px;
}

.el-main{
  padding: 0;
}

.el-header{
  background-color: white;
  border-bottom: solid rgb(215, 215, 215) 1px;
}

.el-form-item{
  margin-bottom: 20px;
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

h1{
  font-size: 16px;
  color:#303133;
  height: 16px;
}

.position-input{
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%
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