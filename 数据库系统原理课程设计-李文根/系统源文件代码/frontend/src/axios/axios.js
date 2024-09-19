import axios from "axios";
import router from "../router/routers";

const serviceAxios = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 5000, 
  withCredentials: false
});

serviceAxios.interceptors.request.use(
	config=>{
		const token = localStorage.getItem('token');
    	// 请求头加上token
		if(token)
			config.headers.authorization = `Bearer ${token}`
		return config
	},err=>{
		return Promise.reject(err);
	}
)

export default serviceAxios;