
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
2025-09-26 18:31:48,961 - INFO - Found credentials in environment variables.
2025-09-26 18:31:49,067 - INFO - ================================================================================
2025-09-26 18:31:49,068 - INFO - Starting Listing Tool...
2025-09-26 18:31:49,068 - INFO - 
2025-09-26 18:31:49,068 - INFO - Started uploading images.
...
2025-09-26 18:31:49,381 - INFO - Uploaded .../ebay-lister/images/2/IMG_8096.JPG to https://<BUCKET_NAME>.s3.eu-west-2.amazonaws.com/2%2FIMG_8096.JPG.
2025-09-26 18:31:49,393 - INFO - Uploaded .../ebay-lister/images/1/IMG_8054.JPG to https://<BUCKET_NAME>.s3.eu-west-2.amazonaws.com/1%2FIMG_8054.JPG.
...
2025-09-26 18:31:50,094 - INFO - Finished uploading images.

2025-09-26 18:32:12,206 - INFO - HTTP Request: POST https://api.openai.com/v1/responses "HTTP/1.1 200 OK"
2025-09-26 18:32:12,257 - INFO - ChatGPT output: M&S Collection womens pink floral blouse size 14 long sleeve top, 53159, Brand, M&S Collection, Size, 14, Type, Blouse, Colour, Pink, Department, Women, Sleeve Length, Long Sleeve
2025-09-26 18:32:36,266 - INFO - HTTP Request: POST https://api.openai.com/v1/responses "HTTP/1.1 200 OK"
2025-09-26 18:32:36,268 - INFO - ChatGPT output: Craghoppers mens casual shirt XL brown checked regular fit long sleeve, 57990, Brand, Craghoppers, Size, XL, Type, Casual Shirt, Colour, Brown, Department, Men, Fit, Regular, Sleeve Length, Long Sleeve
2025-09-26 18:32:36,268 - INFO - 
2025-09-26 18:32:36,268 - INFO - Progress: 2/2 (100%)
2025-09-26 18:32:36,268 - INFO - Failed jobs: []
2025-09-26 18:32:36,268 - INFO - 
2025-09-26 18:32:36,268 - INFO - Total elapsed time: 47.2008 seconds.
```

Step 4: If the tool succeeds, it will produce a CSV file in the `out` directory. This is what you will upload to the [eBay Seller Hub Reports](https://www.ebay.co.uk/sh/reports/uploads) page.

You will be notified of the directories of any failed listings. Logs are stored in the `out/log` directory.


## Authors
- [Samir Hasan Chowdhury](https://www.github.com/SamirHC)

