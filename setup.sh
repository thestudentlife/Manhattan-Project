#!/usr/bin/env bash

cwd=$(pwd)
echo $(pip3 --version)
pip3 install virtualenv
if [ ! -d "$cwd/ve" ]; then
    virtualenv -p $(which python3) -q $cwd/ve
    echo "Virtualenv created."
fi

source $cwd/ve/bin/activate

if [ ! -f "$cwd/ve/updated" -o $cwd/requirements.txt -nt $cwd/ve/updated ]; then
    pip3 install -r $cwd/requirements.txt
    touch $cwd/ve/updated
    echo "Requirements for TSL installed"
fi

rm -rf db.sqlite3;
touch db.sqlite3;
cd workflow && mkdir migrations;
cd ..;
rm -rf workflow/migrations/*;
touch workflow/migrations/__init__.py;
rm -rf mainsite/migrations/*;
cd mainsite && mkdir migrations;
touch mainsite/migrations/__init__.py;
cd ..;
python3 manage.py makemigrations;
mkdir website/media/;
mkdir website/media/photo/;
mkdir website/media/thumbs/;
rm -rf website/media/photo/*;
rm -rf website/media/thumbs/*;
cp website/fixtures/goldengatebridge.jpg website/media/photo/goldengatebridge.jpg;
cp website/fixtures/pearlharbor.jpg website/media/photo/pearlharbor.jpg;
cp website/fixtures/ramune.jpg website/media/photo/ramune.jpg;
cp website/fixtures/goldengatebridge_thumbnail.jpg website/media/thumbs/goldengatebridge_thumbnail.jpg;
cp website/fixtures/pearlharbor_thumbnail.jpg website/media/thumbs/pearlharbor_thumbnail.jpg;
cp website/fixtures/ramune_thumbnail.jpg website/media/thumbs/ramune_thumbnail.jpg;
python3 manage.py migrate;
python3 manage.py loaddata website/fixtures/initial_data.json;
python3 manage.py collectstatic --noinput;
python3 manage.py runserver;