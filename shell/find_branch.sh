#!/bin/bash

# 1. 获取远程仓库的所有分支
#/bin/bash
git fetch --all
branches=$(git branch -r)

# 2. 过滤出符合条件的分支
filtered_branches=""
for branch in $branches; do
    if [[ $branch =~ ^origin/release_train_[0-9]{5}$ ]]; then
        filtered_branches="$filtered_branches $branch"
    fi
done

# 3. 按创建时间倒序排序，输出最新的一个分支
if [[ $filtered_branches == "" ]]; then
    echo "No matching branches found."
else
    latest_branch=$(git for-each-ref --sort=committerdate refs/remotes --format='%(refname:short)' $filtered_branches | head -1)
    echo "Latest matching branch: $latest_branch"
fi

#####################################################################################
# git branch -r --sort=-committerdate | grep -E "release_train_[0-9]{5}$" | head -1 #
#####################################################################################