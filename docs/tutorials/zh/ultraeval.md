UltraEval是一个开源的基础模型能力评测框架，提供了一套轻量级、易于使用的评测体系。整体框架组织如下图所示:

<div align="center">
<p align="center">
<img src="../../pics/ultraeval_pipeline_white.png" width="800px">
</p>
</div>

按照操作顺序，共分为【数据准备】、【模型部署】、和【任务评测】三大模块，分别对应

* [【配置文件】](./configuration_file/config.md)
* [【模型部署】](./deployment_model/model_download.md)
* [【任务评测】](./evaluation/model_instantiation.md)

此外UltraEval具有很好的扩展性，为了便于用户扩展其他任务或者模型，我们提供了定制化评测流程。
* [【用户个性化设置教程】](./customization/new_dataset.md)


