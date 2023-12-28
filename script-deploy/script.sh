if [ ! -f ~/.ssh/google_compute_engine ]; then
  ssh-keygen -t rsa -f ~/.ssh/google_compute_engine -N ''
fi

gcloud compute config-ssh --quiet

gcloud compute ssh cultucat-back --zone=us-central1-a --tunnel-through-iap --project=cultucat-405114 << EOF

pwd
whoami
sudo -i -u emanuel.cuevas03
cd backend/
source myenv/bin/activate
git pull
sudo service apache2 restart

EOF