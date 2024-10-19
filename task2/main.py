import csv
from typing import Optional, List


class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.children: List['Node'] = []
        self.parent: Optional['Node'] = None  # Родитель узла

    def add_child(self, child: 'Node') -> None:
        self.children.append(child)
        child.parent = self  # Устанавливаем родителя для потомка


class Tree:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def insert(self, value: int, parent: Optional[Node] = None) -> Node:
        new_node = Node(value)

        if self.root is None:
            self.root = new_node
            return self.root

        if parent is None:
            raise ValueError("Parent can't be None")

        parent.add_child(new_node)
        return new_node

    def find(self, value: int) -> Optional[Node]:
        if self.root is None:
            return None
        return self._find_recursive(value, self.root)

    def _find_recursive(self, value: int, node: Node) -> Optional[Node]:
        if node.value == value:
            return node

        for child in node.children:
            found = self._find_recursive(value, child)
            if found:
                return found

        return None

    def get_all_nodes(self) -> List[Node]:
        """Возвращает список всех узлов дерева."""
        nodes = []
        if self.root:
            self._collect_nodes(self.root, nodes)
        return nodes

    def _collect_nodes(self, node: Node, nodes: List[Node]) -> None:
        """Рекурсивно собирает все узлы дерева."""
        nodes.append(node)
        for child in node.children:
            self._collect_nodes(child, nodes)

    def extensional_length(self, node: Node, relation_type: str) -> int:
        """Возвращает экстенсиональную длину для заданного узла по типу отношения."""
        if relation_type == 'r1':
            return len(node.children)  # Непосредственное управление (количество детей)
        elif relation_type == 'r2':
            return 1 if node.parent else 0  # Непосредственное подчинение (есть ли родитель)
        elif relation_type == 'r3':
            return self._count_descendants(node)  # Опосредованное управление (все потомки)
        elif relation_type == 'r4':
            return self._count_ancestors(node)  # Опосредованное подчинение (все предки)
        elif relation_type == 'r5':
            return self._count_siblings(node)  # Соподчинение на одном уровне (узлы с тем же родителем)
        else:
            raise ValueError("Invalid relation type.")

    def _count_descendants(self, node: Node) -> int:
        """Подсчитывает количество всех потомков узла (опосредованное управление)."""
        count = 0
        for child in node.children:
            count += 1 + self._count_descendants(child)
        return count

    def _count_ancestors(self, node: Node) -> int:
        """Подсчитывает количество всех предков узла (опосредованное подчинение)."""
        count = 0
        current = node.parent
        while current:
            count += 1
            current = current.parent
        return count

    def _count_siblings(self, node: Node) -> int:
        """Подсчитывает количество узлов на одном уровне с текущим (соподчинение)."""
        if node.parent is None:
            return 0
        return len(node.parent.children) - 1  # Количество "братьев и сестер"


def main():
    path = "C:\\development\\Python\\Системный Анализ\\task2\\task2.csv"
    output_path = "extensional_lengths.csv"

    tree = Tree()

    # Чтение структуры дерева из файла
    with open(path, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            parent_node = int(row[0])
            child_node = int(row[1])

            if not tree.find(parent_node):
                new_node = tree.insert(parent_node)
                tree.insert(child_node, new_node)
            else:
                tree.insert(child_node, tree.find(parent_node))

    # Подсчет экстенсиональных длин для всех узлов и всех отношений
    nodes = tree.get_all_nodes()
    relation_types = ['r1', 'r2', 'r3', 'r4', 'r5']

    # Запись результата в CSV
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Node', 'r1', 'r2', 'r3', 'r4', 'r5']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for node in nodes:
            row = {'Node': node.value}
            for relation in relation_types:
                row[relation] = tree.extensional_length(node, relation)
            writer.writerow(row)

    print(f"Extensional lengths have been written to {output_path}")


if __name__ == '__main__':
    main()
