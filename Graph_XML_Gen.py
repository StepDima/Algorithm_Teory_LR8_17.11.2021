def main():
    flag = True
    name = input('Введите имя графа: ')
    lines = []
    points = []
    option = '0'
    while flag:
        tmp = input(
            "Введите название элемента, который хотите добавить: 'point' или 'line'-- или 'show', чтобы показать добавленные элементы:\n")
        option = option if tmp == '' else tmp
        if 'point' is option:  # сюда бы Python 3.10 с его pattern matching...
            p_name, p_x, p_y = input("Введите имя вершины, координаты х и у в указанном порядке:\n").split()
            points.append(f'<point id="{p_name}" x="{p_x}" y="{p_y}" />')
        elif 'line' == option:
            l_name, l_start, l_end, l_weight = input(
                "Введите номер ребра, стартовую и конечную вершины, вес ребра в указанном порядке:\n").split()
            lines.append(f' <line id="{l_name}" from="{l_start}" to="{l_end}" power="{l_weight}" />')
        elif 'show' == option:
            print('\n'.join(lines))
            print('\n'.join(points))
        else:
            flag = False
    str_points = '\n\t\t\t\t'.join(points)
    str_lines = '\n\t\t\t\t'.join(lines)
    print('\n'.join(points))
    print('\n'.join(lines))
    filename = input("Введите ИМЯ файла для записи: ")
    fout = open(f'{filename}.xml', 'w')
    result = f'''<?xml version="1.0" encoding="windows-1251"?>
        <graph_data>
            <graph id="1">
                <title>{name}</title>
                <points>
                    {str_points}
                </points>
                <lines>
                    {str_lines}
                </lines>
            </graph>
        </graph_data>
    '''
    fout.write(result)
    fout.close()


if __name__ == '__main__':
    main()
