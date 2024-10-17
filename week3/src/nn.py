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
import matplotlib.animation as animation  
import numpy as np  
import pandas as pd  
  
# 假设我们有一个简单的数据框架来模拟数据  
np.random.seed(0)  
dates = pd.date_range(start='2023-01-01', periods=100, freq='D')  
locations = np.random.uniform(low=-10, high=10, size=100)  
magnitudes = np.random.uniform(low=4.0, high=7.0, size=100)  
  
df = pd.DataFrame({  
    '日期（香港时间）': dates,  
    '地震矩震级 Mw': magnitudes,  
    '香港录得最高的水位异常（正常潮位以上高度）': locations  
})  
  
# 创建一个图形和一个子图  
fig, ax = plt.subplots(figsize=(12, 8))  
  
# 初始化散点图  
scatter, = ax.scatter([], [], s=[], c='blue', alpha=0.6, edgecolors='w', linewidth=0.5)  
  
# 初始化函数（用于设置散点图的初始状态）  
def init():  
    scatter.set_offsets([])  
    return scatter,  
  
# 动画更新函数  
def update(frame):  
    # 选择前frame个数据点进行绘制  
    x = df['日期（香港时间）'][:frame]  
    y = df['香港录得最高的水位异常（正常潮位以上高度）'][:frame]  
    s = df['地震矩震级 Mw'][:frame] * 20  
    scatter.set_offsets(np.c_[x.dt.toordinal(), y])  # 注意：这里将日期转换为序数以便绘制，但通常不推荐这样做  
    scatter.set_sizes(s)  
    return scatter,  
  
# 创建动画  
ani = animation.FuncAnimation(fig, update, frames=len(df), init_func=init, blit=True)  
  
# 显示图形  
plt.title('Sea Level Changes Due to Tsunamis Detected in Hong Kong', fontsize=16)  
plt.xlabel('Date (Ordinal)', fontsize=14)  # 注意：这里使用了序数作为x轴标签，因为直接绘制日期会很难看  
plt.ylabel('Maximum Sea Level Change (m)', fontsize=14)  
plt.xticks(rotation=45)  
plt.tight_layout()  
plt.show()