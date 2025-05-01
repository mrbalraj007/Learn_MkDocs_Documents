---
title:  "Mega Project Spotlight: Full-Stack DevSecOps Pipeline for EKS with GitHub Actions & Terraform"
publish: true
description: TESTING DOCUMENT USING GITHUB PAGES- 
cover_image: ./assets/image-10.png
tags:
  - example
  - article
  - blog
# originalArticleURL: "https://example.com/blog/example-title-blog"
# subtitle: Demo- TESTING DOCUMENT USING GITHUB PAGES
enableTableOfContent: true
isNewsletterActivated: true
---

## Executive Summary
This document outlines a solution for AWS cost optimization through automated monitoring and reporting. By implementing this solution, organizations can gain regular insights into their AWS spending patterns, identify cost spikes, and take appropriate actions to optimize cloud expenses.

## Key Points
- **Measurement First Approach**: You cannot optimize what you cannot measure
- **Daily Cost Tracking**: Automated daily reports provide consistent visibility
- **Service-based Analysis**: Breakdown of costs by AWS service helps pinpoint expensive resources
- **Spike Detection**: Comparing daily costs helps identify unusual spending patterns
- **Automated Slack Notifications**: Reduces manual monitoring effort and ensures timely awareness

## Tools and Technologies

| Tool/Technology | Purpose |
|----------------|---------|
| AWS Cost CLA | Command-line application for retrieving cost data |
| NodeJS/npm | Required for installing AWS Cost CLA |
| AWS CLI | For authentication and access to AWS resources |
| Slack | Communication platform for receiving cost reports |
| Slack SDK (Python) | Used for uploading complete reports as files to Slack |
| Python | For creating the script to upload reports to Slack |
| Cron Jobs | For scheduling automated daily reporting |

---
## <span style="color: Yellow;"> Prerequisites </span>
Before diving into this project, here are some skills and tools you should be familiar with:

- Terraform installed on your machine.
- A GitHub account.
- A GitHub personal access token with the necessary permissions to create repositories.

> ⚠️ **Important:** 

> 01. Make sure First you will create a **`.pem`** key manually from the AWS console. i.e "MYLABKEY.pem" because it will be used for creating `EC2` VMs and `EKS cluster`.
> 02. Copy `MYLABKEY.pem` in the terraform directory (`01.Code_IAC_Selfhosted-Runner-and-Trivy` and `03.Code_IAC_Terraform_box` ) as below your terraform code
> 03. [Generate the Github Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

```sh
ls 
\Learning_GitHub_Action\02.Github_Action_DevOps-Project\Terraform_Code_Infra_setup


Mode                 LastWriteTime         Length Name                                                                                                                                                                                              
----                 -------------         ------ ----                                                                                                                                                                                              
dar--l          17/04/25  12:48 PM                .terraform                                                                                                                                                                                        
dar--l          21/04/25  12:34 PM                00.Code_IAC-github-repo                                                                                                                                                                           
dar--l          21/04/25  12:34 PM                01.Code_IAC_Selfhosted-Runner-and-Trivy                                                                                                                                                           
dar--l          21/04/25   1:38 PM                02.Code_IAC_SonarQube                                                                                                                                                                             
dar--l          21/04/25  12:34 PM                03.Code_IAC_Terraform_box                                                                                                                                                                         
-a---l          20/08/24   1:45 PM            493 .gitignore                                                                                                                                                                                                                                                                                                                                    
-a---l          21/04/25   1:59 PM          18225 AboutThis Project.md                                                                                                                                                                              
-a---l          19/04/25   8:48 PM           1309 main.tf # <---(This one need to run)

````

[Clone repository for terraform code](https://github.com/mrbalraj007/Learning_GitHub_Action/tree/main/02.Github_Action_DevOps-Project/Terraform_Code_Infra_setup)<br>
  > 💡 **Note:** Replace GitHub Token, resource names and variables as per your requirement in terraform code
  > - For **`github Repo`** Token value to be updated in file 
      - `00.Code_IAC-github-repo/variables.tf` (i.e default- `xxxxxx`*)
  > - **For EC2 VM** 
      - `01.Code_IAC_Selfhosted-Runner-and-Trivy/terraform.tfvars` (i.e keyname- `MYLABKEY`*)
      - `03.Code_IAC_Terraform_box/terraform.tfvars` (i.e keyname- `MYLABKEY`*)
  > - For **Cluster name** 
      - `03.Code_IAC_Terraform_box/k8s_setup_file/main.tf` (i.e `balraj`*).
  > - For **Node Pod**
      - `03.Code_IAC_Terraform_box/k8s_setup_file/variable.tf` (i.e `MYLABKEY`*)
  
      
**Set up your GitHub token**:
   - Create a new GitHub personal access token with the `repo` scope at https://github.com/settings/tokens. 
   - Then set it as an environment variable (DO NOT commit your token to version control):
   
   ```bash
   # For Linux/macOS
   export GITHUB_TOKEN=your_github_token
   
   # For Windows Command Prompt
   set GITHUB_TOKEN=your_github_token
   
   # For Windows PowerShell (I used this one)
   # $env:GITHUB_TOKEN="your_github_token"
   $env:TF_VAR_github_token = "your-github-personal-access-token"
   ```
**Test and verify with curl again in powershell terminal:**
   ```powershell
   $headers = @{
    Authorization = "token $env:TF_VAR_github_token"
   }
   Invoke-WebRequest -Uri "https://api.github.com/user" -Headers $headers
   ```
   - You should see your GitHub user info in JSON, **not** "Bad credentials".
<!-- 
## **Key Points**
1. **GitHub Actions Overview**:
   - GitHub Actions is used as the CI/CD tool for this project.
   - It eliminates the need for setting up and maintaining Jenkins servers by providing managed runners.

2. **Pipeline Stages**:
   - **Compile**: Builds the application.
   - **Security Checks**: Scans for vulnerabilities using Trivy and GitLeaks.
   - **Unit Testing**: Executes test cases to ensure code quality.
   - **Build and Publish Docker Image**: Builds a Docker image and uploads it as an artifact.
   - **Deploy to Kubernetes**: Deploys the application to an EKS cluster using Terraform.


4. **Why Use This Project**:
   - Automates the software delivery process.
   - Ensures code quality and security through automated checks.
   - Simplifies deployment to Kubernetes clusters.
   - Demonstrates best practices for CI/CD pipelines.

5. **Takeaways**:
   - Understanding of GitHub Actions and its capabilities.
   - Hands-on experience with integrating security tools like Trivy and GitLeaks.
   - Knowledge of deploying applications to Kubernetes using Terraform.
   - Insights into managing AWS resources with AWS CLI. -->

---
## **Step-by-Step Process**

### <span style="color: Yellow;">Setting Up the Infrastructure </span>

I have created a Terraform code to set up the entire infrastructure, including the installation of required `tools` and `EC2` automatically created.

#### 1. Setup Environment
- Create a virtual machine (or use existing server)
- Update system packages
- Install NodeJS using NVM
- Install AWS CLI

#### 2. Install and Configure AWS Cost CLA
- Install AWS Cost CLA using npm
- Configure AWS credentials using `aws configure`
- Test basic cost reporting with command `aws-cost`

> 💡 **Note:**  &rArr;<span style="color: Green;"> `**EKS cluster**` creation will take approx. 15 to 20 minutes.
> 
#### <span style="color: Yellow;"> To Create EC2 Instances

First, we'll create the necessary virtual machines using `terraform` code. 

Below is a terraform Code:

Once you [clone repo](https://github.com/mrbalraj007/Learning_GitHub_Action/blob/main/02.Github_Action_DevOps-Project/Terraform_Code_Infra_setup) then go to folder *<span style="color: cyan;">"02.Github_Action_DevOps-Project/Terraform_Code_Infra_setup"</span>* and run the terraform command.
```bash
cd 01.Github_Action_DevOps-Project/Terraform_Code_Infra_setup

$ ls

 00.Code_IAC-github-repo/   01.Code_IAC_Selfhosted-Runner-and-Trivy/   02.Code_IAC_SonarQube/   03.Code_IAC_Terraform_box/  'AboutThis Project.md'   main.tf   
```

> 💡 **Note:** </span> &rArr; Make sure to run `main.tf` which is located outside of the folder. I have created the code in such a way that a single file will call all of the folders.

```bash
 ls -la
total 72
-rw-r--r-- 1 bsingh 1049089   493 Aug 20  2024  .gitignore
drwxr-xr-x 1 bsingh 1049089     0 Apr 21 12:34  00.Code_IAC-github-repo/
drwxr-xr-x 1 bsingh 1049089     0 Apr 21 12:34  01.Code_IAC_Selfhosted-Runner-and-Trivy/
drwxr-xr-x 1 bsingh 1049089     0 Apr 21 13:38  02.Code_IAC_SonarQube/
drwxr-xr-x 1 bsingh 1049089     0 Apr 21 12:34  03.Code_IAC_Terraform_box/
-rw-r--r-- 1 bsingh 1049089 21284 Apr 21 14:44 'AboutThis Project.md'
-rw-r--r-- 1 bsingh 1049089  1309 Apr 19 20:48  main.tf # <---This need to be run>
```
You need to run ```main.tf``` file using following terraform command.

Now, run the following command.
```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply 
# Optional <terraform apply --auto-approve>
```
-------
![alt text](All_ScreenShot/image.png)
![alt text](All_ScreenShot/image-1.png)
![alt text](All_ScreenShot/image-2.png)

- After Terraform deploys on the instance, now it's time to setup the cluster. If you logout the ssh session then reconnect the SSH and run to following command:

   ```bash
   eksctl utils write-kubeconfig --cluster="$CLUSTER_NAME" --region="$REGION"
   ```
- Once EKS cluster is setup then need to run the following command to make it intract with EKS.

   ```sh
   eksctl utils write-kubeconfig --cluster="balraj-cluster" --region="us-east-1"
   ```
   ![alt text](All_ScreenShot/image-3.png)

> > ⚠️ **Important:** <br>
*The ```aws eks update-kubeconfig``` command is used to configure your local kubectl tool to interact with an Amazon EKS (Elastic Kubernetes Service) cluster. It updates or creates a kubeconfig file that contains the necessary authentication information to allow kubectl to communicate with your specified EKS cluster.*

> > <span style="color: Orange;"> **What happens when you run this command**:</span><br>
The AWS CLI retrieves the required connection information for the EKS cluster (such as the API server endpoint and certificate) and updates the kubeconfig file located at ```~/.kube/config (by default)```.
It configures the authentication details needed to connect kubectl to your EKS cluster using IAM roles.
After running this command, you will be able to interact with your EKS cluster using kubectl commands, such as ```kubectl get nodes``` or ```kubectl get pods```.

   ```sh
   kubectl get nodes
   kubectl cluster-info
   kubectl config get-contexts
   ```
   ![alt text](All_ScreenShot/image-12.png)

![alt text](All_ScreenShot/image-17.png)
![alt text](All_ScreenShot/image-13.png)


---
### <span style="color: yellow;"> **Verify GitHub Repo and GitHub Actions**
   - Verify GitHub repository created and initialize it because we are using terraform.
      ![alt text](All_ScreenShot/image-16.png)
   - Verify a `.github/workflows` directory created along with two YAML file for the pipeline.
      ![alt text](All_ScreenShot/image-55.png)

### <span style="color: cyan;">**Adding a Virtual Machine as a Runner**
   - I'll be using self-hosted runner to execute all the pipeline.
   - Configure the runner by following the commands provided in GitHub's settings.
      ```
         Go to "GithubAction_DevOps_Projects"
         Click on settings
         then select the actions and choose "runners"
      ```
   ![alt text](All_ScreenShot/image-5.png)
   - Click on new `self-hosted runner` and select `Linux`
   - Notedown the token value somewhere as we need to in runner VM.
   ![alt text](All_ScreenShot/image-6.png)
   - Take putty session of `runner` EC2
   - Go to `actions-runner` folder
      ![alt text](All_ScreenShot/image-7.png)
   - Update/Paste the token value here as mentioned in screenshot.
      ![alt text](All_ScreenShot/image-8.png)
   - Change the execution mode for script and run it.
   - `chmod +x selfhost-runner.sh`

> 💡 **Note:** 
> >*Take note of the token value from here and paste it into the script in runner at the following spot. This ensures that the script executes successfully with the necessary permissions. Once you've finished, save your modifications and run the script to test whether it works as planned.*

#### **Troubleshooting:** 
- I am getting below error message while execute the file.
![alt text](All_ScreenShot/image-9.png)
![alt text](All_ScreenShot/image-10.png)
![alt text](All_ScreenShot/image-11.png)

![alt text](All_ScreenShot/image-12.png)
![alt text](All_ScreenShot/image-13.png)

![alt text](All_ScreenShot/image-14.png)
![alt text](All_ScreenShot/image-15.png)


Invite the Bot in Slack Channel
/invite @AWS Cost Notifier and click on `send`
![alt text](All_ScreenShot/image-16.png)

![alt text](All_ScreenShot/image-17.png)

![alt text](All_ScreenShot/image-18.png)

> 💡 **Note:** 
> >*You have to update all the required tokens and secrets value here. Part of Terraform code, I have already created a dummy values, which needs to be replaced. Once you have replaced the dummy values with the actual tokens and secrets, ensure that you test the configuration thoroughly to confirm that everything functions as expected. This will help prevent any issues during deployment and maintain the integrity of your infrastructure.*

- **To update the `EKS_KUBECONFIG` secret**
  - Take putty session of `Terraform EC2` instnace
  - run the command `cat ~/.kube/config`
  - copy the whole content and paste into the secret.
   ![alt text](All_ScreenShot/image-25.png)

### **Attach Role to Runner EC2**
   - Select the EC2 VM and click on the `actions` > `security`>` Mofify IAM Roles on the runner`.
   ![alt text](All_ScreenShot/image-14.png)
   - Select the role `Role_k8_Cluster_profile` 
   ![alt text](All_ScreenShot/image-15.png)
   - Click on update IAM Role.

### <span style="color: orange;">  **Writing the CI/CD Pipeline**
   - **Compile Stage**:
     - Use `actions/checkout` to clone the repository.
     - Set up the required environment (e.g., JDK 17 for Java projects).
     - Compile the application using build tools like Maven.
   - **Security Checks**:
     - Install and run Trivy to scan for vulnerabilities in Docker images.
     - Use GitLeaks to detect hardcoded secrets in the source code.
   - **Unit Testing**:
     - Execute test cases to validate the application.
   - **Build and Publish Docker Image**:
     - Build a Docker image using `docker build`.
     - Push the image to a container registry or upload it as an artifact.
   - **Deploy to Kubernetes**:
     - Use Terraform to provision an EKS cluster.
     - Deploy the application using Kubernetes manifests.

![alt text](All_ScreenShot/image-23.png)
![alt text](All_ScreenShot/image-24.png)

- Here is the complete [CICD- Pipeline details](https://github.com/mrbalraj007/Learning_GitHub_Action/tree/main/02.Github_Action_DevOps-Project/Working_PipeLine)

<!-- **6. Deploying to Kubernetes**
   - Use `kubectl` to apply Kubernetes manifests.
   - Verify the deployment by checking the status of pods and services. -->

### Verify the Docker Image
   ![alt text](All_ScreenShot/image-26.png)
   ![alt text](All_ScreenShot/image-27.png)
### Verify code coverage in SonarQube
   ![alt text](All_ScreenShot/image-28.png)
   ![alt text](All_ScreenShot/image-29.png)
### Verify pipeline Status
   ![alt text](All_ScreenShot/image-30.png)


### Verify the pods status from `runner VM`
```bash
ubuntu@ip-172-31-5-61:~$ kubectl get nodes
NAME                         STATUS   ROLES    AGE   VERSION
ip-10-0-3-164.ec2.internal   Ready    <none>   57m   v1.32.1-eks-5d632ec
ip-10-0-4-227.ec2.internal   Ready    <none>   58m   v1.32.1-eks-5d632ec
ubuntu@ip-172-31-5-61:~$ kubectl get all
NAME                                       READY   STATUS    RESTARTS   AGE
pod/boardgame-deployment-99f486879-q6twl   1/1     Running   0          27m
pod/boardgame-deployment-99f486879-wnkqj   1/1     Running   0          27m

NAME                     TYPE           CLUSTER-IP       EXTERNAL-IP                                                              PORT(S)        AGE
service/boardgame-ssvc   LoadBalancer   172.20.232.244   ab89f017a0d0c415a8d64e42810e63a4-389987165.us-east-1.elb.amazonaws.com   80:31107/TCP   27m
service/kubernetes       ClusterIP      172.20.0.1       <none>                                                                   443/TCP        64m

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/boardgame-deployment   2/2     2            2           27m

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/boardgame-deployment-99f486879   2         2         2       27m

```
   ![alt text](All_ScreenShot/image-31.png)
   
### Verify Application Status
   - Notedown the cluster IP address from above command and run it in browser.
   ![alt text](All_ScreenShot/image-32.png)

### <span style="color: orange;"> Setup ArgoCD </span>

- Run the following commands to verify the `Pods` and `services type` in `terraform EC2`

```sh
kubectl get pods -n argocd
```
![alt text](All_ScreenShot/image-33.png)

```sh
kubectl get svc -n argocd
```
![alt text](All_ScreenShot/image-34.png)

```sh
kubectl get pods -n prometheus
```
![alt text](All_ScreenShot/image-38.png)

```sh
kubectl get service -n prometheus
```
![alt text](All_ScreenShot/image-39.png)

<!-- - Run these commands to change the service type from ```ClusterIP``` to ```LoadBalancer```.
```sh
kubectl patch svc stable-kube-prometheus-sta-prometheus -n prometheus -p '{"spec": {"type": "LoadBalancer"}}'
kubectl patch svc stable-grafana -n prometheus -p '{"spec": {"type": "LoadBalancer"}}'
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```
Verify status now.
![image-24](https://github.com/user-attachments/assets/7d359db7-4768-4a07-9f8d-77c37a2b6df5) -->

- validate `ArgoCD` and `Grafana` access on browser.

#### <span style="color: orange;"> Access ArgoCD </span>
- run the following command to get URL of ArgoCD
```sh
ubuntu@bootstrap-svr:~$ kubectl get svc -n argocd
NAME                                      TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)                      AGE
argocd-applicationset-controller          ClusterIP      172.20.167.221   <none>                                                                    7000/TCP,8080/TCP            66m
argocd-dex-server                         ClusterIP      172.20.158.1     <none>                                                                    5556/TCP,5557/TCP,5558/TCP   66m
argocd-metrics                            ClusterIP      172.20.168.248   <none>                                                                    8082/TCP                     66m
argocd-notifications-controller-metrics   ClusterIP      172.20.67.200    <none>                                                                    9001/TCP                     66m
argocd-redis                              ClusterIP      172.20.2.127     <none>                                                                    6379/TCP                     66m
argocd-repo-server                        ClusterIP      172.20.162.115   <none>                                                                    8081/TCP,8084/TCP            66m
argocd-server                             LoadBalancer   172.20.184.179   a05d8113a21ea47e0ad6499f45767594-1028681490.us-east-1.elb.amazonaws.com   80:32509/TCP,443:32733/TCP   66m
argocd-server-metrics                     ClusterIP      172.20.152.24    <none>                                                                    8083/TCP                     66m
```
![alt text](All_ScreenShot/image-40.png)
![alt text](All_ScreenShot/image-41.png)
![alt text](All_ScreenShot/image-42.png)

- To get the login credential for argocd.
```sh
tail -n 200 /var/log/cloud-init-output.log | grep "ArgoCD Initial Password"
```
![alt text](All_ScreenShot/image-43.png)

#### <span style="color: orange;"> Configure Application in ArgoCD </span>
Once you access the ArgoCD URL and create an application
 - **Application Name**: boardgame-app
 - **Project Name**: default
 - **Sync Policy**: Automatic (Select Prune Resources and SelfHeal)
 - **Repository URL**: https://github.com/mrbalraj007/GithubAction_DevOps_Projects.git
 - **Revison**: main
 - **Path**: . (where Kubernetes files reside)
 - **cluster URL**: Select default cluster
 - **Namespace**: default

![alt text](All_ScreenShot/image-44.png)
![alt text](All_ScreenShot/image-45.png)

- Try to change something in ```deployment.yml``` (i.e Replica to `2` from 5))

![alt text](All_ScreenShot/image-47.png)

- **Verify the apps Status**
![alt text](All_ScreenShot/image-46.png)

- **Verify Pods & service status**
![alt text](All_ScreenShot/image-48.png)
![alt text](All_ScreenShot/image-54.png)

Click on the hostnames (URL details) from the service and access it in the browser.
```
ab89f017a0d0c415a8d64e42810e63a4-389987165.us-east-1.elb.amazonaws.com
```
![alt text](All_ScreenShot/image-49.png)

**Congratulations** :-) the application is working and accessible.
![alt text](All_ScreenShot/image-50.png)

### <span style="color: orange;"> Setup Monitoring using Prometheus/Grafana  </span>
- Will run the following command to get a URL of Grafana
```bash
ubuntu@bootstrap-svr:~$ tail -n 200 /var/log/cloud-init-output.log | grep "You can access Grafana at: "
You can access Grafana at: http://ab1f9e98b0d4b40dc84beed46f7c20ad-854431452.us-east-1.elb.amazonaws.com
```
![alt text](All_ScreenShot/image-51.png)

- Get Grafana 'admin' user password by running:
```bash
  kubectl --namespace prometheus get secrets stable-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo
```
![alt text](All_ScreenShot/image-52.png)

- Access Prometheus/Grafana and create a custom dashboard in Prometheus/Grafana.
  
![image-32](https://github.com/user-attachments/assets/452104dd-c859-46cd-909a-c53345055cab)
![image-33](https://github.com/user-attachments/assets/5f96e4af-4b06-49f8-9eae-a22b1c60ba04)
![image-34](https://github.com/user-attachments/assets/b54fcf5d-98fe-4196-8c6d-d66b154af843)
![image-35](https://github.com/user-attachments/assets/c0b83f08-4fdc-4f9b-b1cf-8d562918b806)

#### Dashboard in Grafana
![image-36](https://github.com/user-attachments/assets/ec873ad5-ed0c-43b4-9d85-2a08e16a5839)

---

## Setup Notification in Slack

### 1. Create a channel for Slack

1. Go to your Slack workspace and create a new channel
   - Visit: https://api.slack.com/apps
   - Click "Create New channel" > "From scratch"
   ![alt text](All_ScreenShot/image-67.png)
   ![alt text](All_ScreenShot/image-68.png)
   - Click on `Blank Channel` and next
   ![alt text](All_ScreenShot/image-69.png)
   - Name your channel (e.g., "GitHub Actions Notifier") and select private and create it.
   ![alt text](All_ScreenShot/image-70.png)
   - It will ask for adding email address and skip for now.   
   ![alt text](All_ScreenShot/image-71.png)

### 2. Create a app for Slack

1. Go to your Slack workspace and create a new app (or use an existing one):
   - Visit: https://api.slack.com/apps
   - Click "Create New App" > "From scratch"
   ![alt text](All_ScreenShot/image-72.png)
   ![alt text](All_ScreenShot/image-73.png)
   - Name your app (e.g., "GitHub Actions Notifier")
   - Select your workspace i.e ("Jenkins_Notification")
   ![alt text](All_ScreenShot/image-74.png)
   
### 3. Set Slack App Permissions
   - In your app dashboard:
   - Go to OAuth & Permissions.
      ![alt text](All_ScreenShot/image-75.png)
   - Scroll to Scopes:
      - Under Bot Token Scopes, add:
         - chat:write → Allows the bot to post messages.
         - chat:write.public → (Optional) Allows posting in public channels without being invited.
         - Files:write → To be able to write to the slack channel
         ![alt text](All_ScreenShot/image-76.png)
        
     
### 4. Configure Slack Incoming Webhook

1. Set up Incoming Webhooks:
   - Under "Add features and functionality", select "Incoming Webhooks"
   - Toggle "Activate Incoming Webhooks" to On
   - Click "Add New Webhook to Workspace"
   - Choose the "aws-cost-notification" channel
   - Copy the Webhook URL that is generated
   - Go to `https://api.slack.com/apps`
    ![alt text](All_ScreenShot/image-77.png)
    ![alt text](All_ScreenShot/image-78.png)
    ![alt text](All_ScreenShot/image-79.png)
    ![alt text](All_ScreenShot/image-80.png)
    ![alt text](All_ScreenShot/image-66.png)
    ![alt text](All_ScreenShot/image-81.png)
    ![alt text](All_ScreenShot/image-82.png)
   - Invite the Bot in Slack Channel
   /invite @AWS Cost Notifier and click on `send`
   ![alt text](All_ScreenShot/image-83.png)


### 5. Add Webhook URL to GitHub Repository Secrets

1. In your GitHub repository, go to "Settings" > "Secrets" > "Actions"
2. Select "secret" ,Name: `SLACK_WEBHOOK_URL`
3. Value: Paste the webhook URL from the previous step
4. Click "Add secret"

### 6. Workflow Execution

The workflow will run:
- When code is pushed to the main branch
- When a pull request is made to the main branch
- Manually via the "Actions" tab in GitHub

### Customization in Slack webhook

You can customize the notification message by modifying the `custom_payload` in the `.github/workflows/hello-world-slack.yml` file.


The `SLACK_WEBHOOK_URL` in your workflow file refers to a webhook URL that needs to be stored as a GitHub Actions secret. This is not an actual URL in the file, but a reference to a secret value.

To set up a Slack webhook URL:

1. Go to your Slack workspace and create an incoming webhook:
   - Visit https://api.slack.com/apps
   - Create a new app or use an existing one
   - Enable "Incoming Webhooks"
   - Add a new webhook to a specific channel
   - Copy the webhook URL provided (looks like: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX)

2. Add this webhook URL as a GitHub repository secret:
   - Go to your GitHub repository
   - Navigate to Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `SLACK_WEBHOOK_URL`
   - Value: paste the webhook URL from Slack
   - Click "Add secret"

- Your workflow will then use this secret value when sending notifications to Slack. The actual URL is kept secure and not visible in your workflow file. 

- Once the pipeline is executed successfully, then get the below notification in Slack. This notification will provide details about the execution status, including any errors or warnings that may have occurred during the process. Additionally, it will outline the next steps to take if further action is required.
   ![alt text](All_ScreenShot/image-65.png)

## Final Status of Pipeline
![alt text](All_ScreenShot/image-63.png)
![alt text](All_ScreenShot/image-64.png)


## <span style="color: Yellow;"> Environment Cleanup:
- Following resouces are created as part of this project.   
   ![alt text](All_ScreenShot/image-53.png)

### <span style="color: cyan;"> To delete deployment:
- I've created a `Github Action` to destroy the Kubernetes `deployment` and `services`.
   

  - __Delete all deployment/Service__: 
    - In github action, and click on the second pipeline to delete the deployment and service.
    ![alt text](All_ScreenShot/image-56.png)
    ![alt text](All_ScreenShot/image-57.png)

    - Here is the complete [CICD- Pipeline to destroy Deployment and Services](https://github.com/mrbalraj007/Learning_GitHub_Action/tree/main/02.Github_Action_DevOps-Project/Working_PipeLine)

### <span style="color: cyan;"> To delete ```AWS EKS cluster```
   -   Login into the `Terraform EC2 `instance and change the directory to /`k8s_setup_file`, and run the following command to delete the cluster.
       - ```sh
         sudo su - ubuntu
         cd /k8s_setup_file
         sudo terraform destroy --auto-approve
         ```
#### **Troubleshooting:** 
- I am getting below error message while running the `Terraform destroy`.
   ![alt text](All_ScreenShot/image-35.png)


##### **Fix/Solution:**

- I noticed that permission is set to root for terraform dirctory. we have to take ownership first and then try to delete it.
![alt text](All_ScreenShot/image-36.png)
- Run the following command to take ownership
   ```sh
   pip install slack-sdk
   ```
- I was still getting error message while runing the desrtoy
   ![alt text](All_ScreenShot/image-37.png)
- I ran the following command again for entire terraform folder.
   ```sh
   sudo chown -R ubuntu:ubuntu /home/ubuntu/k8s_setup_file/terraform*
   ```
- Rerun the destroy command and this time it works :-)


###  <span style="color: cyan;"> To delete the ```Virtual machine```.
Go to folder *<span style="color: cyan;">"02.Github_Action_DevOps-Project/Terraform_Code_Infra_setup"</span>* and run the terraform command.
   - `00.Code_IAC-github-repo`
   - `01.Code_IAC_Selfhosted-Runner-and-Trivy`
   -` 02.Code_IAC_SonarQube`
   - `03.Code_IAC_Terraform_box`
      
      ```sh
      Terraform destroy --auto-approve
     ```
> 💡 **Note:** 
>> You must use this command from `each folder` in order to destroy the entire infrastructure.

#### **Troubleshooting:** 
- I am getting below error message while running the `Terraform destroy`.
   ![alt text](All_ScreenShot/image-58.png)

##### **Fix/Solution:**
- I need to delete the all `Load balancer`
![alt text](All_ScreenShot/image-59.png)
![alt text](All_ScreenShot/image-60.png)

- Again, I am getting the below error message and noticed that the security group is stopping me from deleting it. So, when I delete the `VPC` and try to run the destroy command again. This time it works.

   ![alt text](All_ScreenShot/image-61.png)
   ![alt text](All_ScreenShot/image-62.png)

---

### **Why Use This Project**
- **Automation**: Reduces manual effort in building, testing, and deploying applications.
- **Security**: Ensures code and container security through automated scans.
- **Scalability**: Deploys applications to scalable Kubernetes clusters.
- **Best Practices**: Demonstrates industry-standard CI/CD practices.
---

## Project Challenges

#### Technical Complexity
   - Coordinating multiple tools and technologies in a cohesive pipeline
   - Ensuring proper authentication between services (GitHub, Docker Hub, Kubernetes)
   - Managing Kubernetes RBAC for secure but sufficient permissions
   - Configuring Prometheus targets with proper scraping intervals

#### Integration Points
   - Bridging self-hosted runner with GitHub Actions ecosystem
   - Connecting pipeline stages with appropriate artifact handoffs
   - Ensuring monitoring tools receive metrics from all components
   - Managing secrets securely across multiple services

#### Infrastructure Management
   - Provisioning right-sized VMs for each component
   - Configuring network security for appropriate access
   - Ensuring high availability for critical components
   - Managing resource consumption across the stack

## Project Benefits

#### Development Workflow
   - Automated quality gates prevent problematic code from reaching production
   - Developers receive immediate feedback on code quality and security
   - Clear visibility of deployment status and application health
   - Reduced manual intervention in deployment processes

#### Operational Excellence
   - Real-time monitoring of application and infrastructure
   - Early detection of performance degradation or failures
   - Ability to correlate infrastructure metrics with application behavior
   - Historical metrics for capacity planning and optimization

#### Security Enhancements
   - Vulnerability scanning at multiple levels (code, container)
   - Principle of least privilege through RBAC implementation
   - Secure secret management across the pipeline
   - Audit trail of deployments and changes

#### Business Value
   - Faster time-to-market for new features and bug fixes
   - Improved application reliability and performance
   - Reduced operational overhead through automation
   - Better resource utilization through monitoring insights

## Conclusion

AWS cost optimization requires consistent monitoring and analysis of spending patterns. This solution provides an automated approach to cost reporting that enables teams to quickly identify unusual spending patterns or resource utilization. By implementing daily cost reports delivered directly to Slack, organizations can foster a cost-conscious culture and respond rapidly to unexpected expenses.

The combination of AWS Cost CLA, Slack integration, and scheduled reporting creates a seamless system that reduces the manual effort required for cost monitoring while increasing visibility across the organization. This approach transforms cost optimization from a reactive, month-end activity into a proactive, daily practice that can significantly reduce cloud spending over time.



**Ref Link:**
- [YouTube Link](https://www.youtube.com/watch?v=kBs59NlNxys&t=783s)
- [Download NodeJs](https://nodejs.org/en/download)
- [Repo Link](https://github.com/kamranahmedse/aws-cost-cli?tab=readme-ov-file)
- [My Repo](https://github.com/mrbalraj007/aws-cost-cli)


