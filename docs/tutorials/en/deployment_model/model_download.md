## Downloading the Model

When deploying a model for the first time, it is necessary to download the model from HuggingFace. Depending on the model size, this process may take from 10 minutes to an hour. Before downloading, you need to:

1. **Log in to Huggingface CLI**:

Enter the following command and log in:

```
huggingface-cli login
```

2. **Enter Your Token**:

When prompted during login, enter your Token from Huggingface.

3. **Download the Model**:

Here, you can either git clone the corresponding model or download it through the subsequent [Single-Card Deployment](./deployment.md) process.