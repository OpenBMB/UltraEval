## 下载模型


首次部署某模型时，需要从 HuggingFace 下载模型，根据模型大小，此过程可能需花费 10 分钟至 1 小时。其中下载前需要：

1.**登录 Huggingface CLI**：

输入以下命令并登录：

```
huggingface-cli login
```

2.**输入您的 Token**：

登录时，输入 Huggingface 上的 Token。
3.**下载模型**：

在这里既可以git clone对应的模型，也可以通过之后的单卡部署进行下载。