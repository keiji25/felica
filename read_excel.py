import pandas as pd

df = pd.read_excel('全学生名簿2022.xlsx')

s = df[["学科名", "記号", "年次", "性別", "学籍番号", "氏名＿漢字", "氏名＿カナ"]][df["学籍番号"].isin(["K019C1084"])]
print(s.values.tolist())