import pandas as pd
import xml.etree.ElementTree as et 
from config import *  
from bs4 import BeautifulSoup

'''
I really love lego and in one day i decided to buy set. It have outstanding minifigures but, other than that, model is kinda meh.
It was unfortunate but not the end of the world. ALso, right whn my set was delivered - i found video about set modification! 
HEre is the video. 

It was so much better than original set, that a decided to build. To do that I needed some additional pieces..
Lego is a great product. One of the reasons is that pieces have great quality and, in fact, you can use really old lego pieces almost like the new ones.
In my opinion, because of that, there is a large second hand market, where you can buy set or piece in any shape or form.
There are two large markets that sell lego pieces: bricklink and brickowl. Bricklink is more popular and have more seller, brickowl, in my opinion, have more frendly site.
Well.. the problem is that both sites doesnt have a good wishlist search. So i decded to build one by myself.

Let's start with data excraction.

I decided to start of with part colors. There are huge variety of colors presented in lego bricks. Lukly briklink have convinient page where all colors are presented with they respectful id.
(image)

'''

def exctract_withlist(path):
    xtree = et.parse(path)
    xroot = xtree.getroot()

    rows = []
    for node in xroot: 
        s_id = node.find("ITEMID").text
        s_maxprice = node.find("MAXPRICE").text
        s_qty = node.find("MINQTY").text
        s_condition = node.find("CONDITION").text
        s_color = node.find("COLOR").text if node.find("COLOR") is not None else None
        
        d = {'part_id': s_id, 'max price': s_maxprice, 'quantity': s_qty, 'condition': s_condition, 'color_id':s_color}
        rows.append(d)
    
    out_df = pd.DataFrame(rows, columns=['part_id','max price','quantity','condition','color_id'])
    return out_df

def excract_colors():
	# so it would be pretty easy to parse it. I will use bs to achive that goal.
	# During inspection of page I found that every each of tables, that contain color information, have table tag and have white background
	# 
	soup = None
	print('loading html file')
	with open('pages//tables.html', 'r') as file:
		soup = BeautifulSoup(file, 'html.parser')
	
	color_tables = soup.find_all('table', attrs={'bgcolor':"#FFFFFF"})
	color_tables = color_tables[1:] # first html-table is header and have no usefull info
	
	#excract information from every table and then concat it to a dataframe.
	#data stored in table tags are pretty easy to parse. Each row is inside tr tag and each column is inside td tag.
	colors = []
	
	i = 0
	for color_table in color_tables[:]:
		i = i+1
		print('exctracting colors from tables... ' + str(i), end='\r')
		color_rows = color_table.find_all('tr')  # tables with color information
		#print('color_rows',len(color_rows))
		colors_table = []
		for color_row in color_rows[2:]:		# proces each row of table
			col = color_row.find_all('td')		# exctract each column from row
			#print('col',len(col))
			if (col[4].text.strip() == ''): # color with no info, such as "Neon Orange" are skipped
				continue
			color_code = col[1]['bgcolor']	# second column is box colored with color's color (color color?)
			colors_table.append({'color_id': int(col[0].text), 
							'Name':col[3].text.strip(), 
							'Parts':int(col[4].text), 
							'In Sets':int(col[5].text), 
							'Wanted':int(col[6].text), 
							'For Sale':int(col[7].text), 
							'Color Timeline':col[8].text.strip().replace(u'\xa0',u' '),
							'Code': color_code
						})
		colors.extend(colors_table)
	#Im saving everything to dataframe
	colors_df = pd.DataFrame(colors,columns=['color_id','Name', 'Code','Parts','In Sets','Wanted','For Sale','Color Timeline'])
	print('\nexmaple:',colors_df[['color_id','Name','Code']].head(5), '\nlen: ',len(colors_df.index))
	print('writing to file')
	colors_df.to_csv('colors.csv', float_format='%.0f', index=False)
		
	
def main():
	#excract_colors()
	xml_path = 'whislists//mecjh.xml'
	df = exctract_withlist(xml_path)
	print(df)
    

if __name__ == '__main__':
    main()


    