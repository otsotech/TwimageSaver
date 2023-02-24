# TwimageSaver

A Python script that downloads images from a Twitter user's timeline and saves them to a local directory.
## Installation

1. Clone the repository:

```
git clone https://github.com/otsotech/TwimageSaver.git
```
2. Install the required Python packages:
```
pip install -r requirements.txt
```
## Usage

1. Edit the file named api_credentials.json with your Twitter API credentials in the following format:

```
{
    "api_key": "your_api_key",
    "api_secret": "your_api_secret",
    "access_token": "your_access_token",
    "access_token_secret": "your_access_token_secret"
}
```

2. Run the script:
```
python TwimageSaver.py
```

3. Enter a Twitter username and the number of images to download (leave blank for all).

4. The script will create a directory named username_images (where username is the Twitter username entered) and download the images to that directory.

Note: This script only works for public Twitter accounts.
