gcloud compute instances create frankenstein-ai-server \
    --machine-type n1-highmem-8 --zone us-central1-f \
     --accelerator type=nvidia-tesla-k80,count=1 --boot-disk-size=100 \
    --image ubuntu-1604-lts --image-project ubuntu-os-cloud \
    --maintenance-policy TERMINATE --restart-on-failure \
    --metadata startup-script='#!/bin/bash
    echo "Checking for CUDA and installing."
    # Check for CUDA and try to install.
    if ! dpkg-query -W cuda-8-0; then
      curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
      dpkg -i ./cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
      apt-get update
      apt-get install cuda-8-0 -y
    fi'
