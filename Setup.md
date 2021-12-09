# Setup Lambda Locally

Get [aws-sam-cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

```bash
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
sam --version
```

Init application:

```bash
sam init
```

Build and invoke application:

```bash
sam build -t hello_world.yaml
sam local invoke
```

Start api in local environment:

```bash
sam local start-api
```

```bash
curl http://127.0.0.1:3000/hello
```
