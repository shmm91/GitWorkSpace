### Git基本概念

Git是一个开源的分布式版本控制系统，其初始目的是为了帮助管理Linux内核而开发的。

### Git配置

Git使用git config工具来配置和读取相应的工作环境变量。

* git config时使用--system选项，读写的是/etc/gitconfig文件,即系统中所有用户都普遍适用的配置。
* git config时使用--global选项，读写的事~/.gitconfig文件，即用户目录下的配置文件只适用于该用户。
* 当前项目中Git中的配置文件（即工作目录中的.git/config），仅仅对当前项目有效，每一个级别的配置会覆盖上一层的相同配置。

Windows系统，Git会寻找主目录下的.gitconfig文件，主目录一般是C：\Documents and Settings\$USER。

#### 配置用户信息

```
git config --global user.name "shmm91"
git config --global user.email shmm91@sina.com
```

#### 配置文本编辑器

```
git config --global core.editor emacs
```

#### 配置差异分析工具

```
git config --global merge.tool vimdiff
```

#### 查看配置信息

```
git config --list
```

### Git工作流程

一般的工作流程如下：

* clone Git资源作为工作目录。
* 在clone的资源上添加或者修改文件。
* 如果他人修改了，你也可以更新资源。
* 在提交前查看修改。
* 提交修改。
* 在修改完成后，如果发现错误，可以撤回提交并再次修改并提交。

工作流程如下图：![](C:\Users\shmm\Desktop\笔记\git-process.png)

### Git分区

工作区：即电脑里能看到的目录。

暂存区：即stage,或index区，一般存放在“.git目录下”的index文件（.git/index），也叫索引区。

版本库：工作区有一个隐藏目录.git，是Git的版本库。

![](C:\Users\shmm\Desktop\笔记\gitworkspace.jpg)

上图中左侧为工作区，右侧为版本库，在版本库中标记为index的区域是暂存区-stage/index，标记为master的是master分支代表的目录树。

HEAD实际是指向master分支的一个游标，图中出现HEAD命令的地方均可以用master替换。

图中的objects标识的区域为Git的对象库，实际位于“.git/objects”目录下，里面包含了创建的各种对象及内容。

* 当对工作区域修改或者新增的文件执行git add命令时，暂存区的目录会被更新，同时工作区修改或者新增的文件内容被写到对象库中的一个新对象中，而该对象的ID被记录在暂存区的文件索引中。
* 当执行git commit时，暂存区的目录树写到版本库中，master分支会做响应的更新，即master指向的目录树就是提交时暂存区的目录树。
* 当执行git reset HEAD命令时，暂存区的目录树会被重写，被master分支做响应的更新，但是工作区不受影响。
* 当执行git rm --cached <file> 命令时，会直接从暂存区删除文件，工作区不做响应改变。
* 当执行git checkout. 或者git checkout --<file>命令时，会用暂存区全部或者指定的文件替换工作区的文件。这个操作很危险，会清楚工作区中未添加到暂存区的改动。
* 当执行git checkout HEAD .或者git checkout HEAD <file>命令时，会用HEAD指向的master分支中的全部或者部分文件替换暂存区以及工作区的文件，这个命令也极其危险。因为不但会清除工作区中未提交的改动，也会清除暂存区中未提交的改动。

### Git创建仓库

Git使用git init命令来初始化一个Git仓库，该命令会生成一个.git目录，该目录包含了资源的所有元数据，其他的项目目录保持不变。

```
git init newrepo
```

初始化后，会在newrepo目录下出现一个.git目录，所有Git需要的数据和资源都存放在这个目录。

如果当前目录下有几个文件想要纳入版本控制，需要先用git add命令告诉Git开始对这些文件进行跟踪，然后提交：

```
git add *.c
git add README
git commit -m '初始化项目版本'
```

clone仓库的命令格式为：

```
git clone <repo>
```

如果需要clone到指定的目录，可以使用以下命令格式：

```
git clone <repo> <directory>
```

如果要自定义新建的项目名称，可以在上面的命令末尾指定新的名字：

```
git clone git://github.com/schacon/grit.git mygrit
```

git clone时可以使用不同的协议，如下：

```
git clone git@github.com:fsliurujie/test.git
git clone git://github.com/fsliurujie/test.git
git clone https://github.com/fsliurujie/test.git
```

git add 命令将内容写入缓存区，git commit将缓存区内容添加到仓库中。

### Git分支管理

列出分支基本命令：

```
git branch
```

手动创建一个分支

```
git branch testing
```

切换分支

```
git checkout testing
```

创建分支并切换到该分支下

```
git checkout -b testing
```

删除分支

```
git branch -d testing
```

合并分支（将testing合并到主分支）

```
git merge testing
```

### Git标签

创建带注释的标签

```
git tag -a v1.0
```

追加标签

```
git tag -a v1.0 56454td
```

查看标签

```
git tag
```

### Git远程仓库

在git-bash下执行以下命令生成SSH Key

```
ssh-keygen -t rsa -C "shmm91@sina.com"
```

将生成的id_rsa.pub复制到github账户设置SSH and GPG keys里。

输入以下命令测试是否成功：

```
ssh -T git@github.com
```

将本地仓库推送到github

```
git remote add origin https://github.com/shmm91/GitWorkSpace.git
git push -u origin master
```

查看当前配置有哪些远程仓库

```
git remote
```

添加-v参数，查看实际链接地址

```
git remote -v
```

从远程仓库下载分支与数据，该命令执行完需要执行git merge远程分支到你所在的分支。

```
git fetch
git fetch origin
```

从远端仓库提取数据并尝试合并到当前分支

```
git merges
git merge origin/master
```

推送新分支与数据到某个远端仓库：

```
git commit -m "***"
git push -u origin master
```

删除远程仓库

```
git remote rm "***"
```

