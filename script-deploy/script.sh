gcloud compute ssh cultucat-back --zone=us-central1-a --ssh-key-file ${{ secrets.GCP_SSH_PRIVATE_KEY }} --tunnel-through-iap --project=cultucat-405114
sudo -i -u emanuel.cuevas03
cd backend/
source myenv/bin/activate
git pull
sudo service apache2 restart