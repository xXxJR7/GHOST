# IT_S6

### Local Deploy
- `sudo apt update && sudo apt upgrade -y`

- `sudo apt install --no-install-recommends -y curl git libffi-dev libjpeg-dev libwebp-dev python3-lxml python3-psycopg2 libpq-dev libcurl4-openssl-dev libxml2-dev libxslt1-dev python3-pip python3-sqlalchemy openssl wget python3 python3-dev libreadline-dev libyaml-dev gcc zlib1g ffmpeg libssl-dev libgconf-2-4 libxi6 unzip libopus0 libopus-dev python3-venv libmagickwand-dev pv tree mediainfo nano`

- Clone the repository:    
`git clone https://github.com/sa3ed266it/ITALIA.git`
- Go to the cloned folder:    
`cd ITALIA`
- Create a screen:      
`screen -S ITALIA`
- Create .env file:      
- `mv .env.sample .env`
- Open .env file:      
- `nano .env`
- Fill Your Info And Press Ctrl + s , Ctrl + x
- Create a virtual env:      
`virtualenv venv`
- Activate the virtual environment you've just created:      
`source venv/bin/activate`
- Install the requirements:      
`pip3 install -U -r requirements.txt`
- Run the bot:      
`python -B -m IT_S6`
