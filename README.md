
# NCC AUTO ROI     
The program was created with the support of the National Cancer Center.     
The program was written on the advice of Yuh-Seog Jung, Jungirl Seok, medical doctor.     

The GNU General Public License(GPL)     
Version 2, June 1991     
Copyright (C) 1989, 1991 Free Software Foundation, Inc.

This is a preprocessing program to help AI.     
Split the slide CT medical images using the THRESHOLD.     
It makes it easy to make 3D images.     

![123](https://user-images.githubusercontent.com/19296155/106537490-c6580600-653d-11eb-8216-f28bf8baa4b3.png)     

step 1     
512 * 512 similar to below     
Continuous CT Image(dicom file) is required.    Creative Commons license CT image    
![Phaeochromozytoma_CT](https://user-images.githubusercontent.com/19296155/106423123-28176200-64a3-11eb-8b92-396efc1ded24.jpg)

step 2    
Install the Python package listed below.     
latest installation of pycharm     
After installing python 3.7     
pip upgrade for python3.7     
sudo python3.7 -m pip install --upgrade pip setuptools wheel     
sudo pip3 install opencv-python     
sudo pip3 install pillow     
sudo pip install pypng     
import pydicom -> install pie true red underscore click install     

step 3     
WORK_ROI project folder     
Download to the appropriate location.     

![555](https://user-images.githubusercontent.com/19296155/106425611-74fd3780-64a7-11eb-91e7-7fd586965295.png) 

step 4     
Run main.py

The following tasks:    
Run the application with tools such as PiCham.     
It is to look at the screen as below.     
![111](https://user-images.githubusercontent.com/19296155/106424051-e4bdf300-64a4-11eb-8a1f-6ce15a636a6c.png)   

step 5     
CT DICOM file -> jpg change
![777](https://user-images.githubusercontent.com/19296155/106426809-97905000-64a9-11eb-926c-1f794589c34d.png)

step 6     
The generated folder displays the date and time.     
Select the jpg file converted.     
The image is displayed in the left table view and on the screen.     
![888](https://user-images.githubusercontent.com/19296155/106428474-62d1c800-64ac-11eb-872d-41312901e93d.png)

step 7     
ROI & Threshold     
![5555555](https://user-images.githubusercontent.com/19296155/106532803-39f51580-6534-11eb-9b55-34c795cca4b3.png)   

Press the Property button on the left.     
We've got more options for ROI.     
I can handle it.    
![99999](https://user-images.githubusercontent.com/19296155/106533067-c43d7980-6534-11eb-8c48-5a9c599dfb98.png)

step 8     
When ROI selection is complete,     
Press the algorithm button at the top of the center.     
Extract the mask.     
![34634463](https://user-images.githubusercontent.com/19296155/106534033-8b9e9f80-6536-11eb-96d5-5d0d03112308.png)     

step 9     
Active Export to Green     
When the button is pressed, the mask image is...      
Converts to binary text data.     
![573456346346](https://user-images.githubusercontent.com/19296155/106535359-6c554180-6539-11eb-82c3-a9a80ac8e5d1.png)

step 10     
Press the Export button, and then click     
When I refresh it,     
There is a folder as below.     
The binary data for the selected mask is generated.     

The image restore code for binary data is also located in the path below.     
LAB -> common -> util -> img_text.py
![647456452](https://user-images.githubusercontent.com/19296155/106534896-614de180-6538-11eb-9209-25576d49132b.png)     

[![HitCount](http://hits.dwyl.com/sungminYoon/NCC.svg)](http://hits.dwyl.com/sungminYoon/NCC)






