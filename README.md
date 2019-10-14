# quant




# 修改内核参数
    vim /etc/sysctl.conf
    net.core.somaxconn= 4000
    sysctl -p

# 安装MariaDB

    cat <<EOF | sudo tee /etc/yum.repos.d/MariaDB.repo
    [mariadb]
    name = MariaDB
    baseurl = http://yum.mariadb.org/10.3/centos7-amd64
    gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
    gpgcheck=1
    EOF
    
    
    cat <<EOF | sudo tee /etc/yum.repos.d/MariaDB.repo
    [mariadb]
    name = MariaDB
    baseurl = http://mirrors.ustc.edu.cn/mariadb/yum/10.2/centos7-amd64/
    gpgkey = http://mirrors.ustc.edu.cn/mariadb/yum/RPM-GPG-KEY-MariaDB
    gpgcheck = 1
    EOF


```sh

yum install -y mariadb mariadb-server
systemctl start mariadb   #启动mariadb
systemctl enable mariadb  #设置开机自启动
mysql_secure_installation #设置root密码等相关
mysql -uroot           #测试登录
```


# 初始化数据库
```mysql

CREATE SCHEMA `quant` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin ;

```