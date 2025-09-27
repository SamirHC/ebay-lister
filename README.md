
# AI Ebay Listing Tool

A tool that takes your images and automatically creates a CSV file of listings to be uploaded to eBay Seller Hub. Create hundreds of listings in just a few minutes!
This tool was commissioned by Anas Benzeggouta, an eBay clothing merchant.

## Installation

You will need the following to use this tool:

- [Python 3.10](https://www.python.org/downloads/)
- [OpenAI](https://platform.openai.com/api-keys) API Key (Requires Tier 1 and model access)
- [AWS](https://aws.amazon.com/console/) (You will need to set up a public S3 bucket for image hosting)
- eBay Seller Account

Install the required packages by running the command from the `ebay-lister` root directory:

`pip install -e .`

It is good practice to install such dependencies in a virtual environment.

## Environment Variables

You will need to add the following environment variables to a `.env` file in the root directory of the tool:

`OPENAI_API_KEY` - This will authorize the program to make API calls to ChatGPT on your behalf. Ensure your account is sufficiently credited.

`AWS_BUCKET_NAME` `AWS_REGION_NAME` - The AWS S3 bucket details for where your images will be uploaded to.

`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` - These will give the program authorization to upload images to your AWS S3 bucket.

## How To Use

Step 1: Create a folder `images` in the root directory of the tool. 

Step 2: Fill the `images` folder with folders containing the images of the items you wish to list. For example your directory may look like this:

```
images/
├── item1/
|   ├── 1.png
|   ├── 2.png
|   ├── 3.png
├── item2/
|   ├── 4.png
|   ├── 5.png
|   ├── 6.png
|
...
```

Step 3: Navigate to the root directory of the tool and run the `main.py` file.  The program will go through each directory in `images`, and create a listing for the csv file, outputting its progress as it goes.

```
================================================================================
Starting Listing Tool...

Started uploading images.
Uploaded .../ebay-lister/images/1/IMG_8054.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/1%2FIMG_8054.JPG.
Uploaded .../ebay-lister/images/2/IMG_8096.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/2%2FIMG_8096.JPG.
Uploaded .../ebay-lister/images/1/IMG_8055.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/1%2FIMG_8055.JPG.
Uploaded .../ebay-lister/images/2/IMG_8097.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/2%2FIMG_8097.JPG.
Uploaded .../ebay-lister/images/1/IMG_8056.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/1%2FIMG_8056.JPG.
Uploaded .../ebay-lister/images/2/IMG_8098.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/2%2FIMG_8098.JPG.
Uploaded .../ebay-lister/images/1/IMG_8057.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/1%2FIMG_8057.JPG.
Uploaded .../ebay-lister/images/2/IMG_8099.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/2%2FIMG_8099.JPG.
Uploaded .../ebay-lister/images/1/IMG_8058.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/1%2FIMG_8058.JPG.
Uploaded .../ebay-lister/images/2/IMG_8100.JPG to https://BUCKETNAME.s3.REGION.amazonaws.com/2%2FIMG_8100.JPG.
Finished uploading images.

ChatGPT output: {
  "title": "M&S Collection womens pink floral blouse size 14 long sleeve top",
  "category_id": 53159,
  "item_specifics": {
    "Brand": "M&S Collection",
    "Size": "14",
    "Type": "Blouse",
    "Colour": "Pink",
    "Department": "Women",
    "Sleeve Length": "Long Sleeve"
  }
}
ChatGPT output: {
  "title": "Craghoppers mens brown checked casual shirt XL regular long sleeve",
  "category_id": 57990,
  "item_specifics": {
    "Brand": "Craghoppers",
    "Size": "XL",
    "Type": "Casual Shirt",
    "Colour": "Brown",
    "Department": "Men",
    "Fit": "Regular",
    "Sleeve Length": "Long Sleeve"
  }
}

Progress: 2/2 (100%)
Failed jobs: []

Total elapsed time: 40.5166 seconds.
```

Step 4: On success, a CSV file is produced in the `out` directory. This is what you will upload to the [eBay Seller Hub Reports](https://www.ebay.co.uk/sh/reports/uploads) page.

You will be notified of the directories of any failed listings. Logs are stored in the `out/log` directory.


## Authors
- [Samir Hasan Chowdhury](https://www.github.com/SamirHC)

