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
  git clone https://github.com/sudoskys/Tool-Asoul-Music
  cd Tool-Asoul-Music || (
    echo "Cant find !?"
    exit 1
  )
  pip3 install --upgrade pip
  pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt || echo "===pip failed,please check it====="
  echo "Ok"
}
dataBack="$(pwd)/tmp"
dir="$(pwd)/Tool-Asoul-Music"
data="$(pwd)/Tool-Asoul-Music/data"
echo "=============Setup============"

run() {
  if [ ! -d "$dir" ]; then
    echox skyBlue "No found ${dir}，setup..."
    Gitpull
  else
    if [ ! -d "$data" ]; then
      if [ ! -d "$dataBack" ]; then
         mkdir "$dataBack"
      else
         echox skyBlue "Already exist ${dataBack}"
      fi
      echo "Auto Backup data to ${dataBack}...."
      cp -rf "$data" "$dataBack" #文件夹目录 文件夹上级
    fi
    echox skyBlue "Attention!!"
    read -r -p "默认使用旧的数据吗？Do you want to update with using your old data?[Y/n] " input
    case $input in
    [nN][oO] | [nN])
      echox skyBlue "Remove it"
      rm -rf Tool-Asoul-Music
      Gitpull
      exit 0
      ;;
    [yY][eE][sS] | [yY])
      if [ ! -d "$data" ]; then
        echox skyBlue "you haven t have ${data} ？？？....we will reinstall app...."
        rm -rf Tool-Asoul-Music
        Gitpull
      else
        mkdir "$dataBack"
        echox skyBlue "Copy old data to app...."
        cp -rf "$data" "$dataBack" #文件夹目录 文件夹上级
        rm -rf Tool-Asoul-Music
        Gitpull
        # mkdir "$data"
        cp -rf "${dataBack}/data" "$dir" #文件夹目录 文件夹上级
        echox skyBlue "All Down....."
      fi
      exit 0
      ;;

    *)
      echox skyBlue "Invalid input"
      ;;
    esac
  fi
}

run || {
  echox skyBlue "command failed"
  exit 1
}
