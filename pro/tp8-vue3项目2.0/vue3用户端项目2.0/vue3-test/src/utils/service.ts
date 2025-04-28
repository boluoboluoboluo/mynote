import axios from "axios";
import { ElMessage } from "element-plus";


// 创建 axios 实例
let service:any;
service = axios.create({
	baseURL: "", // api 的 base_url
	timeout: 50000 // 请求超时时间
});

// request 拦截器 axios 的一些配置
service.interceptors.request.use(
  (config:any) => {
    return config;
  },
  (error: any) => {
    // Do something with request error
    console.error("error:", error); // for debug
    return Promise.reject(error);
  }
);

// respone 拦截器 axios 的一些配置
service.interceptors.response.use(
  (res:any) => {
    if (res.status === 200) {
	  return res.data;
    } else {
	  ElMessage.error("网络错误")
      return Promise.reject(new Error("Error"));
    }
  },
  (error: any) => {
	ElMessage.error("请求错误")
	return Promise.reject(error)
  } 
);

export default service;