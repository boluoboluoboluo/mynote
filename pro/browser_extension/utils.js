// 当前未使用

// 引入方式:
// import { storage_get, storage_update } from './utils.js';
//========================================
// 获取缓存内容
// tabid: 当前页面id
// localorsession: chrome.local.local 或者 session 获取,参数值为 "local" 或 "session"
// key: 通过 键值对的 key 获取
//========================================
export async function storage_get(tabid,localorsession,key){
	let data = null;
	let re_data = null;
	if(localorsession === "local"){
		data = await chrome.storage.local.get([tabid]);
	}else if(localorsession === "session"){
		data = await chrome.storage.session.get([tabid]);
	}

	if(data[tabid])re_data = data[tabid][key];
	return re_data;
}
//========================================
// 根据key更新数据
// tabid: 当前页面id
// localorsession: chrome.local.local 或者 session 获取,参数值为 "local" 或 "session"
// newdata: 要添加的数据
//========================================
export async function storage_update(tabid,localorsession,key,newdata){
	let data = null;
	if(localorsession === "local"){
		data = await chrome.storage.local.get([tabid]);
		data[tabid] = data[tabid] || {};
		data[tabid][key] = newdata;
		await chrome.storage.local.set({[tabid]:data[tabid]})
	}else if(localorsession === "session"){
		data = await chrome.storage.session.get([tabid]);
		data[tabid] = data[tabid] || {};
		data[tabid][key] = newdata;
		await chrome.storage.session.set({[tabid]:data[tabid]})
	}
}

