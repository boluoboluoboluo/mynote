```sql
#id756589不存在则插入，否则不插入
insert into qnh_users(username,phone) select 'test','177xxxxxxxx' from dual where not exists (select id from qnh_users u where u.id=756589)
```

