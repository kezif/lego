import pandas as pd
import xml.etree.ElementTree as et 
from config import  item_condition_table
from bs4 import BeautifulSoup


def exctract_withlist(path):
    xtree = et.parse(path)
    xroot = xtree.getroot()

    rows = []
    for node in xroot: 
        s_id = node.find("ITEMID").text
        s_maxprice = node.find("MAXPRICE").text
        s_qty = node.find("MINQTY").text
        s_condition = node.find("CONDITION").text
        s_color = node.find("COLOR").text if node.find("COLOR") else None
        
        d = {'part_id': s_id, 'max price': s_maxprice, 'quantity': s_qty, 'condition': s_condition, 'color':s_color}
        rows.append(d)
    
    out_df = pd.DataFrame(rows, columns=['part_id','max price','quantity','condition','color_id'])
    return out_df

def excract_colors():
	soup = None
	print('loading html file')
	with open('pages\\tables.html', 'r') as file:
		soup = BeautifulSoup(file, 'html.parser')
	print('exctacting tables')	
	color_tables = soup.find_all('table', attrs={'bgcolor':"#FFFFFF"})
	color_tables = color_tables[1:] # first table doesnt contain color information
	
	colors = []
	#print('color_tables',len(color_tables))
	colors_df = pd.DataFrame(columns=['color_id','Name', 'Code','Parts','In Sets','Wanted','For Sale','Color Timeline'])
	
	i = 0
	for color_table in color_tables[:]:
		i = i+1
		print('exctracting colors from tables... ' + str(i), end='\r')
		color_rows = color_table.find_all('tr')  # tables with color information
		#print('color_rows',len(color_rows))
		for color_row in color_rows[2:]:		# proces each row of table
			col = color_row.find_all('td')		# exctract each column from row
			#print('col',len(col))
			if (col[4].text.strip() == ''): # color with no info, such as "Neon Orange" are skipped
				continue
			color_code = col[1]['bgcolor']	# second column is box colored with color's color (color color?)
			colors.append({'color_id': int(col[0].text), 
							'Name':col[3].text.strip(), 
							'Parts':int(col[4].text), 
							'In Sets':int(col[5].text), 
							'Wanted':int(col[6].text), 
							'For Sale':int(col[7].text), 
							'Color Timeline':col[8].text.strip().replace(u'\xa0',u' '),
							'Code': color_code
						})
		#colors_df.loc[len(colors)] = colors  # appending to the end
		colors_df = colors_df.append(colors)
	print('\nexmaple:',colors_df[['color_id','Name','Code']].head(5), '\nlen: ',len(colors_df.index))
	print('writing to file')
	colors_df.to_csv('colors.csv', float_format='%.0f', index=False)
		
	
def main():
	excract_colors()
    #df = exctract_withlist(xml_path)
    #print(df.head())

if __name__ == '__main__':
    main()


    