# Automated-Data-Preprocessing

- An End-to-End Application build using Python and React to automate the data preprocessing task for Machine Learning model building purpose.
- It can handle structured dataset (Continuous and Categorical attributes) as well as Compressed Image Dataset.
- For <b>structured data</b>, it identifies the type of attribute (continuous or categorical) and performs respective actions such as
  - Handling Missing Values using MICE algorithm
  - Outlier detection and removal
  - Normalization/Scaling down using Robust Scaler
  - Encoding
  - Finally, it combines all the processed attributes and combines it to form a new dataset and gives it back to user

</br>

- For <b>Image dataset</b>, following actions are performed
  - Conversion to numpy array
  - Reshaped to 224 x 224
  - Converted to RGB format
  - Converting complete array into one dimensional array
  - Compressed into a file and sent back to user

#### Sample dataset can be found in the repository

### Steps to run the application:
> 1. Clone the repository : git clone https://github.com/rohangawhade/Automated-Data-Preprocessing.git
> 2. Go to `backend` directory and install packages: `pip install -r .\requirements.txt` . Then update the location on `api.py` lines 17 and 18.
> 3. Go to `frontend` directory and install modules: `yarn add`
> 4. Create .env file in backend and frontend directory and add firebase api keys in it.
> 5. Now run the following command `backend: python api.py` and `frontend: yarn start`

</br>

### Demo
https://user-images.githubusercontent.com/49246157/177576800-555f2d85-9362-493d-9127-48efe66aee0d.mp4

