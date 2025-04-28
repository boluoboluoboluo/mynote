### win10下，git配置sshkey：
* 右键Git Bash here

* 执行：

  ```sh
  cd ~/.ssh/
  ```

  若不存在则新建：

  ```sh
  mkdir ../.ssh/
  ```

* 继续执行：

  ```sh
  git config --global user.name "xxx"
  ```

  ```sh
  git config --global user.email "xxx@xxx.com"
  ```

  ```sh
  ssh-keygen -t rsa -C "xxx@xxx.com"
  ```

* 然后：将~/.ssh/id_rsa.pub的全部内容复制，在服务器（如gitlab）里面配置sshkey即可。



### 配置多个sshkey

```sh
ssh-keygen -t rsa -C "xxx@xxx.com" -f github_id_rsa			#生成的密钥文件起名字github_id_rsa，配置给github用
```

添加ssh配置：

.ssh`目录下新建`config

```sh
Host github.com
HostName github.com
PreferredAuthentications publickey
IdentityFile C:\Users\${username}\.ssh\github_id_rsa
```

测试：

```sh
ssh -T git@github.com
```





