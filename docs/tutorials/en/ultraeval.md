UltraEval is an open-source framework for evaluating the capabilities of foundational models, offering a lightweight and easy-to-use evaluation system. The overall framework structure is illustrated in the following diagram:

<div align="center">
<p align="center">
<img src="../../pics/ultraeval_pipeline_white.png" width="800px">
</p>
</div>

Following the operational sequence, it is divided into three main modules: 【Data Preparation】, 【Model Deployment】, and 【Task Evaluation】, corresponding to

* [【Configuration File】](./configuration_file/config.md)
* [【Model Deployment】](./deployment_model/model_download.md)
* [【Task Evaluation】](./evaluation/model_instantiation.md)

Additionally, UltraEval is highly extensible. To facilitate users in extending other tasks or models, we provide a customization evaluation process.
* [【Customization Tutorial】](./customization/new_dataset.md)