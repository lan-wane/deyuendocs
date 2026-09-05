---
title: DeSource Markdown 表格测试样例
description: 用于验证简单模式与复杂模式表格渲染
author: DeSource
datetime: 2026-09-02 00:00:00
protect: false
---

# 一、简单模式

## 1.1 基础表格（对齐 + 主题）

!theme striped
!style row=2 highlight

|  姓名 | 年龄 | 城市 |
| :-: | -: | :- |
|  张三 | 25 | 北京 |
|  李四 | 30 | 上海 |
|  王五 | 28 | 广州 |

## 1.2 跨列合并 + 预设样式

!theme bordered rounded
!style col=B bold
!style col=C color-blue
\| :: 班级成绩表 :: |  |  |
\| 姓名 | 语文 | 数学 |
\| 小明 | 90 | 85 |
\| 小红 | 88 | 92 |
\| 小刚 | 95 | 78 |

## 1.3 纵向合并（..）

!theme compact
\| 部门 | 姓名 | 职位 |
\| 技术部 | 张三 | 工程师 |
\| .. | 李四 | 架构师 |
\| 市场部 | 王五 | 经理 |

***

# 二、复杂模式

## 2.1 多级表头 + 列样式 + 单元格格式

?list sales =
?config theme=striped
?style cell A1 { background-color:#fff3bf; font-weight:bold; }
?style col=B color-blue
?format C2:E5 "#,##0.00"
?comment B2 "销售额来自销售系统"
?thead
\| :: 销售统计表 :: |  |  |  |
\| 地区 | 销售额 | 提成 | 评分 |
\| 北京 | 5000 | 500 | 4.5 |
\| 上海 | 3000 | 300 | 4.0 |
\| 广州 | 7000 | 700 | 4.8 |
\| 深圳 | 2000 | 200 | 3.5 |
?total sum=销售额 sum=提成 avg=评分

## 2.2 条件格式

?list scoreboard =
?config theme=striped
?conditional-format range=B2:C6 {
rule: cell.value >= 90 -> style { background-color: #9f9; font-weight: bold; }
rule: cell.value < 60 -> style { background-color: #f99; color: #fff; }
}
?thead
\| 姓名 | 语文 | 数学 |
\| 小明 | 92 | 88 |
\| 小红 | 55 | 90 |
\| 小刚 | 70 | 65 |
\| 小雨 | 58 | 82 |
\| 小强 | 95 | 99 |

## 2.3 公式计算（总分 / 平均）

?list formula =
?config theme=bordered
?thead
\| 姓名 | 语文 | 数学 | 总分 | 平均 |
\| 张三 | 90 | 85 | {{ 语文 + 数学 }} | {{ (语文 + 数学) / 2 }} |
\| 李四 | 70 | 80 | {{ 语文 + 数学 }} | {{ (语文 + 数学) / 2 }} |
\| 王五 | 60 | 75 | {{ 语文 + 数学 }} | {{ (语文 + 数学) / 2 }} |
?total sum=总分 avg=平均

## 2.4 排序 + 筛选

?list ranking =
?config theme=compact
?order by 销售额 desc
?filter 销售额 > 2500
?thead
\| 地区 | 销售额 |
\| 北京 | 5000 |
\| 上海 | 3000 |
\| 广州 | 7000 |
\| 深圳 | 2100 |
\| 成都 | 2600 |

## 2.5 纵向合并（指定跨度 merge down）

?list org =
?style col=A bold
?thead
\| 一级部门 | 二级部门 | 负责人 |
\| merge down=2 华东大区 | 研发部 | 张三 |
\| .. | 销售部 | 李四 |
\| merge down=2 华北大区 | 研发部 | 王五 |
\| .. | 市场部 | 赵六 |

## 2.6 图表（?chart）

?list chart\_demo =
?config theme=striped
?thead
\| 地区 | 销售额 | 费用 |
\| 北京 | 5000 | 3000 |
\| 上海 | 3000 | 1500 |
\| 广州 | 7000 | 4200 |
\| 深圳 | 2000 | 900 |
?chart type=bar title="各地区销售额（柱状图）" x=地区 y=销售额
?chart type=pie title="销售占总比（饼图）" x=地区 y=销售额
?chart type=line title="销售与费用趋势（折线图）" x=地区 y=销售额,费用 legend=true
?chart type=area title="销售额面积（渐变+平滑）" x=地区 y=销售额
?chart type=bar title="自定义刻度 step=2000" x=地区 y=销售额 step=2000
?chart type=bar title="断裂轴（锯齿折叠下方数据）" x=地区 y=销售额 break=on yname=销售额
?chart type=line title="ECharts 同款平滑折线" x=地区 y=销售额,费用 smooth=on legend=true

各位这是一坨测试文本，我会在10分钟内给他删掉，如果GitHub崩了就当我没说