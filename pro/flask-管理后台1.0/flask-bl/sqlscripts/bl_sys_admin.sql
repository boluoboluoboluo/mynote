--建表
drop table if exists bl_sys_admin;
create table bl_sys_admin(
	id bigserial primary key not null,			--说明bigserial 代表类型为bigint，且能实现自增
	admin_name character varying(50) not null default '',
	password character varying(500) not null default '',
	nick_name character varying(100) not null default '',
	role_id int not null default 0,
	email character varying(100) not null default '',
	createtime bigint not null default 0,
	updatetime bigint not null default 0,
	is_del int not null default 0
);
comment on column bl_sys_admin.id is '主键id';
comment on column bl_sys_admin.admin_name is '用户名';
comment on column bl_sys_admin.password is '密码';
comment on column bl_sys_admin.nick_name is '昵称';
comment on column bl_sys_admin.role_id is '角色id';
comment on column bl_sys_admin.email is '邮箱';
comment on column bl_sys_admin.createtime is '创建时间';
comment on column bl_sys_admin.updatetime is '更新时间';
comment on column bl_sys_admin.is_del is '是否逻辑删除状态，0启用1停用';

--插入数据
insert into bl_sys_admin (admin_name,password,nick_name,email,createtime,updatetime) 
values('admin','pbkdf2:sha256:260000$LKnWuIhig7QwRyfq$197c3be3a208d96b518cec190728528043fabc49412f0cd75671e81a259f93f1','管理员','',floor(extract(epoch from now())),floor(extract(epoch from now())));


