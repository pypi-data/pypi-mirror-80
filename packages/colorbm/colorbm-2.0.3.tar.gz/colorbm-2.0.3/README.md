# colorbm

Color Beyond Matplotlib：提供`matplotlib` 之外的色彩图（Colormap）以及色板（Color Palette），仅此而已。

主要用于使用`matplotlib`进行科技论文配图的绘制。
`colorbm`提供三类色彩图或色板（色彩图包含diverging和sequential两类）：
1. `diverging` 色彩图：此类色彩图适合绘制需要突出数值正负区别的图片，或者数值大小之间有明显的分界线
2. `sequential` 色彩图：此类色彩图具有连续的色彩变化，适合绘制数值连续变化（Continuous Data）的图片
3. `palettes` 色板：顾名思义，色板是不同颜色的集合，适合绘制分类数据（Categorical Data）以及离散数据（Discrete Data）

所有彩色图以及色板均从网络收集，包括或不仅限于以下图集：
- `ggsci` ：[官网](https://nanx.me/ggsci/index.html)
- `seaborn` ：[官网](https://seaborn.pydata.org/)
- `cmocean` ：[官网](https://github.com/matplotlib/cmocean)
- `scientific` ：[官网](http://www.fabiocrameri.ch/colourmaps.php)
- `CMasher` ：[官网](https://github.com/1313e/CMasher)
- `CARTO` ：[官网](https://github.com/CartoDB/cartocolor)
- `Material Design` ：[官网](https://material.io/design/color/the-color-system.html#color-usage-and-palettes)


## 版本变动
20200924:
- 增加了`pal`类，现在导入色板与色彩图有同样的操作
- 增加了输出颜色至`xml`与`csv`格式文件，可以用于导入至`paraview`软件；
- 色板中增加了`nintendo`分类，包括`mario`，`luigi`，`yoshi`，`isabelle`以及`tomnook` 五个色板

20200923：
- 增加了色彩图
- 增加了预览色彩图以及色板的功能
- 增加了输出色彩图以及色板名称的功能
- 增加`pip`安装选项
- 增加了色彩图：`turbo`（Google AI Lab）以及`parula`（MATLAB默认色彩图）

20200922：增加来自[世界名画](https://designshack.net/articles/inspiration/10-free-color-palettes-from-10-famous-paintings/) 的色板以及《经济学人》杂志色板
<br>
<br>


## 使用说明
### 安装
使用`pip`进行安装：
```
pip install colorbm
```
在国内网络环境可以通过`pypi`镜像进行安装，例如：
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple colorbm
```

如果使用`anaconda`发行版，可切换至需要安装的虚拟环境，再使用`pip`进行安装：
```
conda activate myenv
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple colorbm
```

### 安装测试
```
import colorbm as cbm

cbm.pcolor('crest').show()
```

如果安装成功便可输出类似下方图片。

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/221106_6844c853_7853830.png "test.png")

### 色彩图与色板名称说明
为了输入方便，所有的色彩图与色板名称均采用`小写字母`

### 色板的使用
调用`pal()`类以使用色板，该类下面有4种方法：
- `as_cmap` ：此方法返回`Colormap object`
- `as_cmap_r`：此方法返回反向色彩图
- `as_hex` ：此方法返回所选色板颜色的`HEX`列表
- `as_rgb`： 此方法返回所选色板颜色的`RGB`列表

这四种方法定义时加上了属性（`property`）装饰器，调用时不用加括号。
例如： `cbm.pal('mario').as_cmap`，将返回通过 `mario` 色板创建的 `Colormap object`

实例：将所选择色板赋值于`matplotlib`中`cmap`参数
下例中调用`npg` 色板
```
import numpy as np
import matplotlib.pyplot as plt
import colorbm as cbm

plt.rcParams['scatter.edgecolors'] = 000000

np.random.seed(19680801)
N = 50
x = np.random.rand(N)
y = np.random.rand(N)

fig, ax = plt.subplots()
colors = np.random.rand(N)
area = (30 * np.random.rand(N)) ** 2  # 0 to 15 point radii

ax.scatter(x, y, s=area, c=colors, alpha=0.5, cmap=cbm.pal('npg').as_cmap)
plt.show()
```

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/203533_1b632acc_7853830.png "scatter.png")

此外，也可将颜色的`HEX`列表用于`seaborn`中

```
import matplotlib.pyplot as plt
import seaborn as sns
import colorbm as cbm

sns.set_palette(sns.color_palette(cbm.pal('npg').as_hex))

# Load the penguins dataset
penguins = sns.load_dataset("penguins")

# Plot sepal width as a function of sepal_length across days
g = sns.lmplot(
    data=penguins,
    x="bill_length_mm", y="bill_depth_mm", hue="species",
    height=5
)

plt.show()
```

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/203555_f95c72d6_7853830.png "sns.png")

### 色彩图的使用
调用`seq()` 或 `div()` 类以使用色彩图，这两类分别对应 `sequential` 和 `diverging` 色彩图
这两类同样有四种方法：
- `as_cmap` ：此方法返回`Colormap object`
- `as_cmap_r`：此方法返回反向色彩图
- `as_hex` ：此方法返回所选色板颜色的`HEX`列表
- `as_rgb`： 此方法返回所选色板颜色的`RGB`列表

例如： 
`cbm.seq('burg').as_cmap` ：使用连续色彩图`burg`；
`cbm.div('vlag').as_cmap` ：使用离散色彩图`vlag`；
`cbm.seq('burg').as_cmap_r` ：使用可以反转的`burg`色彩图。

此外，还可以确定离散颜色的个数，例如： `cbm.seq('burg', 10).as_cmap`。这将从色彩图中通过均匀抽样取得10种颜色。下方是5种与10种离散颜色的区别：

![输入图片说明](https://images.gitee.com/uploads/images/2020/0924/151439_75cc7591_7853830.png "burg_d.png")


实例：

```
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import colorbm as cbm

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cbm.seq('burg', 50).as_cmap)

plt.show()
```

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/203618_fd101c81_7853830.png "mat.png")

### 色彩图与色板的测试
调用`pcolor`类对已有色彩图与色板进行测试，此类下方有三种方法：
- `show()` ：会临时显示一幅使用该色板的图像。例如：`cbm.pcolor('flare').show()`；或者使用 `cbm.pcolor('flare', 50).show(reversed=True)` 获得反转色彩图
- `to_xml()`：输出`paraview`使用的色彩图`xml`文件，对色板无效。需要输入保存文件路径以及文件名（如果没有参数输入，默认路径为当前路径，文件名为色彩图名称）。例如： `cbm.pcolor('flare').to_xml(wd=myDir, filename=myName)`
- `to_csv()`：默认输出色彩图以及色板中颜色的`RGB`列表至`csv`文件，可以设置输出`HEX`列表，例如`cbm.pcolor('flare').to_csv(wd=myDir, filename=myName, fmt='hex')`

### 通过色彩图与色板方案查询色彩图或色板名称
`print(cbm.available_palettes().get)` :输出所有色板的名称
`print(cbm.available_palettes('nintendo').get)` ：输出特定色板方案中有的色板名称<br>
现色板方案有：<br>
`ggsci`, `paintings`, `carto`, `misc`，`nintendo`

`print(cbm.available_colormaps().all)` :输出所有色彩图的名称
`print(cbm.available_colormaps('carto').all)` :输出某个色彩图方案中所有色彩图的名称
`print(cbm.available_colormaps().div)` :输出所有离散色彩图的名称
`print(cbm.available_colormaps().seq)` :输出所有连续色彩图的名称
`print(cbm.available_colormaps('carto').div)` :输出某个色彩图方案中所有离散色彩图的名称
`print(cbm.available_colormaps('carto').seq)` :输出某个色彩图方案中所有离散色彩图的名称<br>
现色彩图方案有：<br>
`seaborn`，`carto`，`scientific`，`cmasher`，`cmocean`，`misc`，`mat`



## 包含的色彩图以及色板
### 色彩图
#### **`seaborn`**

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/203728_26efe3d1_7853830.png "seaborn_cmaps.png")

#### **`carto`**

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/203803_7c1a5956_7853830.png "carto_cmaps_2.png")

#### **`cmoceam`**

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/203923_ccef48f4_7853830.png "cmocean_cmap.png")

#### **`scientific`**

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/203941_8fe2b6a7_7853830.png "scientific_cmaps.png")

#### **`cmasher`**

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/203955_eac6ed84_7853830.png "cmasher_cmaps.png")

#### **`mat`** （Material Design）

#### **`misc`**


### 色板
#### **`carto`**

![输入图片说明](https://images.gitee.com/uploads/images/2020/0923/164736_29eeda62_7853830.png "carto_pal.png")

- `antique`
- `bold`
- `pastel`
- `prism`
- `safe`
- `vivid`

#### **_`ggsci`_**
具体颜色可查询[ggsci网站](https://cran.r-project.org/web/packages/ggsci/vignettes/ggsci.html)
- `npg`：自然出版集团出版杂志所用色板（Nature系列杂志）
- `aaas`：美国科学促进会出版杂志所用色板（Science系列杂志）
- `nejm`: 新英格兰医学杂志所用色板
- `lancet`：柳叶刀杂志所用色板
- `jama`：美国医学会杂志所用色板
- `jco`: 临床肿瘤学杂志所用色板
- `ucscgb`: 基因组浏览器用于染色体可视化的色板
- `d3`: JavaScript程序库D3.js所用色板，有四个分类： `d3_10`、`d3_20`、`d3_20b`以及 `d3_20c`
- `locuszoom`: LocusZoom图所用色板
- `igv`：`IGV`软件所用色板，有两个分类可用：`igv`以及`igv_alternative`
- `uchicago`: 芝加哥大学所用色板，有三个分类可用：`uchicago`、`uchicago_light`以及`uchicago_dark`
- `startrek`: 《星际迷航》系列影片所用色板
- `tron`: 《创：战纪》影片所用色板，其背景颜色较暗
- `futurama`: 《飞出个未来》电视剧所用色板
- `rickandmorty`: 《瑞克和莫蒂》电视剧所用色板
- `simpsons`: 《辛普森一家》电视剧所用色板
- `gsea`: GSEA分析所用色板
- `economist`: 经济学人杂志所用色板，有三个分类：`economist`、`economist_primary`以及`economist_alternative`

#### **_`paintings`_**
具体颜色可查询[网站](https://designshack.net/articles/inspiration/10-free-color-palettes-from-10-famous-paintings/)
- `starrynight`：来自梵高的名画《星夜》
- `monalisa`：来自达芬奇的名画《蒙娜丽莎》
- `scream`：来自蒙克的名画《呐喊》
- `lastsupper`：来自达芬奇的名画《最后的晚餐》
- `afternoon`：来自修拉的名画《大碗岛的星期天下午》
- `optometrist`：来自洛克威尔的名画《验光师》
- `kanagawa`：来自葛饰北斋的名画《神奈川冲浪里》
- `kiss`：来自克里姆特的名画《吻》
- `memory`：来自达利的名画《《持续的记忆》
- `lilies`：来自莫奈的名画《睡莲》

#### **_`misc`_**
包含以下色板
- `economist`
- `economist_primary`
- `economist_alternative`