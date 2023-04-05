# Template Development Environment to build nlp docker container apps
Runs deep learning stuff on top of docker in windows 10 on wsl2
I tested this out on windows10 wsl2 system with a 3080gtx/10GB 

See https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template for information on cloning this repo




see nvidia_tests.ipynb file in this repo for source of below info

## 4/1/23 update 
3 things required underneath:
* docker desktop 4.16.3 
  * (4.17.1 did NOT work - see https://github.com/docker/for-win/issues/13324 )
* nvidia-smi
    * NVIDIA-SMI 530.41.03
    * Driver Version: 531.41
    * CUDA Version: 12.1
* nvcc -V
```nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Jun__8_16:49:14_PDT_2022
Cuda compilation tools, release 11.7, V11.7.99
Build cuda_11.7.r11.7/compiler.31442593_0
```

* VScode Help-> About

```Version: 1.77.0 (user setup)
Commit: 7f329fe6c66b0f86ae1574c2911b681ad5a45d63
Date: 2023-03-29T10:02:16.981Z
Electron: 19.1.11
Chromium: 102.0.5005.196
Node.js: 16.14.2
V8: 10.2.154.26-electron.0
OS: Windows_NT x64 10.0.19045
Sandboxed: No
```

## Useful stuff - vscode
* https://code.visualstudio.com/docs/devcontainers/create-dev-container#_use-docker-compose
* https://code.visualstudio.com/docs/devcontainers/tutorial
* https://containers.dev/implementors/json_reference/ 
* https://containers.dev/features
* https://code.visualstudio.com/docs/devcontainers/containers



* https://docs.docker.com/get-started/
* https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml


* 
