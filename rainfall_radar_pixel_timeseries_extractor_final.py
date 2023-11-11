# -*- coding: utf-8 -*-
"""
#Code by Kaushal Gnyawali and Saksham Arora
"""

#Keep this file in this same diectory as the images
#First printing all filenames and maunnly 

# Importing Image from PIL package
# import the modules
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image



from image_scraper import scraper

website_url = str(input('Paste the website URL: '))

coo_x= int(input ("Type the x coordinate: "))
coo_y= int(input("Type the y coordinate: "))

err = int(input("Enter the range you want to look around: "))


scraper(website_url)

# gets the current working directory where the python file is stored
file = 'images/'

# Store the image file names in a list as long as they are jpgs
images = [f for f in os.listdir(file) if os.path.splitext(f)[-1] == '.gif']


for coordinate_x in range(coo_x-err,coo_x+err+1):
    for coordinate_y in range(coo_y-err,coo_y+err+1):
    
            
        img_array = []
        for image in images:
            im=Image.open(os.path.join(file,image))
            px = im.load()
            rgb_convert=im.convert("RGB")
            
            #rgb_pixel_value=rgb_convert.getpixel((189,219)
            rgb_pixel_value=rgb_convert.getpixel((coordinate_x,coordinate_y))
            #the following line will append pixel rgb values in each loop iteration to a list 
            img_array.append(rgb_pixel_value)

        print(img_array)
        # rainfall intensity color_codes189
        color_codes = [(153,204,255),(0,153,255),(0,255,102),(0,204,0),(0,153,0),(0,102,0),(255,255,51),(255,204,0),(255,153,0),(255,102,0),(255,0,0),(255,2,153),(153,51,204),(102,0,153),(152,152,102),(153,153,102),(255,255,255),(254,254,254),(0,0,0),(105,105,105),(51,51,102)]
        intensity_legend =('0.1-1','1-2.5','2.5-4','4-8','8-12','12-18','18-24','24-37','37-50','50-75','75-100','100-150','150-200','Above 200','0','0','No data (White)','No data (White)','No data (Black)','No data (Grey)', '0')
        intensity_lower = (0.1,1,2.5,4,8,12,18,24,37,50,75,100,150,200,0,0,0,0,0,0,0)
        intensity_upper = (1,2.5,4,8,12,18,24,37,50,75,100,150,200,300,0,0,0,0,0,0,0)
        intensity_middle = (0.55,1.75,3.25,6,10,15,21,30.5,43.5,62.5,87.5,125,175,200,0,0,0,0,0,0,0)

        intensity = []
        for i in img_array:
            for idx, j in enumerate(color_codes):
                if i == j:
                    intensity.append((intensity_legend[idx],intensity_lower[idx],intensity_middle[idx],intensity_upper[idx]))
                    
        x = np.linspace(1,len(img_array),len(img_array))
        print(intensity)
        intensity = np.asarray(intensity, dtype = object)
        intensity[:,1] = intensity[:,1].astype(float)
        intensity[:,2] = intensity[:,2].astype(float)
        intensity[:,3] = intensity[:,3].astype(float)
        
        time = []
        time_24hr= []
        for filename in os.listdir(file):
            if os.path.splitext(filename)[-1] == '.gif':
                time.append(filename[9:13])

        for idx,i in enumerate(time):
            time_24hr.append(time[idx][:2] + ':' + time[idx][2:])  #buuild a simple string array with 24 hr time format

        df_array = np.hstack((time_24hr, intensity[:,0], intensity[:,1], intensity[:,2], intensity[:,3]))


        df_1 = pd.DataFrame(intensity, columns = ['Intensity range (mm/hr)','Lower range of intensity (mm/hr)','Mean intensity (mm/hr)','Upper range of intensity (mm/hr)'])
        df_2 = pd.DataFrame(time_24hr, columns = ['Time (24 hr format)']) 


        #Seaborn plot
        fig = plt.figure(figsize=(15,4))
    
        a=sns.lineplot(x=x, y=intensity[:,2], label = 'Mean rainfall', color ='b', markers = "o",palette="Accent")
        b=sns.lineplot(x=x, y=intensity[:,1], label='Upper limit', color = 'b', alpha=.1)
        c=sns.lineplot(x=x, y=intensity[:,3], label='Lower limit', color = 'b', alpha=.1)

        line = c.get_lines()
        # plt.fill_between(line[0].get_xdata(), line[1].get_ydata(), line[2].get_ydata(), color='blue', alpha=.3)

        #set x ticks as range from 1 to number of rain data points
        a.set_xticks(range(len(x)))
        # replaces the x ticks with 24 hour time format
        a.set_xticklabels(time_24hr)
        #sns.scatterplot(x =df_sat_test['t'], y = np.array(test_ppc.observed_data.obs), label = 'True Value')

        plt.legend()
        plt.grid()
        plt.xlabel("Time (hr)")
        plt.ylabel("Rainfall intensity (mm/hr)")
        plt.title("Rainfall Hydrograph at Pixel Co-ordinate: x={} , y={}".format(coordinate_x,coordinate_y))
        plt.xticks(rotation=90)
        ###
        files = 'graphs/'+ str(coordinate_x) + ',' + str(coordinate_y)+'.tiff'
        plt.savefig(files, dpi = 300, bbox_inches='tight')
        plt.close()
        # print("Graph generated successfully!")
        #Convert to dataframe
        tuples=tuple(time)
        df_test= pd.DataFrame ({"Time":time,"Lower":intensity[:,1],"Mean":intensity[:,2],"Upper":intensity[:,3]})
        df_test.to_csv('excel_files/'+'export_rainfall_hydrograph'+'_'+str(coordinate_x)+','+str(coordinate_y)+'.csv')

#Convert to dataframe
print('Hydrographs plotted!')

