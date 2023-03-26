
# 克隆代码仓库

## 代码仓库历史记录太多，克隆到本地，避免占用太多本地磁盘，只克隆最新的提交情况
如果你想克隆代码仓库的最新提交情况，可以使用 --depth 参数来限制克隆的历史记录深度，只获取最新的提交信息。例如： 

```bash
git clone --depth=1 https://github.com/username/repo.git
```
> 这将克隆 repo.git 仓库的最新提交记录。--depth=1 参数表示只获取最新的提交记录，不包括历史记录。
如果你想在克隆时忽略某些文件或目录，可以使用 .gitignore 文件来配置。这个文件列出了你想要忽略的文件或目录，以及一些通配符来匹配文件名。例如：

```bash
# 忽略所有 .txt 文件
*.txt

# 忽略目录 logs 和 tmp
logs/
tmp/
``` 
> 将 .gitignore 文件放在代码仓库的根目录下，并在克隆时添加 --exclude 参数来忽略这些文件或目录。例如：

```bash
git clone --depth=1 --exclude=.gitignore https://github.com/username/repo.git

```


