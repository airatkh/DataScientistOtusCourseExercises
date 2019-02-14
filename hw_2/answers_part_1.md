

Есть несколько замечаний:

Вы писали
 > - В графике количество мужчин женщин подписи к оси абсцисс слились

Единственное что пока удалось это сделать вот статистик

Выставить
```sh
plt.figure(figsize=(80,5))
```

[PrinnScree_Image](http://i.imgur.com/F85OHzq.png)

Этот вариан нормально?
Если **нет** , **подскажите куда копать**?


> - По первым буквам имени лучше использовать гистограмму

Решил добавить гистограмму и для гругих грфиков.

[Добавил гистограмму 1](http://i.imgur.com/uDKNqLr.png)

[Добавил гистограмму 2](http://i.imgur.com/P4B7tkr.png)

[Добавил гистограмму ](http://i.imgur.com/K32XhVW.png)


> - Не стоит использовать переменную sorted (это встроенная функция)

Глупая ошибка новичка, переименовал в ```sorted_baby_year```


> - за какую сложность реализовано:

```python
total_baby = baby.groupby(['year', 'name']).sum().unstack()

names_number = []
for year in range(1880, 2011):
    year = str(year)
    half_year = total_baby.loc[year].sum() / 2
    sorted_baby_year = total_baby.loc[year].sort_values(ascending=False)
    for i in range(1, len(total_baby.loc[year])):
        s = sorted_baby_year[:i].sum()
        if s >= half_year:
            names_number.append(i)
            break

```

Мне кажеться:

```O(n2)``` — квадратичная сложность

> Можно ли быстрее? (можете не исправлять, а только написать ответ)

Скорее всего да. Сейчас нет ответ
