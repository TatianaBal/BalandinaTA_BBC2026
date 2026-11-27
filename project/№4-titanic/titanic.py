import pandas as pd
import numpy as np
df=pd.read_csv('tested.csv')
#print(df)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

n=int(input("Введите количество первых строк для вывода: "))
print(f"\nпервые {n} строк:" )
print(df.head(n))#первые n строк
#8
print("\nПосдедние 5 строк:" )
print(df.tail(5))#последние 5 строк
#9
print(f"\nРазмерность таблицы: {df.shape} (строк, столбцов)")
#10
print(f"\nСтолбцы: {df.columns.tolist()}")
#11
print("\nТипы данных столбцов: ")
print(df.dtypes)
#12
numeric_cols=df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols=df.select_dtypes(exclude=[np.number]).columns.tolist()
print(f"\nЧисловые столбцы: {numeric_cols}")
print(f"\nКатегориальные столбцы: {categorical_cols}")
#13
print("\nСтатистика числовых признаков (среднее, медиана, мин, макс, стд.откл):")
print(df[numeric_cols].describe().loc[['mean','50%','min','max','std']])
#14
print("\Количество пассажиров по классам: ")
print(df['Pclass'].value_counts())
#15
print(f"\nУникальных значений в Embarked: {df['Embarked'].nunique()}")
#16
print("\nКоличество пропусков в столбцах:")
print(df.isnull().sum())
#17
print("\nПроцент пропусков:")
print((df.isnull().sum()/len(df))*100)
#18
max_missing_col=df.isnull().sum().idxmax()
print(f"\nМаксимальное количество пропусков: {max_missing_col}")
#19
print("\nСтатистика Age до заполнения:")
age_stats_before=df['Age'].agg(['mean','median','min','max','std','count'])
print(age_stats_before)
#20
age_median=df['Age'].median()
df['Age']=df['Age'].fillna(age_median)
#21
print("\nСтатистика Age после заполнения:")
age_stats_after=df['Age'].agg(['mean','median','min','max','std','count'])
print(age_stats_after)
#22
print("\nСравнени до/после:")
comparison=pd.DataFrame({
    'До обработки': age_stats_before,
    'После обработки': age_stats_after
})
print(comparison)
#23
df=df.dropna(subset=['Embarked'])
print("\nСтроки с пустым Embarked удалены")
#24
cabin_missing_pct=df['Cabin'].isnull().mean()
if cabin_missing_pct>0.5:
    df=df.drop(columns=['Cabin'])
    print("Столбец Cabin удален(пропусков >50%)")
#25
print("\nОставшиеся пропуски:")
print(df.isnull().sum())
#26
print(f"\nТекущий размер таблицы: {df.shape}")
#массивы
survived_np=df['Survived'].to_numpy()
sex_np=df['Sex'].to_numpy()
age_np=df['Age'].to_numpy()
fare_np=df['Fare'].to_numpy()
#31
print(f"\nОбщий процент выживших: {np.mean(survived_np)*100:.2f}%")
#32
male_survived=np.mean(survived_np[sex_np=='male'])*100
female_survived=np.mean(survived_np[sex_np=='female'])*100
print(f"Выжившие мужчины: {male_survived:.2f}%")
print(f"Выжившие женщины: {female_survived:.2f}%")
#33
male_age=np.mean(age_np[sex_np=='male'])
female_age=np.mean(age_np[sex_np=='female'])
print(f"Средний возраст мужчин: {male_age:.2f}, женщин: {female_age:.2f}")
#34
print("\nСредний возраст по категориям:")
male_survived_age=age_np[(sex_np=='male')&(survived_np==1)]
male_dead_age=age_np[(sex_np=='male')&(survived_np==0)]
female_survived_age=age_np[(sex_np=='female')&(survived_np==1)]
female_dead_age=age_np[(sex_np=='female')&(survived_np==0)]
if len(male_survived_age)>0:
    print(f"Мужчины выжившие: {np.mean(age_np[(sex_np=='male')&(survived_np==1)]):.2f}")
else:
    print("Мужчины выжившие: таких нет")
if len(male_dead_age)>0:
    print(f"Мужчины погибшие: {np.mean(age_np[(sex_np=='male')&(survived_np==0)]):.2f}")
else:
    print("Мужчины погибшие: таких нет")
if len(female_survived_age)>0:
    print(f"Мужчины выжившие: {np.mean(age_np[(sex_np=='female')&(survived_np==1)]):.2f}")
else:
    print("Женщины выжившие: таких нет")
if len(female_dead_age)>0:
    print(f"Мужчины погибшие: {np.mean(age_np[(sex_np=='female')&(survived_np==0)]):.2f}")
else:
    print("Женщины погибшие: таких нет")
#35
print(f"Билет: min={np.min(fare_np):.2f}, max={np.max(fare_np):.2f}, mean={np.max(fare_np):.2f}")
#36
print(f"Станд.откл. возраста: {np.std(age_np):.2f}")
#1 задание
task1=df[(df['Sex']=='male')&(df['Age']>30)&(df['Pclass']==1)]
print(f"\nЗадание 1: Найдено {len(task1)} пассажирa(ов).")
print(task1.head(10))
#2 задание
task2=df[((df['Age']<18)|(df['Sex']=='female'))&(df['Survived']==1)]
print(f"\nЗадание 2: Найдено {len(task2)} пассажирa(ов)")
#3 Задание
mean_fare_3rd=df[df['Pclass']==3]['Fare'].mean()
task3=df[(df['Pclass']==3)&(df['Fare']>mean_fare_3rd)]
print(f"\nЗадание 3: Средняя цена в 3 классе = {mean_fare_3rd:.2f}. Найдено {len(task3)} пассажирa(ов).")
#4 задание
task4=df[(df['Age']>=20)&(df['Age']<=40)&(df['Embarked']=='S')]
print(f"\nЗадание 4: Найдено {len(task4)} пассажирa(ов).")
#37
group1=df.groupby(['Pclass','Sex']).agg(
    Количество=('Sex','count'),
    Средний_возраст=('Age','mean'),
    Доля_выживших=('Survived',lambda x: np.mean(x)*100),
    Средняя_стоимость=('Fare','mean')
)
print("\nГруппировка по классу и полу:")
print(group1)
#38
group2=df.groupby('Embarked').agg(
    Количество=('Sex','count'),
    Процент_выживших=('Survived', lambda x: np.mean(x)*100)
)
print("\nГруппировка по порту:")
print(group2)
#39
class_survival=df.groupby('Pclass')['Survived'].mean()
best_class=class_survival.idxmax()
print(f"\nКласс с наибольшей долей выживших: {best_class}")
#cохранение
df.to_csv('titanic_processed.csv', index=False)
print("\nФайл titanic_processed.csv сохранен.")
group1.to_csv('titanic_statistics.csv')
print("Файл titanic_statistics.csv сохранен.")
df_check=pd.read_csv('titanic_processed.csv')
print("\nПроверка загрузки (первые 3 строки):")
print(df_check.head(3))
print(f"Размер загруженного файла: {df_check.shape}")

