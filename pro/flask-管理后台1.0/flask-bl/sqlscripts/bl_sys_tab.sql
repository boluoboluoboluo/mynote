--建表(菜单表)
drop table if exists bl_sys_tab;
create table bl_sys_tab(
	id bigserial primary key not null,			--说明bigserial 代表类型为bigint，且能实现自增
	tab_name character varying(50) not null default '',
	tab_level int not null default 0,
	parent_id int not null default 0,
	icon character varying(50) not null default '',
	mode_code character varying(50) not null default '',
	jmp_url character varying(50) not null default '',
	ordering int not null default 0,
	createtime bigint not null default 0,
	updatetime bigint not null default 0
);
comment on column bl_sys_tab.id is '主键id';
comment on column bl_sys_tab.tab_name is '菜单(或权限节点)名称';
comment on column bl_sys_tab.tab_level is '菜单级别，0一级菜单，1二级菜单，2三级节点';
comment on column bl_sys_tab.parent_id is '所指向的父id';
comment on column bl_sys_tab.icon is '图标代码，一级菜单有显示图标';
comment on column bl_sys_tab.mode_code is '权限标识，唯一，在具体的后台请求方法配置该项，实现绑定';
comment on column bl_sys_tab.jmp_url is '跳转路径，点击二级菜单实现跳转';
comment on column bl_admibl_sys_tabn_tab.ordering is '菜单排序';
comment on column bl_sys_tab.createtime is '创建时间';
comment on column bl_sys_tab.updatetime is '更新时间';

