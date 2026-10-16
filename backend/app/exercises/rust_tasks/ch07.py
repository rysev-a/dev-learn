"""Задачи книги «Изучаем Rust»: глава 7 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {7: [{'id': 'r7-tuple-basic',
      'mode': 'rust',
      'title': 'Кортеж из трёх',
      'statement': 'Создайте кортеж person = ("Аня", 30, 1.68). Напечатайте его элементы по номеру через '
                   'пробел: «Аня 30 1.68».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Аня 30 1.68',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Доступ к элементам: person.0, person.1, person.2.',
      'standalone': True,
      'expected': ['Аня 30 1.68']},
     {'id': 'r7-tuple-destructure',
      'mode': 'rust',
      'title': 'Разбор кортежа',
      'statement': 'Разберите кортеж (10, 20, 30) на переменные a, b, c одним let и напечатайте их сумму '
                   '«60».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '60',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'let (a, b, c) = (…);',
      'standalone': True,
      'expected': ['60']},
     {'id': 'r7-tuple-debug',
      'mode': 'rust',
      'title': 'Печать кортежа',
      'statement': 'Напечатайте кортеж (1, "два", 3.0) в отладочном формате {:?}: «(1, "два", 3.0)».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '(1, "два", 3.0)',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Кортеж нельзя печатать через {} — нужен {:?}.',
      'standalone': True,
      'expected': ['(1, "два", 3.0)']},
     {'id': 'r7-array-sum',
      'mode': 'rust',
      'title': 'Сумма массива',
      'statement': 'Объявите массив nums = [4, 8, 15, 16, 23, 42] и посчитайте сумму его элементов циклом '
                   'for. Напечатайте «108».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '108',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Накопитель sum и цикл for x in nums.',
      'standalone': True,
      'expected': ['108']},
     {'id': 'r7-array-len',
      'mode': 'rust',
      'title': 'Длина и элементы',
      'statement': 'Объявите массив из пяти нулей с помощью [0; 5], затем запишите в a[2] число 7. '
                   'Напечатайте длину и сам массив в формате {:?}: «5» и «[0, 0, 7, 0, 0]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '5\n'
                   '[0, 0, 7, 0, 0]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Массив надо объявить как let mut a, чтобы присвоить элемент.',
      'standalone': True,
      'expected': ['5', '[0, 0, 7, 0, 0]']},
     {'id': 'r7-array-first-last',
      'mode': 'rust',
      'title': 'Первый и последний',
      'statement': 'Для массива [3, 6, 9, 12, 15] напечатайте первый и последний элементы через индексы '
                   '(длина — len()). «3» и «15».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '3\n'
                   '15',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Последний индекс — a.len() - 1.',
      'standalone': True,
      'expected': ['3', '15']},
     {'id': 'r7-array-get',
      'mode': 'rust',
      'title': 'Безопасный индекс',
      'statement': 'Для массива [10, 20, 30] напечатайте a.get(1) и a.get(7) в формате {:?}: «Some(20)» и '
                   '«None».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Some(20)\n'
                   'None',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'get возвращает Option.',
      'standalone': True,
      'expected': ['Some(20)', 'None']},
     {'id': 'r7-slice-print',
      'mode': 'rust',
      'title': 'Срезы',
      'statement': 'Дан массив a = [1, 2, 3, 4, 5, 6]. Напечатайте срезы &a[1..4] и &a[..2] и &a[4..] через '
                   '{:?}: «[2, 3, 4]», «[1, 2]», «[5, 6]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[2, 3, 4]\n'
                   '[1, 2]\n'
                   '[5, 6]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Правая граница не входит.',
      'standalone': True,
      'expected': ['[2, 3, 4]', '[1, 2]', '[5, 6]']},
     {'id': 'r7-vec-push',
      'mode': 'rust',
      'title': 'Растим вектор',
      'statement': 'Создайте пустой вектор v: Vec<i32> и добавьте в цикле for числа 1…5 методом push. '
                   'Напечатайте вектор через {:?}: «[1, 2, 3, 4, 5]» и его длину «5».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[1, 2, 3, 4, 5]\n'
                   '5',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Vec::new() и v.push(i).',
      'standalone': True,
      'expected': ['[1, 2, 3, 4, 5]', '5']},
     {'id': 'r7-vec-pop',
      'mode': 'rust',
      'title': 'pop',
      'statement': 'Из вектора vec![1, 2, 3] удалите последний элемент методом pop и напечатайте его '
                   '(«Some(3)»), затем оставшийся вектор («[1, 2]»).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Some(3)\n'
                   '[1, 2]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'pop возвращает Option.',
      'standalone': True,
      'expected': ['Some(3)', '[1, 2]']},
     {'id': 'r7-vec-evens',
      'mode': 'rust',
      'title': 'Чётные в вектор',
      'statement': 'Создайте вектор чётных чисел от 2 до 20 (цикл и push). Напечатайте вектор: «[2, 4, 6, 8, '
                   '10, 12, 14, 16, 18, 20]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[2, 4, 6, 8, 10, 12, 14, 16, 18, 20]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Условие i % 2 == 0 внутри цикла.',
      'standalone': True,
      'expected': ['[2, 4, 6, 8, 10, 12, 14, 16, 18, 20]']},
     {'id': 'r7-vec-insert-remove',
      'mode': 'rust',
      'title': 'insert и remove',
      'statement': 'Начните с v = [1, 2, 3, 4]. Вставьте 99 на позицию 1 (insert), затем удалите элемент с '
                   'индексом 3 (remove). Напечатайте результат «[1, 99, 2, 4]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[1, 99, 2, 4]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'После insert вектор [1, 99, 2, 3, 4]; remove(3) убирает тройку.',
      'standalone': True,
      'expected': ['[1, 99, 2, 4]']},
     {'id': 'r7-vec-iter-sum',
      'mode': 'rust',
      'title': 'Сумма и среднее',
      'statement': 'Для v = [3, 7, 2, 9, 4] напечатайте через iter(): сумму «25» и среднее арифметическое '
                   '«5» (сумма / длина, целое деление; тип i32).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '25\n'
                   '5',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'v.iter().sum() и приведение длины к i32.',
      'standalone': True,
      'expected': ['25', '5']},
     {'id': 'r7-vec-max-min',
      'mode': 'rust',
      'title': 'Наибольшее и наименьшее',
      'statement': 'Для v = [12, -5, 33, 0, 8] найдите максимум и минимум (iter().max(), iter().min() + '
                   'unwrap): «33» и «-5».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '33\n'
                   '-5',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'max() и min() возвращают Option.',
      'standalone': True,
      'expected': ['33', '-5']},
     {'id': 'r7-vec-mut-loop',
      'mode': 'rust',
      'title': 'Удвоить все',
      'statement': 'Удвойте каждый элемент вектора [1, 2, 3, 4] циклом for x in &mut v (*x *= 2). '
                   'Напечатайте «[2, 4, 6, 8]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[2, 4, 6, 8]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Звёздочка нужна, чтобы изменить само значение.',
      'standalone': True,
      'expected': ['[2, 4, 6, 8]']},
     {'id': 'r7-vec-sort',
      'mode': 'rust',
      'title': 'Сортировка',
      'statement': 'Отсортируйте вектор [5, 2, 9, 1, 7] по возрастанию и напечатайте «[1, 2, 5, 7, 9]», '
                   'затем разверните (reverse) и напечатайте «[9, 7, 5, 2, 1]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[1, 2, 5, 7, 9]\n'
                   '[9, 7, 5, 2, 1]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'sort() и reverse() меняют вектор на месте.',
      'standalone': True,
      'expected': ['[1, 2, 5, 7, 9]', '[9, 7, 5, 2, 1]']},
     {'id': 'r7-vec-contains',
      'mode': 'rust',
      'title': 'Есть ли значение',
      'statement': 'Для v = [10, 20, 30, 40] напечатайте v.contains(&30) и v.contains(&35): «true» и '
                   '«false».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'true\n'
                   'false',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'contains принимает ссылку на значение.',
      'standalone': True,
      'expected': ['true', 'false']},
     {'id': 'r7-vec-dedup',
      'mode': 'rust',
      'title': 'Убрать повторы',
      'statement': 'Отсортируйте вектор [3, 1, 3, 2, 1, 2, 3] и уберите повторы методом dedup. Результат '
                   '«[1, 2, 3]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[1, 2, 3]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'dedup убирает соседние дубликаты — поэтому сначала sort.',
      'standalone': True,
      'expected': ['[1, 2, 3]']},
     {'id': 'r7-vec-enumerate',
      'mode': 'rust',
      'title': 'Индексы и значения',
      'statement': 'Для v = ["a", "b", "c"] напечатайте по строке «0: a», «1: b», «2: c» (enumerate).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '0: a\n'
                   '1: b\n'
                   '2: c',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'for (i, x) in v.iter().enumerate()',
      'standalone': True,
      'expected': ['0: a', '1: b', '2: c']},
     {'id': 'r7-vec-filter-collect',
      'mode': 'rust',
      'title': 'Фильтр',
      'statement': 'Из вектора [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] соберите в новый вектор только числа, кратные '
                   '3 (filter + collect). «[3, 6, 9]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[3, 6, 9]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'v.iter().filter(|x| **x % 3 == 0).cloned().collect()',
      'standalone': True,
      'expected': ['[3, 6, 9]']},
     {'id': 'r7-vec-map-collect',
      'mode': 'rust',
      'title': 'Квадраты',
      'statement': 'Постройте вектор квадратов чисел 1…6 (map и collect): «[1, 4, 9, 16, 25, 36]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[1, 4, 9, 16, 25, 36]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '(1..=6).map(|x| x * x).collect()',
      'standalone': True,
      'expected': ['[1, 4, 9, 16, 25, 36]']},
     {'id': 'r7-grid-print',
      'mode': 'rust',
      'title': 'Сетка 3×3',
      'statement': 'Объявите двумерный массив grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] и напечатайте его '
                   'построчно: три строки «1 2 3», «4 5 6», «7 8 9».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '1 2 3\n'
                   '4 5 6\n'
                   '7 8 9',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Каждую строку превратите в Vec<String> и склейте через join(" ").',
      'standalone': True,
      'expected': ['1 2 3', '4 5 6', '7 8 9']},
     {'id': 'r7-grid-diag',
      'mode': 'rust',
      'title': 'Диагональ',
      'statement': 'Для той же сетки grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] посчитайте сумму главной '
                   'диагонали (элементы grid[i][i]): «15».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '15',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Цикл по i и grid[i][i].',
      'standalone': True,
      'expected': ['15']},
     {'id': 'r7-fn-sum-slice',
      'mode': 'rust',
      'title': 'Сумма среза',
      'statement': 'Напишите функцию sum(v: &[i32]) -> i32, возвращающую сумму элементов среза.',
      'starter': 'fn sum(v: &[i32]) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let arr = [1, 2, 3];\n'
                '    let vec = vec![10, 20, 30, 40];\n'
                '    println!("{}", sum(&arr));\n'
                '    println!("{}", sum(&vec));\n'
                '    println!("{}", sum(&vec[1..3]));\n'
                '    println!("{}", sum(&[]));\n'
                '}\n',
      'hint': 'Срез принимает массив, вектор и часть вектора.',
      'expected': ['6', '100', '50', '0']},
     {'id': 'r7-fn-max',
      'mode': 'rust',
      'title': 'Максимум среза',
      'statement': 'Напишите функцию largest(v: &[i32]) -> i32, возвращающую наибольший элемент (срез не '
                   'пуст).',
      'starter': 'fn largest(v: &[i32]) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", largest(&[3, 9, 2]));\n'
                '    println!("{}", largest(&[-5, -2, -9]));\n'
                '    println!("{}", largest(&[7]));\n'
                '}\n',
      'hint': 'Начните с v[0] и сравнивайте со всеми.',
      'expected': ['9', '-2', '7']},
     {'id': 'r7-fn-reverse',
      'mode': 'rust',
      'title': 'Развернуть вектор',
      'statement': 'Напишите функцию reversed(v: &[i32]) -> Vec<i32>, возвращающую новый вектор с элементами '
                   'в обратном порядке (исходный не менять).',
      'starter': 'fn reversed(v: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let a = vec![1, 2, 3, 4];\n'
                '    println!("{:?}", reversed(&a));\n'
                '    println!("{:?}", a);\n'
                '    println!("{:?}", reversed(&[]));\n'
                '}\n',
      'hint': 'v.to_vec() делает копию, которую можно изменить.',
      'expected': ['[4, 3, 2, 1]', '[1, 2, 3, 4]', '[]']},
     {'id': 'r7-fn-count-even',
      'mode': 'rust',
      'title': 'Сколько чётных',
      'statement': 'Напишите функцию count_even(v: &[i32]) -> usize: число чётных элементов (включая 0 и '
                   'отрицательные).',
      'starter': 'fn count_even(v: &[i32]) -> usize {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", count_even(&[1, 2, 3, 4, 5, 6]));\n'
                '    println!("{}", count_even(&[-2, 0, 7]));\n'
                '    println!("{}", count_even(&[]));\n'
                '}\n',
      'hint': 'x % 2 == 0 для ссылки x работает, как для числа.',
      'expected': ['3', '2', '0']},
     {'id': 'r7-fn-minmax-tuple',
      'mode': 'rust',
      'title': 'Минимум и максимум парой',
      'statement': 'Напишите функцию min_max(v: &[i32]) -> (i32, i32): пара (наименьшее, наибольшее) для '
                   'непустого среза.',
      'starter': 'fn min_max(v: &[i32]) -> (i32, i32) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", min_max(&[4, -1, 9, 3]));\n'
                '    println!("{:?}", min_max(&[5]));\n'
                '    println!("{:?}", min_max(&[2, 2, 2]));\n'
                '}\n',
      'hint': 'Две переменные lo и hi и кортеж в конце.',
      'expected': ['(-1, 9)', '(5, 5)', '(2, 2)']},
     {'id': 'r7-fn-dot',
      'mode': 'rust',
      'title': 'Скалярное произведение',
      'statement': 'Напишите функцию dot(a: &[i32], b: &[i32]) -> i32: сумма произведений соответствующих '
                   'элементов (срезы одной длины).',
      'starter': 'fn dot(a: &[i32], b: &[i32]) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", dot(&[1, 2, 3], &[4, 5, 6]));\n'
                '    println!("{}", dot(&[], &[]));\n'
                '    println!("{}", dot(&[-1, 2], &[3, 4]));\n'
                '}\n',
      'hint': 'Цикл по индексам от 0 до a.len().',
      'expected': ['32', '0', '5']},
     {'id': 'r7-fix-mut-vec',
      'mode': 'rust',
      'title': 'Исправьте: вектор без mut',
      'statement': 'Программа не собирается: метод push меняет вектор, а он объявлен неизменяемым. Исправьте '
                   'объявление; результат «[1, 2, 3, 4]».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[1, 2, 3, 4]',
      'starter': 'fn main() {\n    let v = vec![1, 2, 3];\n    v.push(4);\n    println!("{:?}", v);\n}\n',
      'driver': '',
      'hint': 'Добавьте mut: let mut v.',
      'standalone': True,
      'expected': ['[1, 2, 3, 4]']}]}
