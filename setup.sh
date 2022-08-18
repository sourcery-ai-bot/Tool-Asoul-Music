#!/bin/bash
initVar() {
  echoType='echo -e'
}
initVar
echox() {
  case $1 in
  # 红色
  "red")
    # shellcheck disable=SC2154
    ${echoType} "\033[31m$2\033[0m"
    ;;
    # 绿色
  "green")
    ${echoType} "\033[32m$2\033[0m"
    ;;
    # 黄色
  "yellow")
    ${echoType} "\033[33m$2\033[0m"
    ;;
    # 蓝色
  "blue")
    ${echoType} "\033[34m$2\033[0m"
    ;;
    # 紫色
  "purple")
    ${echoType} "\033[35m$2\033[0m"
    ;;
    # 天蓝色
  "skyBlue")
    ${echoType} "\033[36m$2\033[0m"
    ;;
    # 白色
  "white")
    ${echoType} "\033[37m$2\033[0m"
    ;;
  esac
}
Gitpull() {
  git clone https://github.com/sudoskys/Tool-Asoul-Music.git || (
    echox yellow "Git failed,try pull from mirror"
    git clone https://gitclone.com/github.com/sudoskys/Tool-Asoul-Music.git
  )
}


dependenceInit() {
  cd Tool-Asoul-Music || (
    echo "Cant find !?"
    exit 1
  )
  pip3 install --upgrade pip
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt || pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt.bak || echox red "===pip install failed,please check it===== \n if you are in python3.10 please edit the requirements.txt,delete the pycrypto pkg"
  echox yellow "========Down=========="
}
dataBack="$(pwd)/tmp"
dir="$(pwd)/Tool-Asoul-Music"
data="$(pwd)/Tool-Asoul-Music/data"
echo "=============Setup============"

run() {
  if [ ! -d "$dir" ]; then
    echox skyBlue "初始化:No found ${dir}，init, setup..."
    Gitpull
    dependenceInit
  else
    # 初始化备份文件夹
    if [ ! -d "$dataBack" ]; then
      echox skyBlue "初始化备份文件夹：init ${dataBack}...."
      mkdir "$dataBack"
    fi
    # 备份配置文件
    if [ -f "${dir}/config.yaml" ]; then
      echox skyBlue "备份配置文件：backup ${dir}/config.yaml to ${dataBack} ...."
      cp -f "${dir}/config.yaml" "$dataBack"
    fi
    # 备份运行数据
    if [ -d "$data" ]; then
      echox skyBlue "备份运行数据：Copy run data to ${dataBack}...."
      cp -rf "$data" "$dataBack" #文件夹目录 文件夹上级
    fi
    # 询问
    read -r -p "请问，是否使用可能存在的备份配置？Do you want to update your app with probably exist old data？${dir} y/n?" input
    case $input in
    [nN][oO] | [nN])
      echox red "We will reinstall a pure app...."
      rm -rf "${dir}"
      Gitpull
      dependenceInit
      ;;
    [yY][eE][sS] | [yY])
      rm -rf "${dir}"
      Gitpull
      if [ -f "${dataBack}/config.yaml" ]; then
        echox green "Reuse the config.yaml from ${dataBack}...."
        cp -f "${dataBack}/config.yaml" "$dir" #文件夹目录 文件夹上级
      fi
      if [ -d "${dataBack}/data" ]; then
        echox green "Reuse the run data from ${dataBack}...."
        cp -rf "${dataBack}/data" "$dir" #文件夹目录 文件夹上级
      fi
      dependenceInit || exit 1
      ;;
    *)
      echox skyBlue "Invalid input"
      ;;
    esac
  fi
}

run || {
  echox skyBlue "command failed"
}
