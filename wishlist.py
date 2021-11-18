import xml.etree.ElementTree as et 
import pandas as pd

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

def main():
	#excract_colors()
	xml_path = 'whislists//mecjh.xml'
	df = exctract_withlist(xml_path)
	print(df)
    

if __name__ == '__main__':
    main()