# 代码贡献

    如果你：
    
    - 有新的想法
    - 提交Feature
    - Bug report/fix
    - 贡献文档
    - Help wanted
    
    建议先提[Issues](https://github.com/hango-io/hango-gateway/issues)，描述你的目的或者问题。  

## 代码/文档贡献流程

Hango 项目分多个模块仓库，下面以 Hango-portal 为例，介绍代码如何提交至我们的开源仓库！

### 1. fork代码

访问 [https://github.com/hango-io/portal](https://github.com/hango-io/portal)，选择指定仓库，点击右上角的 Fork ，将 Hango-portal 仓库代码 fork 到自己的 github 仓库中。

### 2. 创建本地工程

本地 clone 远端的 github 仓库，添加、修改制定内容，如何进行本地调试可以参考本地调试章节；代码开发请遵守 [Hango 代码开发规范](https://hango-io.github.io/developer-guide/development/)，否则在代码 review 阶段会被驳回

### 3. 将变更推送到远端

本地完成代码构建后，我们需要将代码内容进行 commit， commit 按如下格式进行信息提交

commit message格式
```
<type>(<scope>): <subject>
```
- type: 用于说明git commit的类别，只允许使用下面的标识。
- feat: 新功能（feature）。
- fix/to: 修复bug
- docs: 文档（documentation）。
- style: 格式（不影响代码运行的变动）。
- refactor: 重构（即不是新增功能，也不是修改bug的代码变动）。
- perf: 优化相关，比如提升性能、体验。
- test: 增加测试。
- chore: 构建过程或辅助工具的变动。
- revert: 回滚到上一个版本。
- merge: 代码合并。
- sync: 同步主线或分支的Bug。
- scope(可选): scope用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。
- subject(必须): subject是commit目的的简短描述，不超过50个字符。
> 结尾不加其他标点符号

commit 要求功能聚合，因此在推送前请进行适当的代码 rebase 操作

### 4. 提交Pull Request

待代码提交到个人的 fork 仓库后，我们可以向 Hango-portal 主仓库进行 PR 提交， PR 提交信息如下

- 关联 issue
- 提交人（关联人）
  Signed-off-by: \[姓名\] <邮箱>
- PR 简要描述
- 对模块或 Hango 项目的影响点

### 5. 其他

提交 PR 后，可以通过我们的官方微信平台或邮箱方式（hango.io@gmail.com）通知我们检视合入

![wechat](./images/hango-wechat.png)