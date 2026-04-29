<!-- Author: mikewang6700 -->
# 历史清理（草稿）——风险说明与命令

警告与风险：
- 使用 `git filter-repo` 或 `bfg-repo-cleaner` 会重写 Git 历史（强制 push 会更新远端历史）。这会使所有已克隆仓库的历史与远端不再兼容，所有协作者必须重新 clone 或手动处理重写后的历史。请在进行之前备份仓库（镜像克隆）并通知所有协作者。
- 务必先在本地测试命令并检查删除结果，再选择是否推送到远端。

推荐流程（`git filter-repo`，现代且高效）：

1) 备份与镜像克隆：

```bash
git clone --mirror <repo-url> repo-mirror.git
cd repo-mirror.git
```

2) 运行 `git filter-repo` 删除指定文件或匹配字符串（示例：删除私钥文件和替换敏感字符串）：

删除特定路径：

```bash
git filter-repo --invert-paths --paths docker/nginx/ssl/llmops.shortvar.com.key
```

按字符串替换（示例：把明文 API Key 替换为 <REDACTED>）：

```bash
git filter-repo --replace-text ../replacements.txt
```

其中 `replacements.txt` 示例内容：

```
# 替换格式：<要替换的文本>==>REPLACEMENT
sk-hsCakL5nDjwe5LGSnSR0U3kL8emdYpLeMctPROCIIzSPfyv6==><OPENAI_API_KEY_REDACTED>
ftBC9hKkjfdbdi0wW3T6kEtMh5BZFpGa1DF8==><WEAVIATE_API_KEY_REDACTED>
llmops123456==><REDACTED_PASSWORD>
```

3) 检查结果（查看是否还存在敏感字符串）：

```bash
git grep -n "sk-" || true
git grep -n "ftBC9h" || true
```

4) 如果确认无误，强制推送到远端（会重写远端历史）：

```bash
git push --force --mirror origin
```

---

使用 BFG 的简单示例（相比 filter-repo 更简洁，但也会重写历史）：

1) 备份：`git clone --mirror <repo-url>`
2) 运行 BFG：

```bash
# 删除某个文件
bfg --delete-files llmops.shortvar.com.key repo-mirror.git

# 使用替换文件替换正文
bfg --replace-text replacements.txt repo-mirror.git
```

3) 进入镜像仓库并执行垃圾回收并强推：

```bash
cd repo-mirror.git
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force --mirror origin
```

---

我已将这些命令保存为草稿。如果你确认我可以继续执行（完全清理历史并强推远端），请回复“确认要重写历史并推送”，并确保你有权限且已备份所有重要分支。我不会在未得到你确认前运行这些命令。
