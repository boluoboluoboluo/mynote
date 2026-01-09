--角色表
drop table if exists bl_sys_role;
create table bl_sys_role(
	id bigserial primary key not null,			--说明bigserial 代表类型为bigint，且能实现自增
	role_name character varying(50) not null default '',
	role_desc character varying(500) not null default '',
	role_action text not null default '',
	createtime bigint not null default 0,
	updatetime bigint not null default 0,
	is_del int not null default 0
);
comment on column bl_sys_role.id is '主键id';
comment on column bl_sys_role.role_name is '角色名称';
comment on column bl_sys_role.role_desc is '角色描述';
comment on column bl_sys_role.role_action is '角色权限，以英文逗号隔开得权限节点id';
comment on column bl_sys_role.createtime is '创建时间戳，秒';
comment on column bl_sys_role.updatetime is '更新时间戳，秒';
comment on column bl_sys_role.is_del is '是否逻辑删除状态，0正常1删除';

--插入数据
insert into bl_sys_role (role_name,role_desc,role_action,createtime,updatetime) 
values('管理员','管理员权限','1,2',floor(extract(epoch from now())),floor(extract(epoch from now())));

insert into bl_sys_role (role_name,role_desc,role_action,createtime,updatetime) 
values('经理','经理权限','2',floor(extract(epoch from now())),floor(extract(epoch from now())));

insert into bl_sys_role (role_name,role_desc,role_action,createtime,updatetime) 
values('客服','管理员权限','3',floor(extract(epoch from now())),floor(extract(epoch from now())));


