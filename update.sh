rm -rf site/
python legacy_generate.py
ssh -T kuao << EOF > /dev/null
rm -rf /var/www/kuaochella.com/scavenger_hunt/
EOF
scp -r site/scavenger_hunt/ kuao:/var/www/kuaochella.com/
