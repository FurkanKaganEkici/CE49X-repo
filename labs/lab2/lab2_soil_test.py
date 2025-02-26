{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "c19ad551-1476-4129-9a37-f2324c6db811",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Statistics for soil_ph:\n",
      "Minimum: 6.00\n",
      "Maximum: 6.90\n",
      "Mean: 6.45\n",
      "Median: 6.45\n",
      "Standard Deviation: 0.29\n",
      "-\n",
      "Statistics for nitrogen:\n",
      "Minimum: 18.00\n",
      "Maximum: 26.00\n",
      "Mean: 22.02\n",
      "Median: 22.00\n",
      "Standard Deviation: 2.81\n",
      "-\n",
      "Statistics for phosphorus:\n",
      "Minimum: 12.00\n",
      "Maximum: 18.00\n",
      "Mean: 14.97\n",
      "Median: 15.00\n",
      "Standard Deviation: 2.39\n",
      "-\n",
      "Statistics for moisture:\n",
      "Minimum: 28.00\n",
      "Maximum: 34.00\n",
      "Mean: 30.97\n",
      "Median: 30.97\n",
      "Standard Deviation: 2.22\n",
      "-\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "def load_data(file_path): #it loads the data \n",
    "    \n",
    "    try:\n",
    "        data = pd.read_csv(file_path) #read the data \n",
    "        return data\n",
    "    except FileNotFoundError:   #incase if it gives error finding the file \n",
    "        print(\"Error: File not found.\")\n",
    "        return None\n",
    "\n",
    "def clean_data(data):  #this function cleans the dataset by handling missing values and optionally removing outliers\n",
    "    \n",
    "    if data is None:\n",
    "        return None\n",
    "    \n",
    "   \n",
    "    data.fillna(data.mean(), inplace=True)  # Fills missing values with column mean\n",
    "    \n",
    "    \n",
    "    for column in data.select_dtypes(include=[np.number]).columns:  #This loop removes outliers in numeric columns \n",
    "        mean_col = data[column].mean()\n",
    "        std_col = data[column].std()\n",
    "        data = data[(data[column] >= mean_col - 3 * std_col) & (data[column] <= mean_col + 3 * std_col)]\n",
    "    \n",
    "    return data\n",
    "\n",
    "def compute_statistics(data):  #function for computing min max mean median and std dev\n",
    "    \n",
    "    numeric_columns = [col for col in data.select_dtypes(include=[np.number]).columns if col != 'sample_id'] #sample id column is not included output\n",
    "    \n",
    "    for column in numeric_columns:  #this loop evaluate the statistics\n",
    "        stats = {\n",
    "            \"Minimum\": data[column].min(),\n",
    "            \"Maximum\": data[column].max(),\n",
    "            \"Mean\": data[column].mean(),\n",
    "            \"Median\": data[column].median(),\n",
    "            \"Standard Deviation\": data[column].std()\n",
    "        }\n",
    "        \n",
    "        print(f\"Statistics for {column}:\") #getting the output\n",
    "        for key, value in stats.items():\n",
    "            print(f\"{key}: {value:.2f}\")\n",
    "        print(\"-\")\n",
    "\n",
    "if __name__ == \"__main__\":  #defining file path\n",
    "    file_path = r\"C:\\Users\\furka\\OneDrive\\Masaüstü\\lab\\CE49X-repo\\datasets\\soil_test.csv\"\n",
    "    data = load_data(file_path)\n",
    "    \n",
    "    if data is not None:\n",
    "        data = clean_data(data)\n",
    "        compute_statistics(data)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "804c88c2-c404-4bec-b1d9-dd8a3745b17a",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d2c3a968-fcd6-4e02-b5b3-4b54531c9576",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (Ce49X)",
   "language": "python",
   "name": "ce49x"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
