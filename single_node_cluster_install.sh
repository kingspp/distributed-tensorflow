#!/usr/bin/env bash


NODE_IP=172.22.22.22
CLUSTER_NAME=dist_tf
NODE_MEMORY_SIZE=2048
PROXY_PORT=8080


echo 'Welcome to Kubernetes Single Node Cluster Setup'
echo 'Removing Previous Vagrant Setup . . .' && vagrant destroy
rm -rf .vagrant/
echo 'Removing Previous SSL Certificates . . .' && rm -rf ssl/
sed 's/.*NODE_IP =.*/NODE_IP = "'$NODE_IP'"/' VagrantFile >/dev/null 2>&1
sed 's/.*NODE_MEMORY_SIZE =.*/NODE_MEMORY_SIZE = '$NODE_MEMORY_SIZE'/' VagrantFile >/dev/null 2>&1
echo 'Initializing Vagrant . . .' && vagrant box update
echo 'Starting Vagrant . . .' && vagrant up
echo 'Generating Kubernetes Configuration . . .'
kubectl config set-cluster ${CLUSTER_NAME}-single-cluster --server=https://${NODE_IP}:443 --certificate-authority=${PWD}/ssl/ca.pem
kubectl config set-credentials ${CLUSTER_NAME}-single-admin --certificate-authority=${PWD}/ssl/ca.pem --client-key=${PWD}/ssl/admin-key.pem --client-certificate=${PWD}/ssl/admin.pem
kubectl config set-context ${CLUSTER_NAME}-single --cluster=${CLUSTER_NAME}-single-cluster --user=${CLUSTER_NAME}-single-admin
echo 'Changing Kubernates Context . . .' && kubectl config use-context ${CLUSTER_NAME}-single
python3 monitor.py
echo 'Waiting for Kubernetes Services . . .' && sleep 10
echo 'Querying Kubernetes Nodes' && kubectl get nodes
echo 'Changing Proxy' && kubectl proxy --port=$PROXY_PORT &
echo 'Quering Kubernetes Cluster Info' && kubectl cluster-info
echo 'Kubernetes is UP and RUNNING!!!'
echo ' _______________________________________________________________________________________________________'
echo '| Dashboard IP: http://localhost:8080/api/v1/proxy/namespaces/kube-system/services/kubernetes-dashboard |'
echo ' _______________________________________________________________________________________________________'
python -c "import webbrowser; webbrowser.open(\"http://localhost:8080/api/v1/proxy/namespaces/kube-system/services/kubernetes-dashboard\")"
python -m SimpleHTTPServer 8121


