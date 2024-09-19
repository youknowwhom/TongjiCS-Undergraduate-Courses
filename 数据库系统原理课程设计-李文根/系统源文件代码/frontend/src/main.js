import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/theme-chalk/el-message.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import VueAMap, {initAMapApiLoader} from '@vuemap/vue-amap';
import '@vuemap/vue-amap/dist/style.css'

initAMapApiLoader({
  key: 'aa77c73bcbb93f304fd19800d73480f9',
  securityJsCode: '089b94688ce3d90e53d1f90e2480c1c9',
  plugin: ["AMap.Autocomplete", 
           "AMap.PlaceSearch",
           "AMap.Scale",
           "AMap.OverView",
           "AMap.ToolBar",
           "AMap.MapType",
           "AMap.PolyEditor",
           "AMap.CircleEditor", 
           "AMap.Geolocation"]})

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(ElementPlus)
app.use(VueAMap)
app.use(router)
app.mount('#app')