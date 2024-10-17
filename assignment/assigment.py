import requests

url = "https://www.hko.gov.hk/sc/gts/equake/tsunami_mon.htm"
response = requests.get(url)
if(response.ok):
    print("data is ready!")
else:
    print(response.status_code)

from bs4 import BeautifulSoup
#print(response.text)
content=requests.get("https://www.hko.gov.hk/sc/gts/equake/tsunami_mon.htm").text
soup = BeautifulSoup (content,"html.parser")
table = soup.find('table', {'class': 'table_align_center table_border_1 data_table'})

# 提取表头
headers = [header.get_text(strip=True) for header in table.find_all('th')]

# 提取表格数据
rows = table.find_all('tr')[1:]  # 跳过表头行
data = []
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True) for cell in cells]
    data.append(row_data)

# 打印提取的数据
print(headers)
for row in data:
    print(row)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 假设 data 和 headers 已经定义好（这里省略了它们的定义）  
# headers = ['日期（香港时间）', '震中地点', '地震矩震级 Mw', '香港录得最高的水位异常（正常潮位以上高度）']  
# data = [...]  
  
# 创建DataFrame  
df = pd.DataFrame(data, columns=headers)  
  
# 打印列名以检查  
print("Columns in DataFrame:", df.columns)  
# 清理地震矩震级数据，移除非数字字符  
def clean_magnitude(value):  
    if pd.isna(value):  # 检查是否为NaN  
        return np.nan  
    value = ''.join(char for char in value if char.isdigit() or char == '.')  # 保留数字和点  
    try:  
        return float(value)  
    except ValueError:  
        return np.nan  # 如果无法转换为浮点数，则返回NaN  
  
# 清理地震矩震级数据  
df['地震矩震级 Mw'] = df['地震矩震级 Mw'].apply(clean_magnitude) 
  
# 处理海平面变化数据，将其转换为数值  
def convert_sea_level_change(value):  
    if '少于' in value or 'less than' in value:  
        return 0.05  # 假设小于某个未明确给出的小值为0.05米  
    elif '约' in value or '大约' in value or 'around' in value:  
        try:  
            return float(value.split()[1])  # 假设“约”或“大约”后跟的是具体数值  
        except ValueError:  
            return 0.1  # 如果无法提取数值，则返回一个默认值  
    else:  
        try:  
            return float(value.split()[0])  # 尝试获取并转换第一个词为浮点数  
        except ValueError:  
            return None  # 如果无法转换，则返回None（或根据需要处理） 
  
# 找到包含海平面变化数据的列名  
sea_level_change_col = '香港录得最高的水位异常（正常潮位以上高度）'  
  
# 转换海平面变化数据  
df[sea_level_change_col] = df[sea_level_change_col].apply(convert_sea_level_change)  
  
# 将日期转换为datetime格式  
df['日期（香港时间）'] = pd.to_datetime(df['日期（香港时间）'], format='%Y/%m/%d')  # 假设日期格式为'%Y/%m/%d'，根据实际情况调整  
  
# 创建图形  
plt.figure(figsize=(12, 8))  

  
plt.scatter(df['日期（香港时间）'],  
            df[sea_level_change_col],  
            s=df['地震矩震级 Mw'].astype(float) * 20,  # 现在可以安全地转换为float  
            c='blue',  
            alpha=0.6,  
            edgecolors='w',  
            linewidth=0.5)  
  
# 添加标题和标签  
plt.title('Sea Level Changes Due to Tsunamis Detected in Hong Kong', fontsize=16)  
plt.xlabel('Date (Hong Kong Time)', fontsize=14)  
plt.ylabel('Maximum Sea Level Change (m)', fontsize=14)  
  
# 显示图形  
plt.xticks(rotation=45)  
plt.tight_layout()  
plt.show()