
# AI Ebay Listing Tool

A tool that takes your images and automatically creates a CSV file of listings to be uploaded to eBay Seller Hub. Create hundreds of listings in just a few minutes!


## Installation

You will need the following to use this tool:

- [Python 3.10](https://www.python.org/downloads/)
- [OpenAI](https://platform.openai.com/api-keys) API Key (Requires Tier 1 and ChatGPT-4o access)
- [AWS](https://aws.amazon.com/console/) (You will need to set up a public S3 bucket for image hosting)
- eBay Seller Account

Install the required packages by running the command:

`pip install -r requirements.txt`

## Environment Variables

You will need to add the following environment variables to a `.env` file in the root directory of the tool:

`OPENAI_API_KEY` - This will authorize the program to make API calls to ChatGPT on your behalf. Ensure your account is sufficiently credited.

`AWS_BUCKET_NAME` `AWS_REGION_NAME` - The AWS S3 bucket details for where your images will be uploaded to.

`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` - These will give the program authorization to upload images to your AWS S3 bucket.
## How To Use

Step 1: Create a folder `images` in the root directory of the tool. 

Step 2: Fill the `images` folder with folders containing the items you wish to list. For example your directory may look like this:

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

Step 3: Navigate to the root directory of the tool and run the `app.py` file.  The program will go through each directory in `images`, and create a listing for the csv file, outputting its progress as it goes.

```
Progress:  0/3 (0%)
Uploaded .../images/1/IMG_8054.JPG to .../1/IMG_8054.JPG.
Uploaded .../images/1/IMG_8055.JPG to .../1/IMG_8055.JPG.
Uploaded .../images/1/IMG_8056.JPG to .../1/IMG_8056.JPG.
Uploaded .../images/1/IMG_8057.JPG to .../1/IMG_8057.JPG.
Uploaded .../images/1/IMG_8058.JPG to .../1/IMG_8058.JPG.
ChatGPT output: Craghoppers XL Men's Check Shirt Long Sleeve Casual Top,57990,Brand, Craghoppers, Size, XL, Type, Shirt, Colour, Multi, Department, Men, Fit, Regular, Sleeve Length, Long Sleeve
Progress:  1/3 (33%)
Uploaded .../images/2/IMG_8096.JPG to .../2/IMG_8096.JPG.
Uploaded .../images/2/IMG_8097.JPG to .../2/IMG_8097.JPG.
Uploaded .../images/2/IMG_8098.JPG to .../2/IMG_8098.JPG.
Uploaded .../images/2/IMG_8099.JPG to .../2/IMG_8099.JPG.
Uploaded .../images/2/IMG_8100.JPG to .../2/IMG_8100.JPG.
ChatGPT output: M&S Floral Pink Top Size 14 Long Sleeve Women's,53159,Brand,M&S,Size,14,Type,Top,Colour,Pink,Department,Women,Sleeve Length,Long
Progress:  2/3 (67%)
Uploaded .../images/3/IMG_8025.JPG to .../3/IMG_8025.JPG.
Uploaded .../images/3/IMG_8026.JPG to .../3/IMG_8026.JPG.
Uploaded .../images/3/IMG_8027.JPG to .../3/IMG_8027.JPG.
Uploaded .../images/3/IMG_8028.JPG to .../3/IMG_8028.JPG.
Uploaded .../images/3/IMG_8029.JPG to .../3/IMG_8029.JPG.
Uploaded .../images/3/IMG_8030.JPG to .../3/IMG_8030.JPG.
ChatGPT output: Vintage Heritage Scotland Black Lace Up Shirt XL Men,185097,Style,Vintage,Material,Cotton,Main Colour,Black,Gender,Men,Size,XL,Brand,Heritage
Progress: 3/3 (100%)
Failed jobs: []
Total elapsed time: 53.6508 seconds
```

Step 4: If the tool succeeds, it will produce an `out.csv` file in the root directory. This is what you will upload to the [eBay Seller Hub Reports](https://www.ebay.co.uk/sh/reports/uploads) page. You will be notified of the directories of any failed listings.

## Authors

- [Samir Hasan Chowdhury](https://www.github.com/SamirHC)

