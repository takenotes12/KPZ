from graphviz import Digraph

dot = Digraph(comment='UC6: Збірка комп\'ютера')

dot.node('A', 'Вхід у систему')
dot.node('B', 'Обрати "Збірка комп\'ютера"')
dot.node('C', 'Показати список замовлень')
dot.node('D', 'Обрати замовлення')
dot.node('E', 'Перевірка комплектуючих')
dot.node('F', 'Почати складання')
dot.node('G', 'Оновити статус: У процесі')
dot.node('H', 'Завершити складання')
dot.node('I', 'Оновити статус: Зібрано')
dot.node('J', 'Повідомити тестувальний відділ')
dot.node('K', 'Комплектуючі відсутні (альтернатива)')
dot.node('L', 'Повідомити відділ постачання')

# Основний потік
dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'HI', 'IJ'])

# Альтернативний потік
dot.edge('E', 'K', label='Немає деталей')
dot.edge('K', 'L')

# Вивід
dot.render('uc6_flowchart', format='png', cleanup=True)
