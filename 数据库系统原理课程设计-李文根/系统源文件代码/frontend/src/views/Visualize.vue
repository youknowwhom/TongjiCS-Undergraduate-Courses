<script>
import serviceAxios from '@/axios/axios';
import * as echarts from 'echarts';
import {h} from 'vue';
import { ElMessageBox } from 'element-plus';

export default{
  data(){
    return{
      chosenTyphoonID: 1,
      selectTyphoonID: null,
      options:[],
      curTyphoon: {
        'name': 'Carmen', 
        'time': '1949.1.13-1949.1.25',
        'max_category': 5,
        "max_wind_speed": 45,
        "min_pressure": 990
      },
      curPath: [],
      infoMode: 'overview',
      polyline: [],
      star: false,
      unreadNum: 0,
    }
  },
  watch: {
    selectTyphoonID(newid, oldid) {
      this.chosenTyphoonID = newid;
      this.changeChosenID();
    }
  },
  computed: {
    markers(){
      let markers = [];
      for(let i=0; i<this.curPath.length; i++){
        markers.push({
          position: [this.curPath[i]['longitude'], this.curPath[i]['latitude']],
          icon: this.getImageUrl(`../assets/dot${this.curPath[i]['category']}.png`)
        })
      }
      return markers;
    },
    polylines(){
      let polylines = [];
      for(let i=0; i<this.curPath.length-1; i++){
        polylines.push({
          path: [[this.curPath[i]['longitude'], this.curPath[i]['latitude']], [this.curPath[i+1]['longitude'], this.curPath[i+1]['latitude']]],
          color: this.categoryColor(this.curPath[i]['category'])
        })
      }
      return polylines;
    },
    pressures(){
      let pressures = [];
      for(let i=0; i<this.curPath.length; i++){
        pressures.push(this.curPath[i]['pressure'])
      }
      return pressures;     
    },
    speeds(){
      let speeds = [];
      for(let i=0; i<this.curPath.length; i++){
        speeds.push(this.curPath[i]['wind_speed'])
      }
      return speeds;     
    },
    times(){
      let times = [];
      for(let i=0; i<this.curPath.length; i++){
        let time = new Date(this.curPath[i]['time'])
        let str = `${time.getFullYear()}.${time.getMonth()+1}.${time.getDate()} ${time.getHours()}:00`
        times.push(str)
      }
      return times;          
    },
    tableData(){
      let table = [];
      for(let i=0; i<this.curPath.length; i++){
        let item = {}
        const currentDate = new Date(this.curPath[i]['time']);
        const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' };
        item['time'] = currentDate.toLocaleString('CN', options);
        item['pressure'] = this.curPath[i]['pressure']
        item['speed'] = this.curPath[i]['wind_speed']
        if(!item['speed'])
          item['speed'] = '-'
        item['category'] = this.curPath[i]['category']
        table.push(item)
      }
      return table;        
    }
  },
  methods:{    
    categoryColor(category){
      const list = ['1c54ff', '6cc343', 'ffc309', 'ff7209', 'e83b0c', 'e80cae', 'bd00ff', '', '', 'aaaaaa' ]
      return '#' + list[category]
    },
    changeChosenID(){
      serviceAxios.get(`/getTyphoonById/${this.chosenTyphoonID}`)
        .then(response => {
          this.curTyphoon = response.data['typhoon'];
          if (this.curTyphoon.end_time){
            let start = new Date(this.curTyphoon.start_time);
            let end = new Date(this.curTyphoon.end_time);
            this.curTyphoon['time'] = `${start.getFullYear()}.${start.getMonth()+1}.${start.getDate()}-${end.getFullYear()}.${end.getMonth()+1}.${end.getDate()}`
          }
          else{
            let start = new Date(this.curTyphoon.start_time);
            this.curTyphoon['time'] = `${start.getFullYear()}.${start.getMonth()+1}.${start.getDate()}-至今`
          }
          this.getPath();
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });

      serviceAxios.get(`/getTyphoonFav/${this.chosenTyphoonID}`)
        .then(response => {
          this.star = response.data['star']
        })
    },
    drawPressureAndSpeed(){
      var myChart = echarts.init(document.getElementById('spgraph'));
      const maxPressure = Math.ceil(Math.max(...this.pressures) / 10) * 10;
      const minPressure = Math.min(Math.min(...this.pressures) / 10) * 10;
      const maxWindSpeed = Math.ceil(Math.max(...this.speeds) / 10) * 10;
      const minWindSpeed = Math.ceil(Math.min(...this.speeds) / 10) * 10;
      var option = {
        legend: [
              {
                bottom: "8%",
                left: "25%",
                data: [ {name: "风速" } ]
              },
              {
                bottom: "8%",
                right: "25%",
                data: [ {name: "气压"} ]
              }
            ],
            xAxis: {
              type:'category',
              data: this.times,
              axisTick:{
                show:false 
              },
              axisLabel:{
                show:false 
              },
            },
            yAxis : [{
              type: 'value',
              name:'风速(m/s)',
              min: minWindSpeed,
              max: maxWindSpeed,
              interval: (maxWindSpeed - minWindSpeed) / 5,
              splitNumber: 5,
              axisLabel:{
                textStyle:{
                  color:"#409EFF"
                }
              }
            },
            {
              type: 'value',
              name:'气压(hPa)',
              min: minPressure,
              max: maxPressure,
              interval: (maxPressure - minPressure) / 5,
              splitNumber: 5, //设置坐标轴的分割段数
            }],
        tooltip : {
            trigger: 'axis',
            axisPointer: {
              label: {
                backgroundColor: '#6a7985'
            }
          }
        },
        series: [
          {
            name: "风速",
            type: "line",
            color: ["#409EFF"],
            itemStyle: {
              normal: {
                lineStyle: {
                  width:1.5
                }
              }
            },
            symbol: "none",
            smooth: true,
            data: this.speeds
          },
          {
            name: "气压",
            type: "line",
            color: ["#909399"],
            itemStyle: {
              normal: {
                lineStyle: {
                  width:1.5
                }
              }
            },
            symbol: "none",
            smooth: true,
            yAxisIndex: 1, //在单个图表实例中存在多个y轴的时候有用
            data: this.pressures
          },
        ],
        grid:{
          right: 50
        },
        textStyle: {   
          fontFamily: 'HarmonyOS Sans SC' 
        },
      };
      myChart.setOption(option);
    },
    getPath(){
      serviceAxios.get(`/getTyphoonPathById/${this.chosenTyphoonID}`)
        .then(response => {
          this.curPath = response.data['path'];
          this.drawPressureAndSpeed();
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    searchByStr(str){
      if(str==''){
        this.options=[]
        return;
      }
      serviceAxios.get(`/searchTyphoonByStr/${str}`)
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
    getImageUrl(url){
      return new URL(url, import.meta.url).href;
    },
    toggleStar(){
      if(this.star){
        serviceAxios.get(`/unsetTyphoonFav/${this.chosenTyphoonID}`)
        .then(response => {
          this.star = false;
        })
        .catch(err=>{
          this.star = false;
        })
      }
      else{
        serviceAxios.get(`/setTyphoonFav/${this.chosenTyphoonID}`)
        .then(response => {
          this.star = true;
        })
        .catch(err=>{
          this.star = true;
        })
      }
      
    },
    getAlert(){
      let color = { '红色': '#E63415',
          '橙色': '#FF6600',
          '黄色': '#FFDE0A',
          '蓝色': '#4167F0' }
      serviceAxios.get(`/getAlert`)
        .then(response => {
          for(let info of response.data['info']){
            let time = new Date(info['time']).toLocaleDateString('zh-CN', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit'}) + ' ' +
              new Date(info['time']).toLocaleTimeString('zh-CN', {
                  hour: '2-digit',
                  minute: '2-digit'
              });
            ElMessageBox({
                title: '气象台预警',
                message: h('p', null, [
                  h('span', null, info['station']),
                  h('span', null, `于 ${time} 发布台风`),
                  h('span', { style: `color: ${color[info['level']]}; font-weight: bold` }, info['level']),
                  h('span', null, '预警。')
                ]),
                })
          }
        })
        .catch(err=>{
        })
    },
    getUnreadNum(){
      serviceAxios.get('/getUnreadMessageNum')
      .then(res=>{
        console.log(res)
        this.unreadNum = res.data['num']
      })
    }
  },
  created(){
    this.chosenTyphoonID = this.$route.params.id;
    this.changeChosenID();
    this.getUnreadNum();
  },
  mounted(){
    this.getAlert();
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
      <el-select
      placeholder="查找台风信息"
      v-model="selectTyphoonID"
      size="large" style="width: 600px"
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
      <el-container class="right-container">
        <router-link style="width: 50px; margin-right:20px;" to="/message">
          <el-badge :value="unreadNum" :max="10" :hidden="unreadNum==0" style="margin-top: 10px; margin-right: 40px;">
            <el-icon size="30" ><ChatDotSquare /></el-icon>
          </el-badge>
        </router-link>
        <router-link to="/personal">
          个人页面
        </router-link>
      </el-container>
    </el-header>

    <el-container style="height:91%;">
      <el-aside width="400px">
        <el-scrollbar>
          <el-container>
          </el-container>
          <el-container @click="toggleStar" class="favorite-container">
            <img v-if="star" class="star" :src="getImageUrl(`../assets/star-chosen.png`)">
            <img v-else class="star" :src="getImageUrl(`../assets/star.png`)">
          </el-container>
          <el-container class="info-header-container">
                <img class="logo" :src="getImageUrl(`../assets/typhoon${curTyphoon['max_category']}.svg`)">
                <h1>{{ curTyphoon['name'].toUpperCase() }}</h1>
                <p>{{ curTyphoon['time'] }}</p>
          </el-container>
          <el-tabs v-model="infoMode">
            <el-tab-pane label="信息总览" name="overview" class="left-card-overview">
              <h3>特征数据</h3>
              <el-container class="statics-container">
                <el-container class="statics-group">
                  <el-avatar size="large" :style="`background-color:${categoryColor(curTyphoon['max_category'])}`">{{curTyphoon['max_category']}}</el-avatar>
                  <p>最高级别</p>
                </el-container>
                <el-container class="statics-group">
                  <el-avatar size="large">{{curTyphoon['min_pressure']}}</el-avatar>
                  <p>最低气压(hPa)</p>
                </el-container>
                <el-container class="statics-group">
                  <el-avatar size="large">{{curTyphoon['max_wind_speed']}}</el-avatar>
                  <p>最大风速(m/s)</p>
                </el-container>
              </el-container>
              <h3 style="margin-top:15px;">风速与气压</h3>
              <el-container style="width: 100%;height: 400px; margin-top: -20px;" id="spgraph">
              </el-container> 
            </el-tab-pane>
            <el-tab-pane label="详细数据" name="details">
              <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="time" align="center" width="150px" label="时间"/>
                <el-table-column prop="category" align="center" label="级别"/>
                <el-table-column prop="pressure" align="center" label="气压"/>
                <el-table-column prop="speed" align="center" label="风速" />
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-scrollbar>
      </el-aside>
      <el-main>
        <el-amap vid="amap" :zoom="5" mapStyle="amap://styles/light">
          <el-amap-marker
            v-for="marker in markers"
            :position="marker.position"
            :icon="marker.icon"
            anchor="center">
          </el-amap-marker>
          <el-amap-polyline
            v-for="polyline in polylines"
            :path="polyline.path"
            :strokeColor="polyline.color"
            strokeStyle="solid"
            :strokeWeight="5">
          </el-amap-polyline>
        </el-amap>
      </el-main>
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
#page{
  position: absolute;
  height: 100%;
  width: 100%;
  margin: 0;
}

/deep/.el-tabs__nav-wrap
.el-tabs__nav-scroll
.el-tabs__nav {
  width: 100%;
  display: flex;
  justify-content: space-around;
}

.favorite-container{
  display: flex;
  justify-content: end;
  padding: 20px;
  padding-bottom: 0;
  opacity: 0.6;
}

.star{
  width: 20px;
  cursor: pointer;
}

.router-link-active {
  text-decoration: none;
  color: black;
}

a{
  text-decoration: none;
  color: black;
}

.el-aside{
  background-color: white;
  border-right: solid rgb(215, 215, 215) 1px;
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

.left-card-overview{
  display: flex;
  flex-direction: column;
  justify-content: center; 
  padding: 10px 30px;
  align-items: start;
}

.left-card-overview h3{
  font-size: 15px;
  color: rgb(120, 120, 120);
  margin-bottom: 15px;
}

.left-card-overview .statics-container{
  display: flex;
  justify-content: start; 
  flex-wrap: wrap;
  width: 100%;
}

.el-header{
  border-bottom: solid rgb(215, 215, 215) 1px;
}

.left-card-overview .statics-group{
  width: 50%;
  margin: 15px 0;
  display: flex;
  align-items: center;
  flex-grow: 0;
}

.left-card-overview p{
  margin-left: 10px;
  font-size: 13px;
}

.info-header-container{
  display: flex;
  flex-direction: column;
  width: 100%;
  justify-content: center; 
  align-items: center;
  margin: 50px 0;
  margin-bottom: 30px;
}

.info-header-container h1{
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  margin-bottom: 5px;
}

.el-input{
  font-size: 16px;
  flex-grow: 0;
}

.el-aside{
  height: 100%;
  overflow-y: auto;
}

.logo-container{
  flex-grow: 0;
  display: flex;
  justify-content: space-between; 
  align-items: center; 
}

.title-container{
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: start; 
}

.right-container{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-grow: 0;
  margin-right: 10px;
}

.el-avatar{
  font-size: 18px;
  font-weight:700;
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

.el-header {
  display: flex;
  justify-content: space-between; 
  align-items: center; 
  padding: 0 10px;
}

.el-main{
  padding: 0;
  height: 100%;
}

</style>